from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from src.database import get_db
from src.utils.pagination import paginate


class RouteHelper:
    def __init__(self, Controller) -> None:
        self.Controller = Controller

    def read_multi(
        self,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        order: str = None,
        direction: str = None,
        criteria: dict = {},
    ):
        try:
            if skip < 0:
                skip = 0

            data = self.Controller.get_multi(
                db,
                skip=skip,
                limit=limit,
                criteria=criteria,
                order=order,
                direction=direction,
            )
            count_all = self.Controller.count(db, criteria=criteria)

            paging = paginate(count_all, skip, limit)
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

        return {
            "data": data,
            "paging": paging,
            "count": count_all,
        }

    def read(
        self,
        id: UUID,
        db: Session = Depends(get_db),
        criteria: dict = {},
    ):
        data = self.Controller.get(db=db, id=id, criteria=criteria)
        if not data:
            raise HTTPException(status_code=404, detail="Requested resource not found")

        return data
