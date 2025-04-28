from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # 👈 Load env vars from .env

print("Loaded environment variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")


# 🔐 Load DB URL from environment variable
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
print("✅ DATABASE_URL =", SQLALCHEMY_DATABASE_URL)

# ✅ Create engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ✅ Session for dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class for models
Base = declarative_base()

