from os import getenv

START_EVENT = getenv("WFE_START_EVENT", "StartEvent")
END_EVENT = getenv("WFE_END_EVENT", "EndEvent")
EXCLUSIVE_GATEWAY = getenv("WFE_EXCLUSIVE_GATEWAY", "ExclusiveGateway")
PARALLEL_GATEWAY = getenv("WFE_PARALLEL_GATEWAY", "ParallelGateway")
MANUAL_TASK = getenv("WFE_MANUAL_TASK", "ManualTask")
SCRIPT_TASK = getenv("WFE_SCRIPT_TASK", "ScriptTask")
USER_TASK = getenv("WFE_USER_TASK", "UserTask")
DATA_STORE = getenv("WFE_DATA_STORE", "DataStore")
DATA_OBJECT = getenv("WFE_DATA_OBJECT", "DataObject")

XML_START_EVENT = "startEvent"
XML_END_EVENT = "endEvent"
XML_EXCLUSIVE_GATEWAY = "exclusiveGateway"
XML_PARALLEL_GATEWAY = "parallelGateway"
XML_MANUAL_TASK = "manualTask"
XML_SCRIPT_TASK = "scriptTask"
XML_FLOW = "sequenceFlow"
XML_INCOMING = "incoming"
XML_OUTGOING = "outgoing"
XML_ANNOTATION = "textAnnotation"
XML_ASSOCIATION = "association"
XML_USER_TASK = "userTask"
XML_DATA_INPUT_ASSOCIATION = "dataInputAssociation"
XML_DATA_OUTPUT_ASSOCIATION = "dataOutputAssociation"
XML_DATA_STORE_REFERENCE = "dataStoreReference"
XML_DATA_OBJECT_REFERENCE = "dataObjectReference"
XML_DATA_OBJECT = "dataObject"
XML_NAMESPACES = {
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "bpmn2": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}
XML_PARSER_INPUTS = "inputs"
XML_PARSER_OUTPUTS = "outputs"
XML_PARSER_DATA_INPUT_ASSOCIATIONS = "stores"
XML_PARSER_DATA_OUTPUT_ASSOCIATIONS = "stores"

KEY_OUTPUT = getenv("WFE_KEY_OUTPUT", "outputs")

SCRIPT_DIR = getenv("WFE_SCRIPT_DIR", "src/scripts")
