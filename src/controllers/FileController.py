from sqlalchemy.orm import Session
from src.repositories.FileRepository import FileRepository
from src.errors.ApiRequestException import NotFoundException
from ._base import BaseController


class _FileController(BaseController):
    def search(
        self,
        db: Session,
        term: str = "",
    ):
        data = self.repository.search(db=db, term=term)

        if not data:
            raise NotFoundException(details="Resource not found")

        return data


FileController = _FileController(FileRepository)
