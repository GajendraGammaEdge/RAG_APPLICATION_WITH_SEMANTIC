
from fastapi import Request 
import logging

async def middle_ware_process(request:Request, call_next):
        logging.info("Middleware is activate")
        response = await call_next(request)
        return response

