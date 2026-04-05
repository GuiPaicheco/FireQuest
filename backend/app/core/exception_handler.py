from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import HTTPException

async def global_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": exc.detail
            }
        )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Erro interno do servidor"
        }
    )