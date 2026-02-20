from fastapi.responses import JSONResponse

def success_response(status_code: int, message: str, data=None):
    return JSONResponse(
        status_code=status_code,   
        content={
            "status_code": status_code,
            "message": message,
            "data": data,
        }
    )


def error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,   
        content={
            "status_code": status_code,
            "message": message,
        }
    )
