import xml.etree.ElementTree as ET
from src.engine.config import (
    RECEIVE_TASK,
    SEND_TASK,
    START_EVENT,
    END_EVENT,
    EXCLUSIVE_GATEWAY,
    PARALLEL_GATEWAY,
    MANUAL_TASK,
    SCRIPT_TASK,
    USER_TASK,
    CALL_ACTIVITY,
    DATA_STORE,
    DATA_OBJECT,
    XML_EXCLUSIVE_GATEWAY,
    XML_MANUAL_TASK,
    XML_RECEIVE_TASK,
    XML_SCRIPT_TASK,
    XML_FLOW,
    XML_NAMESPACES,
    XML_PARSER_INPUTS,
    XML_PARSER_OUTPUTS,
    XML_ANNOTATION,
    XML_ASSOCIATION,
    XML_SEND_TASK,
    XML_USER_TASK,
    XML_CALL_ACTIVITY,
    XML_DATA_INPUT_ASSOCIATION,
    XML_DATA_STORE_REFERENCE,
    XML_DATA_OBJECT_REFERENCE,
    XML_DATA_OBJECT,
    XML_PARSER_DATA_INPUT_ASSOCIATIONS,
    XML_PARSER_DATA_OUTPUT_ASSOCIATIONS,
)
from src.engine.utils.XmlUtils import (
    get_task_type,
    get_property_type,
    parse_flows,
    parse_annotations,
    parse_data_object_refs,
    parse_data_store_refs,
    parse_associations,
    parse_data_input_associations,
)


def get_workflow_entity_types():
    return {
        "event": [START_EVENT, END_EVENT],
        "gateway": [EXCLUSIVE_GATEWAY, PARALLEL_GATEWAY],
        "task": [
            MANUAL_TASK,
            SCRIPT_TASK,
            USER_TASK,
            SEND_TASK,
            RECEIVE_TASK,
            CALL_ACTIVITY,
        ],
        "store": [DATA_STORE, DATA_OBJECT],
    }


def parse_xml(xml_str):
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
                "name": (
                    child.attrib.get("name") if child.attrib.get("name") else task_id
                ),
            }

            tasks[task_id]["manual"] = child.tag in [
                f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_EXCLUSIVE_GATEWAY}',
                f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_MANUAL_TASK}',
                f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_USER_TASK}',
                f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_SEND_TASK}',
                f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_RECEIVE_TASK}',
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

            if child.tag in [
                f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_SCRIPT_TASK}',
                f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_SEND_TASK}',
            ]:
                tasks[task_id]["class"] = text_annotations[associations[task_id]]

    return [tasks, stores]
