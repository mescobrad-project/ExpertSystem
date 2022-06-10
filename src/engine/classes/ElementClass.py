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
    def peri(self, name: str):
        _stepNumber = 0

        state = stateTemplate(_stepNumber)
        steps = [stepTemplate(_stepNumber, name)]

        return state, steps


class EndEvent(Element):
    def peri(self):
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


def Exclusive(details):
    manual = details["manual"] if details["manual"] else False
    inputs = len(details["inputs"])
    outputs = len(details["outputs"])

    response = {
        "complete": False,
        "next_steps": True,
        "rules": {"choice": "one"},
    }

    # check if it is converging
    # else it is diverging
    if inputs > 1:
        response["complete"] = True
    elif outputs > 1 and manual:
        pass
    else:
        raise Exception(f"Something went wrong with task: {details['name']}")

    return response


def Parallel(details):
    inputs = len(details["inputs"])
    outputs = len(details["outputs"])

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
        raise Exception(f"Something went wrong with task: {details['name']}")

    return response


def Manual():
    pass


def Script(_):
    response = {
        "rules": {"task": True},
    }

    return response


def get_class_from_task_name(elementName: str) -> Element:
    elements = {}
    elements[START_EVENT] = StartEvent
    elements[END_EVENT] = EndEvent
    elements[EXCLUSIVE_GATEWAY] = ExclusiveGateway
    elements[PARALLEL_GATEWAY] = Parallel
    elements[MANUAL_TASK] = Manual
    elements[SCRIPT_TASK] = Script

    if elementName not in elements:
        raise Exception("Not available element.")

    return elements[elementName]
