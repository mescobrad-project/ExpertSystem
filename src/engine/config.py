from os import getenv

START_EVENT = getenv("WFE_START_EVENT", "StartEvent")
END_EVENT = getenv("WFE_END_EVENT", "EndEvent")
EXCLUSIVE_GATEWAY = getenv("WFE_EXCLUSIVE_GATEWAY", "ExclusiveGateway")
PARALLEL_GATEWAY = getenv("WFE_PARALLEL_GATEWAY", "ParallelGateway")
MANUAL_TASK = getenv("WFE_MANUAL_TASK", "ManualTask")
SCRIPT_TASK = getenv("WFE_SCRIPT_TASK", "ScriptTask")
