from typing import Any, Union
from pydantic import BaseModel

class APIResponse(BaseModel):
    status: str
    message: str
    data: Union[Any, None] = None  # или просто `Any = None`

class ResponseTemplates:
    @staticmethod
    def success(data: Any = None, message: str = "Operation successful") -> APIResponse:
        return APIResponse(status="success", message=message, data=data)

    @staticmethod
    def error(message: str = "An error occurred", data: Any = None) -> APIResponse:
        return APIResponse(status="error", message=message, data=data)
