from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
import pyodbc


SERVER = "localhost"
DATABASE = "CreditScoringDB"
USERNAME = "sa"
PASSWORD = "123456"
DRIVER = "ODBC Driver 17 for SQL Server"


# =========================
# SQLAlchemy connection
# =========================
connection_url = URL.create(
    "mssql+pyodbc",
    username=USERNAME,
    password=PASSWORD,
    host=SERVER,
    database=DATABASE,
    query={
        "driver": DRIVER,
        "TrustServerCertificate": "yes",
    },
)

engine = create_engine(
    connection_url,
    echo=False,
    future=True,
    fast_executemany=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


# =========================
# Optional: raw pyodbc connection
# =========================
CONNECTION_STRING = (
    f"DRIVER={{{DRIVER}}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    "TrustServerCertificate=yes;"
)


def get_connection():
    return pyodbc.connect(CONNECTION_STRING)


def init_db():
    """
    Tạo bảng trong SQL Server dựa theo các model SQLAlchemy.
    Import models ở trong hàm để tránh lỗi circular import.
    """
    from src.db import models

    Base.metadata.create_all(bind=engine)