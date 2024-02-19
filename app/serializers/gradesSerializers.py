def messageEntity(message) -> dict:
    return {
        "id": str(message["_id"]),
        "listGrades": message["listGrades"],
        "created_at": message["created_at"],
    }


def messageListEntity(messages) -> list:
    return [messageEntity(message) for message in messages]