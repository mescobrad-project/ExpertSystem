from sqlalchemy.orm import Session
from src.errors.ApiRequestException import NotFoundException
from src.repositories.UserRepository import UserRepository
from ._base import BaseController


class _UserController(BaseController):
    def get_from_sub_and_provider(self, db: Session, *, sub: str, provider: str):
        data = self.repository.get_from_sub_and_provider(
            db=db, sub=sub, provider=provider
        )

        if not data:
            raise NotFoundException(details="Resource not found")

        return data


UserController = _UserController(UserRepository)
