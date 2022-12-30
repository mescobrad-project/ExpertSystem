from src.models._all import UserModel
from src.schemas.ModuleCategorySchema import ModuleCategoryCreate, ModuleCategoryUpdate
from ._base import BaseCRUD, Session, ModelType, _parse_criteria


class _UserRepository(BaseCRUD[UserModel, ModuleCategoryCreate, ModuleCategoryUpdate]):
    def get_from_sub_and_provider(
        self, db: Session, *, sub: str, provider: str
    ) -> ModelType:
        return (
            db.query(self.model)
            .filter(
                *_parse_criteria(
                    self.model,
                    criteria={
                        "sub": sub,
                        "provider": provider,
                    },
                )
            )
            .first()
        )


UserRepository = _UserRepository(UserModel)
