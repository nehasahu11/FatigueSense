from backend.app.database.mysql.connection import engine
from backend.app.database.mysql.models import Base

print("Creating MySQL tables...")

Base.metadata.create_all(bind=engine)

print("MySQL tables created successfully!")
