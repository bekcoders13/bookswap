from fastapi import HTTPException
from starlette import status


def get_in_db(db, model, ident: int):
    obj = db.query(model).filter(model.id == ident).first()
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bazada bunday {model.__name__} yo'q")
    return obj
