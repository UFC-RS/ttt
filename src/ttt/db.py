import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


class Database:
    """Database connection manager."""

    def __init__(self):
        self._database_url = os.getenv("DATABASE_URL", "sqlite:///./ttt.db")
        self._engine = None
        self._session_local = None

    @property
    def engine(self):
        if self._engine is None:
            self._engine = create_engine(
                self._database_url, connect_args={"check_same_thread": False} if "sqlite" in self._database_url else {}
            )
        return self._engine

    @property
    def session_local(self):
        if self._session_local is None:
            self._session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        return self._session_local

    def get_db_session(self) -> Session:
        db = self.session_local()
        try:
            yield db
        finally:
            db.close()


db_instance = Database()
get_db_session = db_instance.get_db_session
