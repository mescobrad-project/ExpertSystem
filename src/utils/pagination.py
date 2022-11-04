def paginate(count: int, skip: int, limit: int) -> dict:
    previous_link = ""
    previous_skip = 0
    next_link = ""
    next_skip = 0

    if skip - limit >= 0:
        previous_link = f"?skip={skip-limit}&limit={limit}"
        previous_skip = skip - limit
        if previous_skip >= count:
            previous_skip = count - limit

    if skip + limit < count:
        next_link = f"?skip={skip+limit}&limit={limit}"
        next_skip = skip + limit

    return {
        "previous_link": f"{previous_link}",
        "previous_skip": previous_skip,
        "next_link": f"{next_link}",
        "next_skip": next_skip,
    }


def append_query_in_uri(uri: str, query: str) -> str:
    if uri == "":
        return ""

    return f"{uri}&{query}"
