import xml.etree.ElementTree as ET
from ._base import CRUDBase
from src.models._all import WorkflowModel
from src.schemas.WorkflowSchema import WorkflowCreate, WorkflowUpdate
from src.engine.config import (
    START_EVENT,
    END_EVENT,
    EXCLUSIVE_GATEWAY,
    PARALLEL_GATEWAY,
    MANUAL_TASK,
    SCRIPT_TASK,
    USER_TASK,
    DATA_STORE,
    DATA_OBJECT,
    XML_START_EVENT,
    XML_END_EVENT,
    XML_EXCLUSIVE_GATEWAY,
    XML_PARALLEL_GATEWAY,
    XML_MANUAL_TASK,
    XML_SCRIPT_TASK,
    XML_FLOW,
    XML_INCOMING,
    XML_OUTGOING,
    XML_NAMESPACES,
    XML_PARSER_INPUTS,
    XML_PARSER_OUTPUTS,
    XML_ANNOTATION,
    XML_ASSOCIATION,
    XML_USER_TASK,
    XML_DATA_INPUT_ASSOCIATION,
    XML_DATA_OUTPUT_ASSOCIATION,
    XML_DATA_STORE_REFERENCE,
    XML_DATA_OBJECT_REFERENCE,
    XML_DATA_OBJECT,
    XML_PARSER_DATA_INPUT_ASSOCIATIONS,
    XML_PARSER_DATA_OUTPUT_ASSOCIATIONS,
)


def get_task_type(tag):
    if tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_START_EVENT}':
        return START_EVENT
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_END_EVENT}':
        return END_EVENT
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_EXCLUSIVE_GATEWAY}':
        return EXCLUSIVE_GATEWAY
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_PARALLEL_GATEWAY}':
        return PARALLEL_GATEWAY
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_MANUAL_TASK}':
        return MANUAL_TASK
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_SCRIPT_TASK}':
        return SCRIPT_TASK
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_USER_TASK}':
        return USER_TASK
    else:
        return END_EVENT


def get_store_type(tag):
    if tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_STORE_REFERENCE}':
        return DATA_STORE
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_OBJECT_REFERENCE}':
        return DATA_OBJECT
    else:
        return DATA_STORE


def get_property_type(tag):
    if tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_INCOMING}':
        return XML_PARSER_INPUTS
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_OUTGOING}':
        return XML_PARSER_OUTPUTS
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_INPUT_ASSOCIATION}':
        return XML_PARSER_DATA_INPUT_ASSOCIATIONS
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_OUTPUT_ASSOCIATION}':
        return XML_PARSER_DATA_OUTPUT_ASSOCIATIONS
    else:
        return None


def parse_flows(flows):
    data = {}

    for flow in flows:
        # print(flow.text, flow.tag, flow.attrib)
        data[flow.attrib["id"]] = {
            XML_PARSER_INPUTS: flow.attrib["sourceRef"],
            XML_PARSER_OUTPUTS: flow.attrib["targetRef"],
        }

    return data


def parse_annotations(annotations):
    data = {}

    for annotation in annotations:
        data[annotation.attrib["id"]] = []

        for info in annotation:
            data[annotation.attrib["id"]].append(info.text)

    return data


def parse_data_object_refs(data_object_refs):
    data = {}

    for data_object_ref in data_object_refs:
        data[data_object_ref.attrib["id"]] = {
            "object": data_object_ref.attrib["dataObjectRef"],
            "name": data_object_ref.attrib["name"],
            "type": get_store_type(data_object_ref.tag),
        }

    return data


def parse_data_store_refs(data_store_refs):
    data = {}

    for data_store_ref in data_store_refs:
        data[data_store_ref.attrib["id"]] = {
            "name": data_store_ref.attrib["name"],
            "type": get_store_type(data_store_ref.tag),
        }

    return data


def parse_associations(associations):
    data = {}

    for association in associations:
        data[association.attrib["sourceRef"]] = association.attrib["targetRef"]

    return data


def parse_data_input_associations(stores, associations):
    data = {}

    for association in associations:
        if association.tag == f'{{{XML_NAMESPACES["bpmn2"]}}}sourceRef':
            if association.text in stores.keys():
                data[association.text] = {"mode": "get"}
        else:
            if association.text in stores.keys():
                data[association.text] = {"mode": "set"}

    return data


class CRUDWorkflow(CRUDBase[WorkflowModel, WorkflowCreate, WorkflowUpdate]):
    def get_workflow_entity_types(self):
        return {
            "event": [START_EVENT, END_EVENT],
            "gateway": [EXCLUSIVE_GATEWAY, PARALLEL_GATEWAY],
            "task": [MANUAL_TASK, SCRIPT_TASK, USER_TASK],
            "store": [DATA_STORE, DATA_OBJECT],
        }

    def parse_xml(self, xml_str):
        xml_decoded = ET.fromstring(xml_str)

        processes = xml_decoded.findall("bpmn2:process", XML_NAMESPACES)
        # print(xml_decoded.text, xml_decoded.tag, xml_decoded.attrib)

        sequence_flows = {}
        text_annotations = {}
        associations = {}
        tasks = {}
        stores = {}

        for process in processes:
            sequence_flows = parse_flows(
                process.findall(f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_FLOW}')
            )

            text_annotations = parse_annotations(
                process.findall(f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_ANNOTATION}')
            )

            associations = parse_associations(
                process.findall(f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_ASSOCIATION}')
            )

            stores.update(
                parse_data_store_refs(
                    process.findall(
                        f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_STORE_REFERENCE}'
                    )
                )
            )
            stores.update(
                parse_data_object_refs(
                    process.findall(
                        f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_OBJECT_REFERENCE}'
                    )
                )
            )

            for child in process:
                if child.tag in [
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_FLOW}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_ANNOTATION}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_ASSOCIATION}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_INPUT_ASSOCIATION}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_STORE_REFERENCE}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_OBJECT_REFERENCE}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_DATA_OBJECT}',
                ]:
                    continue

                # print(child.text, child.tag, child.attrib)
                task_id = child.attrib["id"]
                tasks[task_id] = {
                    "type": get_task_type(child.tag),
                    "name": child.attrib.get("name") or task_id,
                }

                tasks[task_id]["manual"] = child.tag in [
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_EXCLUSIVE_GATEWAY}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_MANUAL_TASK}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_USER_TASK}',
                ]

                for prop in child:
                    # print(prop.text, prop.tag, prop.attrib)
                    mode = get_property_type(prop.tag)
                    if not mode:
                        continue

                    if mode not in tasks[task_id].keys():
                        tasks[task_id][mode] = []

                    if mode in [XML_PARSER_INPUTS, XML_PARSER_OUTPUTS]:
                        tasks[task_id][mode].append(sequence_flows[prop.text][mode])
                    elif mode in [
                        XML_PARSER_DATA_INPUT_ASSOCIATIONS,
                        XML_PARSER_DATA_OUTPUT_ASSOCIATIONS,
                    ]:
                        tasks[task_id][mode].append(
                            parse_data_input_associations(stores, prop)
                        )

                if child.tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_SCRIPT_TASK}':
                    tasks[task_id]["class"] = text_annotations[associations[task_id]]

        return [tasks, stores]


WorkflowController = CRUDWorkflow(WorkflowModel)
