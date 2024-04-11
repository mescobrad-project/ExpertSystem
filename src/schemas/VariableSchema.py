from ._association import VariableBase, VariableInDBBase


# Properties to receive on obj creation
class VariableCreate(VariableBase):
    name: str


# Properties to receive on obj update
class VariableUpdate(VariableBase):
    pass


# Properties to return to client
class Variable(VariableInDBBase):
    pass


# Properties stored in DB
class VariableInDB(VariableInDBBase):
    pass
