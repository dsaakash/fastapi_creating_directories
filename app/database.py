from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace 'sqlite:///./test.db' with your database URL (e.g., 'postgresql://user:password@localhost/dbname')
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create engine for the database connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # For SQLite only
)

# SessionLocal will be used for creating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the base class for our models
Base = declarative_base()
