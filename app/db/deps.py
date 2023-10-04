from typing import Generator

from db.session import SingletonDB
from sqlalchemy.orm import scoped_session

# Useful for serverless ms
# SingletonDB.default_engine_params = {"poolclass": NullPool, "connect_args": {"connect_timeout": 10}}


def get_session() -> Generator:
    sess = None
    try:
        sess = scoped_session(SingletonDB.get_db())
        yield sess
    finally:
        if sess:
            sess.close()


def get_ro_session() -> Generator:
    sess = None
    try:
        sess = scoped_session(SingletonDB.get_ro_db())
        # This is actually what makes this session RO.
        sess.flush = lambda: None
        yield sess
    finally:
        if sess:
            sess.close()
