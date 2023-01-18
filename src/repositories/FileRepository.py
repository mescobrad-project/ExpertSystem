from uuid import UUID
from sqlalchemy import or_
from ._base import BaseCRUD, Session, ModelType
from src.models._all import FileModel
from src.schemas.FileSchema import FileCreate, FileUpdate


class _FileRepository(BaseCRUD[FileModel, FileCreate, FileUpdate]):
    def search(self, db: Session, *, term: str = "") -> list[ModelType]:
        print(term)
        return (
            db.query(self.model)
            .filter(
                or_(
                    self.model.__ts_vector__.match(term),
                    self.model.object_name.like(f"%{term}%"),
                )
            )
            .limit(15)
            .all()
        )


FileRepository = _FileRepository(FileModel)
