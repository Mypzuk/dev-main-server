
from fastapi import HTTPException


# Класс для создания стандартных ответов
class ErrorTemplates:

    @staticmethod
    def user_already_exists(message: str = "This user is already registered"):
        raise HTTPException(
            status_code=404,
            detail={"message": message}
        )


    @staticmethod
    def not_found(message: str = f"User not found"):
        raise HTTPException(
            status_code=404,
            detail={"message": message}
        )

    @staticmethod
    def invalid_code(message: str = "Invalid verification code"):
        raise HTTPException(
            status_code=400,
            detail={"message": message}
        )
