import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine 
from sqlalchemy_utils import create_database, database_exists
from ..sql.database import Base
from ..dependencies import get_db
from sqlalchemy.orm import Session
from app.main import app 

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgresadmin@favs-aws-db-instance.cggedkgmg7yn.us-west-2.rds.amazonaws.com:5432/time_tracking_db_test"

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    connection.begin()

    db = Session(bind=connection)

    app.dependency_overrides[get_db] = lambda: db

    yield db 

    db.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db 

    with TestClient(app) as c:
        yield c