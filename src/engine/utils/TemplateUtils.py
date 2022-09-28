from .Generators import getId, getDateTimeNow


def stateTemplate(stepNumber: int) -> dict:
    return {"completed": False, "success": False, "step": stepNumber}


def stepTemplate(number: int | None, sid: str, task_name: str) -> list[dict]:
    return {
        "id": getId(),
        "number": number,
        "start": getDateTimeNow(),
        "finish": "",
        "sid": sid,
        "name": task_name,
    }


def pending_and_waiting_template(pending, waiting):
    return {"pending": pending, "waiting": waiting}
