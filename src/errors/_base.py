from fastapi import HTTPException


class BaseFastApiException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        details: any = None,
        error_id: any = "Runtime",
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail={
                "message": message,
                "details": details,
                "id": error_id,
            },
        )
