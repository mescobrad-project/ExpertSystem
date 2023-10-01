from src.engine.utils.TemplateUtils import stateTemplate, stepTemplate
from src.engine.config import *


class Element:
    def pre(self):
        pass

    def peri(self):
        pass

    def post(self):
        pass


class StartEvent(Element):
    def peri(self, sid: str, name: str):
        _stepNumber = 0

        state = stateTemplate(_stepNumber)
        steps = [stepTemplate(_stepNumber, sid, name)]

        return state, steps


class EndEvent(Element):
    def pre(self):
        return {
            "complete": False,
            "next_steps": False,
            "end_event": True,
        }

    def post(self):
        return {
            "complete": True,
            "finish": True,
            "rules": {
                "event": True,
                "complete": True,
                "finish": True,
            },
        }


class ExclusiveGateway(Element):
    def pre(self):
        return {
            "complete": True,
            "next_steps": True,
            "rules": {"choice": "one"},
        }

    def post(self):
        return {
            "complete": False,
            "next_steps": True,
            "rules": {"choice": "one"},
        }


class ParallelGateway(Element):
    def pre(self):
        return {
            "complete": True,
            "check_converging_pending_tasks": True,
            "next_steps": True,
            "rules": {"choice": "wait_all"},
        }

    def post(self, task):
        inputs = len(task["inputs"])
        outputs = len(task["outputs"])

        response = {
            "complete": False,
            "next_steps": True,
            "rules": {"choice": "all"},
        }

        # check if it is converging
        # else it is diverging
        if inputs > 1:
            response["rules"]["choice"] = "wait_all"
        elif outputs > 1:
            pass
        else:
            raise Exception(f"Something went wrong with task: {task['name']}")

        return response


class ManualTask(Element):
    def pre(self):
        return {
            "complete": False,
            "next_steps": True,
        }

    def post(self):
        return {
            "rules": {"complete": True},
        }


class ScriptTask(Element):
    def pre(self):
        return {
            "complete": False,
            "next_steps": True,
        }

    def post(self):
        return {
            "rules": {"complete": True, "task": True},
        }


class UserTask(ManualTask):
    pass


class CallActivity(Element):
    def pre(self):
        return {
            "complete": False,
            "next_steps": True,
        }

    def post(self):
        return {
            "rules": {"complete": True, "task": True},
        }


class SendTask(ManualTask):
    def post(self):
        return {
            "rules": {
                "complete": False,
                "metadata": True,
                "store": {"type": "DataObject"},
            },
        }


class ReceiveTask(ManualTask):
    def post(self):
        return {
            "rules": {
                "complete": False,
                "metadata": True,
                "store": {"type": "DataObject"},
            },
        }


def get_class_from_task_name(elementName: str) -> Element:
    elements = {}
    elements[START_EVENT] = StartEvent
    elements[END_EVENT] = EndEvent
    elements[EXCLUSIVE_GATEWAY] = ExclusiveGateway
    elements[PARALLEL_GATEWAY] = ParallelGateway
    elements[MANUAL_TASK] = ManualTask
    elements[SCRIPT_TASK] = ScriptTask
    elements[USER_TASK] = UserTask
    elements[CALL_ACTIVITY] = CallActivity
    elements[SEND_TASK] = SendTask
    elements[RECEIVE_TASK] = ReceiveTask

    if elementName not in elements:
        raise Exception("Not available element.")

    return elements[elementName]
