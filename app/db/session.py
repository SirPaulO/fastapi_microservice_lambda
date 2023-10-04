from typing import Any, Dict

from settings.db_settings import db_settings
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker


class SingletonDB:
    Session_instance = None
    Session_ro_instance = None

    default_engine_params: Dict = {}

    @classmethod
    def get_engine(cls, **kwargs: Any) -> Engine:
        db_protocol = db_settings.DBProtocol
        db_user = db_settings.DBUser
        db_password = db_settings.DBPassword
        db_host = db_settings.DBHost
        db_name = db_settings.DBName
        db_conn = db_settings.DBConnectionString

        if not db_host and not db_conn:
            raise ValueError("Invalid DB connection settings")

        if db_host:
            conn_str = f"{db_protocol}://{db_user}:{db_password}@{db_host}/{db_name}"
        else:
            conn_str = db_conn

        return create_engine(conn_str, **kwargs)

    @classmethod
    def get_db(cls) -> sessionmaker:
        if cls.Session_instance:
            return cls.Session_instance

        engine = cls.get_engine(**cls.default_engine_params)
        cls.Session_instance = sessionmaker(engine)
        return cls.Session_instance

    @classmethod
    def get_ro_db(cls) -> sessionmaker:
        if cls.Session_ro_instance:
            return cls.Session_ro_instance

        engine = cls.get_engine(isolation_level="READ UNCOMMITTED", **cls.default_engine_params)
        cls.Session_ro_instance = sessionmaker(engine, autoflush=False, autocommit=False)
        return cls.Session_ro_instance
