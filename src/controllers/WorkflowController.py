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
    else:
        return END_EVENT


def get_flow_type(tag):
    if tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_INCOMING}':
        return XML_PARSER_INPUTS
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_OUTGOING}':
        return XML_PARSER_OUTPUTS
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


def parse_associations(associations):
    data = {}

    for association in associations:
        data[association.attrib["sourceRef"]] = association.attrib["targetRef"]

    return data


class CRUDWorkflow(CRUDBase[WorkflowModel, WorkflowCreate, WorkflowUpdate]):
    def get_workflow_entity_types(self):
        return {
            "event": [
                START_EVENT,
                END_EVENT,
            ],
            "gateway": [
                EXCLUSIVE_GATEWAY,
                PARALLEL_GATEWAY,
            ],
            "task": [
                MANUAL_TASK,
                SCRIPT_TASK,
            ],
        }

    def parse_xml(self, xml_str):
        xml_decoded = ET.fromstring(xml_str)

        processes = xml_decoded.findall("bpmn2:process", XML_NAMESPACES)
        # print(xml_decoded.text, xml_decoded.tag, xml_decoded.attrib)

        sequence_flows = {}
        text_annotations = {}
        associations = {}
        tasks = {}

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

            for child in process:
                if child.tag in [
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_FLOW}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_ANNOTATION}',
                    f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_ASSOCIATION}',
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
                ]

                for flow in child:
                    # print(flow.text, flow.tag, flow.attrib)
                    mode = get_flow_type(flow.tag)
                    if not mode:
                        continue

                    if mode not in tasks[task_id].keys():
                        tasks[task_id][mode] = []

                    tasks[task_id][mode].append(sequence_flows[flow.text][mode])

                if child.tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_SCRIPT_TASK}':
                    tasks[task_id]["class"] = text_annotations[associations[task_id]]

        return tasks


WorkflowController = CRUDWorkflow(WorkflowModel)
