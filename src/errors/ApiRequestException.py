from http.client import responses
from fastapi import status
from ._base import BaseFastApiException

error_id = "API Response"


class BadRequestException(BaseFastApiException):
    def __init__(
        self, message: str = responses[status.HTTP_400_BAD_REQUEST], details: any = None
    ) -> None:
        super().__init__(
            status.HTTP_400_BAD_REQUEST, message, details, error_id=error_id
        )


class UnauthorizedException(BaseFastApiException):
    def __init__(
        self,
        message: str = responses[status.HTTP_401_UNAUTHORIZED],
        details: any = None,
    ) -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED, message, details, error_id=error_id
        )


class ForbiddenException(BaseFastApiException):
    def __init__(
        self, message: str = responses[status.HTTP_403_FORBIDDEN], details: any = None
    ) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, message, details, error_id=error_id)


class NotFoundException(BaseFastApiException):
    def __init__(
        self, message: str = responses[status.HTTP_404_NOT_FOUND], details: any = None
    ) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, message, details, error_id=error_id)


class ConflictException(BaseFastApiException):
    def __init__(
        self, message: str = responses[status.HTTP_409_CONFLICT], details: any = None
    ) -> None:
        super().__init__(status.HTTP_409_CONFLICT, message, details, error_id=error_id)


class GoneException(BaseFastApiException):
    def __init__(
        self, message: str = responses[status.HTTP_410_GONE], details: any = None
    ) -> None:
        super().__init__(status.HTTP_410_GONE, message, details, error_id=error_id)


class ImATeapotException(BaseFastApiException):
    def __init__(
        self, message: str = responses[status.HTTP_418_IM_A_TEAPOT], details: any = None
    ) -> None:
        super().__init__(
            status.HTTP_418_IM_A_TEAPOT, message, details, error_id=error_id
        )


class InternalServerErrorException(BaseFastApiException):
    def __init__(
        self,
        message: str = responses[status.HTTP_500_INTERNAL_SERVER_ERROR],
        details: any = None,
    ) -> None:
        super().__init__(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            message,
            details,
            error_id=error_id,
        )


class NotImplementedException(BaseFastApiException):
    def __init__(
        self,
        message: str = responses[status.HTTP_501_NOT_IMPLEMENTED],
        details: any = None,
    ) -> None:
        super().__init__(
            status.HTTP_501_NOT_IMPLEMENTED, message, details, error_id=error_id
        )


class BadGatewayException(BaseFastApiException):
    def __init__(
        self, message: str = responses[status.HTTP_502_BAD_GATEWAY], details: any = None
    ) -> None:
        super().__init__(
            status.HTTP_502_BAD_GATEWAY, message, details, error_id=error_id
        )


class ServiceUnavailableException(BaseFastApiException):
    def __init__(
        self,
        message: str = responses[status.HTTP_503_SERVICE_UNAVAILABLE],
        details: any = None,
    ) -> None:
        super().__init__(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            message,
            details,
            error_id=error_id,
        )
