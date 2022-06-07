from .dependencies import stepTemplate
from .config import (
    START_EVENT,
    END_EVENT,
    EXCLUSIVE_GATEWAY,
    PARALLEL_GATEWAY,
    MANUAL_TASK,
    SCRIPT_TASK,
)


class Event:
    @staticmethod
    def Start(name: str):
        _stepNumber = 0
        return {
            "state": {"completed": False, "success": False, "step": _stepNumber},
            "step": [stepTemplate(_stepNumber, name)],
        }

    @staticmethod
    def End(_):
        return {
            "complete": True,
            "finish": True,
            "rules": {
                "event": True,
                "complete": True,
                "finish": True,
            },
        }


class Gateway:
    @staticmethod
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

    @staticmethod
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


class Task:
    @staticmethod
    def Manual():
        pass

    @staticmethod
    def Script(_):
        response = {
            "rules": {"task": True},
        }

        return response


def Element(elementName: str) -> any:
    elements = {}
    elements[START_EVENT] = Event.Start
    elements[END_EVENT] = Event.End
    elements[EXCLUSIVE_GATEWAY] = Gateway.Exclusive
    elements[PARALLEL_GATEWAY] = Gateway.Parallel
    elements[MANUAL_TASK] = Task.Manual
    elements[SCRIPT_TASK] = Task.Script

    if elementName not in elements:
        raise Exception("Not available element.")

    return elements[elementName]
