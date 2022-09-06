from .sql import models, schemas, crud
from .sql.database import SessionLocal, engine

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()