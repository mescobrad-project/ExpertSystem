# Import all the models, so that Base has them before being
# imported by Alembic
from ._base import Base

# Import tables with relationships from _associations
from ._association import (
    FeatureModel,
    VariableModel,
    UserModel,
    FileModel,
    ModuleCategoryModel,
    ModuleModel,
    WorkflowCategoryModel,
    WorkflowModel,
    RunModel,
)
