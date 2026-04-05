def success_response(data):
    return {
        "success": True,
        "data": data
    }


def error_response(message):
    return {
        "success": False,
        "error": message
    }