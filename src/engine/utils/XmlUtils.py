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
    DATA_STORE,
    DATA_OBJECT,
    XML_RECEIVE_TASK,
    XML_SEND_TASK,
    XML_START_EVENT,
    XML_END_EVENT,
    XML_EXCLUSIVE_GATEWAY,
    XML_PARALLEL_GATEWAY,
    XML_MANUAL_TASK,
    XML_SCRIPT_TASK,
    XML_INCOMING,
    XML_OUTGOING,
    XML_NAMESPACES,
    XML_PARSER_INPUTS,
    XML_PARSER_OUTPUTS,
    XML_USER_TASK,
    XML_DATA_INPUT_ASSOCIATION,
    XML_DATA_OUTPUT_ASSOCIATION,
    XML_DATA_STORE_REFERENCE,
    XML_DATA_OBJECT_REFERENCE,
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
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_SEND_TASK}':
        return SEND_TASK
    elif tag == f'{{{XML_NAMESPACES["bpmn2"]}}}{XML_RECEIVE_TASK}':
        return RECEIVE_TASK
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
