from uuid import UUID
from sqlalchemy import or_, and_
from ._base import BaseCRUD, Session, ModelType
from src.models._all import FileModel
from src.schemas.FileSchema import FileCreate, FileUpdate


class _FileRepository(BaseCRUD[FileModel, FileCreate, FileUpdate]):
    def search(self, db: Session, *, ws_id: int, term: str = "") -> list[ModelType]:
        return (
            db.query(self.model)
            .filter(
                and_(
                    or_(
                        self.model.__ts_vector__.match(term),
                        # self.model.object_name.like(f"%{term}%"),
                    ),
                    self.model.ws_id == ws_id,
                )
            )
            .limit(15)
            .all()
        )


FileRepository = _FileRepository(FileModel)
