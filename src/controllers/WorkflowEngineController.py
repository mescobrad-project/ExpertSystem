from uuid import UUID
from src.config import QB_API_BASE_URL, ES_UI_BASE_URL
from src.controllers.ObjectStorageController import ObjectStorageController
from src.engine.config import (
    RECEIVE_TASK,
    SEND_TASK,
    MANUAL_TASK,
    SCRIPT_TASK,
    USER_TASK,
    CALL_ACTIVITY,
)
from src.engine.main import WorkflowEngine
from src.engine.classes.ElementClass import get_class_from_task_name
from src.engine.utils.Generators import getId
from src.engine.utils.TemplateUtils import pending_and_waiting_template
from src.errors.ApiRequestException import InternalServerErrorException
from src.schemas.FileSchema import FileCreate
from src.schemas.RequestBodySchema import (
    CallActivityParams,
    TaskMetadataBodyParameter,
    ScriptTaskCompleteParams,
)
from src.clients.artificialintelligence import client as ai_client
from src.clients.dataanalytics import client as da_client
from src.models._all import RunModel


class BaseEngineController:
    def initialize(self, tasks):
        engine = WorkflowEngine(tasks)
        engine.initialize()
        engine.complete_step()
        state, steps, queue = engine.get_workflow_status()

        return state, steps, queue

    def _continue_from(self, workflow, run):
        engine = WorkflowEngine(workflow["tasks"])
        engine.continue_from(
            run["workflow_id"], run["id"], run["state"], run["steps"], run["queue"]
        )
        return engine

    def get_waiting_steps(self, workflow, run):
        engine = self._continue_from(workflow, run)
        return engine.get_waiting_steps()

    def run_pending_step(self, workflow, run, step_id: UUID):
        engine = self._continue_from(workflow, run)

        # check if current step is not completed
        # if not, then return current info
        current_step_completed = engine.check_if_current_step_completed()
        if current_step_completed is not None:
            return current_step_completed
        # else, check for next steps to display

        index, active = engine.find_active_step(engine.queue, step_id)

        details = engine.graph.find_task_by_id(active["sid"])
        element = get_class_from_task_name(details["type"])()
        actions = element.pre()

        if actions["complete"]:
            if not actions.get("check_converging_pending_tasks"):
                engine.set_step_completed(active)

        if actions["next_steps"]:
            waiting = []

            if actions.get("check_converging_pending_tasks"):
                waiting = engine.get_incomplete_converging_tasks(active["sid"])

            if len(waiting) == 0:
                engine.add_to_queue(active["sid"])
                engine.set_task_as_active_step(active)
                if actions["complete"]:
                    engine.set_step_completed(active)
                engine.remove_from_bucket(engine.queue, index)

        if actions.get("end_event") is not None and actions.get("end_event"):
            engine.set_task_as_active_step(active)
            engine.remove_from_bucket(engine.queue, index)

        return pending_and_waiting_template(active, engine.queue)

    def _set_parallelqueue_task_to_queue(self, engine, active, step_id):
        index, next_step = engine.find_active_step(engine.queue, step_id)
        engine.add_current_to_queue(next_step["sid"])
        engine.remove_from_bucket(
            engine.queue[index]["and"],
            engine.get_step_position_index(engine.queue[index]["and"], next_step["id"]),
        )
        steps_waiting = engine.count_waiting_steps_in_bucket(engine.queue[index]["and"])

        if steps_waiting == 0:
            engine.set_step_completed(active)
            engine.remove_from_bucket(engine.queue, index)

        return next_step

    def _prepare_step(self, workflow, run, step_id: UUID):
        engine = self._continue_from(workflow, run)

        (_, active) = engine.find_active_step(engine.steps, step_id)

        details = engine.graph.find_task_by_id(active["sid"])
        element = get_class_from_task_name(details["type"])()
        try:
            rules = (element.post(details))["rules"]
        except TypeError:
            rules = (element.post())["rules"]

        return (engine, active, details, rules)

    def gateway_exclusive_choice(
        self, workflow, run, step_id: UUID, next_step_id: UUID
    ):
        (engine, active, _, rules) = self._prepare_step(workflow, run, step_id)

        if "choice" in rules.keys() and rules["choice"] == "one":
            index, next_step = engine.find_active_step(engine.queue, next_step_id)
            engine.set_step_completed(active)
            engine.add_current_to_queue(next_step["sid"])
            engine.remove_from_bucket(engine.queue, index)
            active = next_step

        return {"pending": active}

    def gateway_parallel_choice(self, workflow, run, step_id: UUID, next_step_id: UUID):
        (engine, active, _, rules) = self._prepare_step(workflow, run, step_id)

        if "choice" in rules.keys():
            if rules["choice"] == "all":
                self._set_parallelqueue_task_to_queue(engine, active, next_step_id)
            elif rules["choice"] == "wait_all":
                # check for previous steps completion
                waiting = engine.get_incomplete_converging_tasks()

                if len(waiting) > 0:
                    return {
                        "display": "Please complete the following tasks first",
                        "pending": active,
                    }

                self._set_parallelqueue_task_to_queue(engine, active, next_step_id)

        return {"pending": active}

    def task_exec(
        self,
        workflow,
        run,
        ws_id: int,
        step_id: UUID,
        data: dict,
    ):
        (engine, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if "task" in rules.keys():
            if "metadata" in active.keys():
                return {"pending": active}

            base_save_path = ai_client.get_base_save_path()
            if not base_save_path.get("is_success"):
                raise Exception(base_save_path)

            for module_name in details["class"]:
                if module_name.startswith("querybuilder"):
                    active["metadata"] = {
                        "url": f"{QB_API_BASE_URL}/{engine.run_id}/{step_id}",
                        "workflow_id": engine.workflow_id,
                        "run_id": engine.run_id,
                        "ws_id": int(ws_id),
                        "base_save_path": {
                            "bucket_name": base_save_path.get("bucket_name"),
                            "object_name": f"{base_save_path.get('object_name')}/{engine.workflow_id}/{engine.run_id}/{step_id}",
                        },
                        "data_use": {
                            "datalake": data.get("data_input").get("datalake"),
                            "trino": data.get("data_input").get("trino"),
                        },
                    }
                else:
                    func_name = data.get("module", "/").split("/")[-1]

                    try:
                        if not da_client.check_if_function_exists(func_name):
                            return {"error": "Function name does not exist!"}
                    except:
                        raise Exception("Cannot reach DataAnalytics")

                    metadata_to_send = {}

                    if data.get("data_input"):
                        metadata_to_send["files"] = []
                        if "datalake" in data.get("data_input"):
                            for obj in data["data_input"]["datalake"]:
                                metadata_to_send["files"].append(
                                    {
                                        "bucket": obj["bucket_name"],
                                        "file": obj["object_name"],
                                    }
                                )
                    if data.get("ref_completed_task"):
                        metadata_to_send["reference"] = data.get("ref_completed_task")

                    request_body = {
                        "workflow_id": str(engine.workflow_id),
                        "run_id": str(engine.run_id),
                        "ws_id": int(ws_id),
                        "step_id": str(step_id),
                        "datalake": {
                            "bucket_name": base_save_path.get("bucket_name"),
                            "object_name": f"{base_save_path.get('object_name')}/{engine.workflow_id}",
                        },
                        "function": func_name,
                        "metadata": metadata_to_send,
                    }

                    response = {}

                    try:
                        response = da_client.put(request_body)
                    except:
                        raise Exception("Cannot reach DataAnalytics")

                    if not response.get("is_success"):
                        return response

                    response["class"] = data.get("module")
                    response["initial_request"] = request_body
                    # response.update(request_body)

                    active["metadata"] = response

        return {"pending": active}

    def task_script_complete(
        self,
        workflow,
        run,
        step_id: UUID,
        FileCreateFn,
        db,
        FileCreateSchema: FileCreate,
        params: ScriptTaskCompleteParams | None = None,
    ):
        (engine, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if "complete" in rules.keys():
            if details["type"] not in [
                SCRIPT_TASK,
            ]:
                raise Exception("Action forbidden.")

            if params["data"].get("datalake") or params["data"].get("trino"):
                task_stores = workflow["tasks"][active["sid"]].get("stores")

                if task_stores and len(task_stores) > 0:
                    ### Start Bad Code
                    to_store = {}

                    for store in task_stores:
                        sid = list(store.keys())[0]

                        mode = store[sid].get("mode")

                        if params.get("error") and params.error:
                            raise InternalServerErrorException(details=params.error)
                        else:
                            if mode not in ["set", "get"]:
                                continue

                            data = {mode: []}
                            if (
                                workflow["stores"][sid]["type"] == "DataObject"
                                and params["data"].get("datalake")
                                and len(params["data"]["datalake"]) > 0
                            ):
                                data[mode] = params["data"]["datalake"]

                                for datalake_object in params["data"]["datalake"]:
                                    if datalake_object.get(
                                        "bucket_name"
                                    ) and datalake_object.get("object_name"):
                                        name = datalake_object.get(
                                            "object_name", ""
                                        ).split("/")[-1]

                                        bucket_name = datalake_object.get(
                                            "bucket_name", ""
                                        )
                                        object_name = (
                                            datalake_object.get("object_name", "")
                                            .replace("/", " ")
                                            .replace("-", " ")
                                            .replace("_", " ")
                                            .replace(".", " ")
                                        )
                                        search = f"{bucket_name} {object_name}"

                                        FileCreateFn(
                                            db=db,
                                            obj_in=FileCreateSchema(
                                                name=name,
                                                ws_id=run.get("ws_id"),
                                                search=search,
                                                info=datalake_object,
                                            ),
                                        )
                            elif (
                                workflow["stores"][sid]["type"] == "DataStore"
                                and params["data"].get("trino")
                                and len(params["data"]["trino"]) > 0
                            ):
                                data[mode] = params["data"]["trino"]

                            # deserialize data because of python's/pydantic's poor handling
                            deserialized = []
                            for raw_data in data[mode]:
                                tmp = None
                                try:
                                    tmp = raw_data.dict()
                                except:
                                    tmp = raw_data
                                deserialized.append(tmp)

                            if len(deserialized) > 0:
                                to_store[sid] = {}
                                to_store[sid][mode] = deserialized
                    ### End Bad Code

                    if to_store:
                        state_id = getId()

                        engine.append_workflow_state_data(
                            {
                                "id": state_id,
                                "sid": active["sid"],
                                "step_number": active["number"],
                                "data": to_store,
                            }
                        )

                        if active.get("metadata"):
                            active["metadata"]["store"] = {
                                "state_data_id": state_id,
                                "state_data_number": len(engine.state["data"]) - 1,
                            }
                        else:
                            active["metadata"] = {
                                "store": {
                                    "state_data_id": state_id,
                                    "state_data_number": len(engine.state["data"]) - 1,
                                }
                            }

            engine.set_step_completed(active)

            # if "task" in rules.keys():
            #     (_, next_step) = engine.find_active_step(engine.queue)
            #     engine.set_task_as_active_step(next_step)
            #     engine.remove_from_bucket(
            #         engine.queue,
            #         engine.get_step_position_index(engine.queue, next_step["id"]),
            #     )

        return {"pending": active}

    def call_activity(
        self,
        workflow,
        run,
        step_id: UUID,
        data: CallActivityParams,
    ):
        (engine, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if details["type"] not in [
            CALL_ACTIVITY,
        ]:
            raise Exception("Action forbidden.")

        if "metadata" in active.keys():
            return {"pending": active, "created": False}

        active["metadata"] = {
            "url": f"{ES_UI_BASE_URL}/workflow/{str(data.workflow_id)}/run/{str(data.run_id)}",
            "parent": {
                "workflow_id": str(engine.workflow_id),
                "run_id": str(engine.run_id),
                "step_id": str(step_id),
            },
            "child": {"workflow_id": str(data.workflow_id), "run_id": str(data.run_id)},
        }

        return {
            "pending": active,
            "data": {
                "DataObject": self._get_data_refs(workflow, run, "DataObject"),
                "DataStore": self._get_data_refs(workflow, run, "DataStore"),
            },
            "variables": engine.state.get("variables"),
            "created": True,
        }

    def task_send(
        self,
        workflow,
        run,
        step_id: UUID,
        data: dict,
    ):
        (engine, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if "metadata" in rules.keys() and rules.get("metadata"):
            for ai_class in details["class"]:
                if not ai_client.router.check_if_route_is_available(ai_class):
                    continue

                for task in engine.queue:
                    if not task.get("sid") in details.get("outputs"):
                        continue

                    step_id_of_receive_task = task.get("id")
                    break

                instructions_response = ai_client.get_instructions_for_(ai_class)

                if not instructions_response.get("is_success"):
                    return instructions_response

                post_data_object = {}
                for key in instructions_response.get("key_name"):
                    if key == "workflow_id":
                        post_data_object[key] = str(engine.workflow_id)
                    elif key == "run_id":
                        post_data_object[key] = str(engine.run_id)
                    elif key == "step_id":
                        post_data_object[key] = step_id_of_receive_task
                    elif key == "data":
                        post_data_object[key] = data.get("data_input")
                    elif key == "user_input":
                        post_data_object[key] = data.get("user_input")
                    elif key == "params":
                        post_data_object[key] = data.get("params")

                response = ai_client.post_(ai_class, post_data_object)

                if not response.get("is_success"):
                    return response

                active["metadata"] = response

                engine.set_step_completed(active)

        return {"pending": active}

    def task_receive(
        self,
        workflow,
        run,
        step_id: UUID,
        data: dict,
    ):
        engine = self._continue_from(workflow, run)
        active = engine.find_task_in_bucket_by_id(engine.queue, str(step_id))
        details = engine.graph.find_task_by_id(active["sid"])
        element = get_class_from_task_name(details["type"])()
        try:
            rules = (element.post(details))["rules"]
        except TypeError:
            rules = (element.post())["rules"]

        if "metadata" in rules.keys() and rules.get("metadata"):
            active["metadata"] = data

        return {"pending": active}

    def task_complete(
        self,
        workflow,
        run,
        step_id: UUID,
        metadata: TaskMetadataBodyParameter | None = None,
    ):
        (engine, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if "complete" in rules.keys():
            # task = engine.find_task_in_bucket_by_id(engine.steps, step_id)

            if details["type"] not in [
                MANUAL_TASK,
                USER_TASK,
                RECEIVE_TASK,
                CALL_ACTIVITY,
            ]:
                raise Exception("Action forbidden.")

            task_stores = workflow["tasks"][active["sid"]].get("stores")

            if task_stores and len(task_stores) > 0:
                to_store = {}

                ### Start Bad Code
                for store in task_stores:
                    sid = list(store.keys())[0]
                    mode = store[sid].get("mode")

                    if metadata.error:
                        to_store["error"] = metadata.error
                    elif metadata.store.get(sid):
                        if mode not in ["set", "get"]:
                            continue

                        data = {}
                        data[mode] = metadata.store.get(sid).get(mode)

                        # deserialize data because of python's/pydantic's poor handling
                        deserialized = []
                        for raw_data in data[mode]:
                            deserialized.append(raw_data.dict())

                        to_store[sid] = {}
                        to_store[sid][mode] = deserialized
                ### End Bad Code

                state_id = getId()

                engine.append_workflow_state_data(
                    {
                        "id": state_id,
                        "sid": active["sid"],
                        "step_number": active["number"],
                        "data": to_store,
                    }
                )

                if active.get("metadata"):
                    active["metadata"]["store"] = {
                        "state_data_id": state_id,
                        "state_data_number": len(engine.state["data"]) - 1,
                    }
                else:
                    active["metadata"] = {
                        "store": {
                            "state_data_id": state_id,
                            "state_data_number": len(engine.state["data"]) - 1,
                        }
                    }

            if details["type"] == USER_TASK and metadata.variables:
                engine.state["variables"] = {
                    "input": metadata.variables["input"],
                    "output": metadata.variables["output"],
                }

            engine.set_step_completed(active)

            # if "task" in rules.keys():
            #     (_, next_step) = engine.find_active_step(engine.queue)
            #     engine.set_task_as_active_step(next_step)
            #     engine.remove_from_bucket(
            #         engine.queue,
            #         engine.get_step_position_index(engine.queue, next_step["id"]),
            #     )

        return {"pending": active}

    def event_actions(self, workflow, run, step_id: UUID):
        (engine, active, _, rules) = self._prepare_step(workflow, run, step_id)

        if "event" in rules.keys():
            if rules["complete"]:
                engine.set_step_completed(active)
                active = {}

            if rules["finish"]:
                engine.set_workflow_as_finished()

        return {"pending": active}

    def task_revert(self, workflow, run, *, step_id: UUID):
        (engine, active, details, _) = self._prepare_step(workflow, run, step_id)

        if details["type"] not in [
            MANUAL_TASK,
            SCRIPT_TASK,
            USER_TASK,
            SEND_TASK,
            RECEIVE_TASK,
        ]:
            return {"pending": active}

        engine.revert_step(step_id)

        return {"pending": active}

    def ping_step_status(self, workflow, run, step_id: UUID):
        engine = self._continue_from(workflow, run)

        (_, active) = engine.find_active_step(engine.steps, step_id)

        if "completed" not in active.keys():
            active["completed"] = False

        return {"step": active, "completed": active["completed"]}

    def get_task_metadata(self, workflow, run, step_id: UUID):
        (engine, active, details, rules) = self._prepare_step(workflow, run, step_id)

        if details["type"] not in [SCRIPT_TASK, CALL_ACTIVITY]:
            raise Exception("Action forbidden.")

        if "task" in rules.keys():
            if active.get("metadata"):
                file_refs = []
                if active["metadata"].get("store"):
                    for sid, data in run["state"]["data"][
                        active["metadata"]["store"]["state_data_number"]
                    ]["data"].items():
                        if sid in workflow["stores"].keys():
                            if workflow["stores"][sid]["type"] == "DataObject":
                                if "get" in data.keys():
                                    file_refs.extend(data["get"])
                                if "set" in data.keys():
                                    file_refs.extend(data["set"])
                active["metadata"]["datasets"] = file_refs

                for module_name in details.get("class", []):
                    if module_name.startswith("dataanalytics"):
                        base_save_path = ai_client.get_base_save_path()
                        if not base_save_path.get("is_success"):
                            raise Exception(base_save_path)

                        try:
                            bucket_name = base_save_path.get("bucket_name")
                            object_name = f"{base_save_path.get('object_name')}/{engine.workflow_id}/{engine.run_id}/{step_id}/info.json"
                            # bucket_name = "demo"
                            # object_name = "expertsystem/workflow/2b28ad6a-5f6c-49fc-af50-a58d0c43cb4b/3a21be76-2ea6-4e97-a04e-21544698f484/9419be1d-67db-4669-8197-20fd99088ab1/analysis_output/info.json"

                            active["metadata"][
                                "info"
                            ] = ObjectStorageController.get_object(
                                bucket_name, object_name
                            )
                        except:
                            pass
                            # S3 operation failed; code: AccessDenied, message: Access Denied., resource: /demo, request_id: 17906EB26AE2C91D, host_id: 36a147e7-9844-456b-b2fa-5aaae991d8ab, bucket_name: demo
                            # raise Exception("Cannot get info json")

                return {"data": active}

        return {"data": active}

    def _get_data_refs(self, workflow: dict, run: dict, data_type: str):
        file_refs = []

        for activity in run["state"]["data"]:
            for sid, data in activity["data"].items():
                if sid in workflow["stores"].keys():
                    if workflow["stores"][sid]["type"] == data_type:
                        if "get" in data.keys():
                            file_refs.extend(data["get"])
                        if "set" in data.keys():
                            file_refs.extend(data["set"])

        return file_refs

    def get_dataobject_refs(self, workflow: dict, run: dict):
        return self._get_data_refs(workflow, run, "DataObject")

    def get_datastore_refs(self, workflow: dict, run: dict):
        return self._get_data_refs(workflow, run, "DataStore")

    def get_previously_completed_steps(self, workflow, run, criteria: dict = {}):
        _steps = []

        for step in run.steps:
            if step["completed"]:
                task_type = workflow.tasks[step["sid"]]["type"]

                if criteria.get("exclude"):
                    if criteria["exclude"].get("not_in_type"):
                        if criteria["exclude"]["not_in_type"] != task_type:
                            continue

                data = {
                    "id": step["id"],
                    "sid": step["sid"],
                    "name": step["name"],
                    "type": task_type,
                    "metadata": step.get("metadata"),
                }

                if criteria.get("include"):
                    if criteria["include"].get("class"):
                        if step.get("metadata"):
                            if step["metadata"].get("class"):
                                if (
                                    criteria["include"]["class"]
                                    == step["metadata"]["class"]
                                ):
                                    _steps.append(data)
                else:
                    _steps.append(data)

        return _steps


WorkflowEngineController = BaseEngineController()
