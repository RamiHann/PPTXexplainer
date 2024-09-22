import os
import uuid
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create a dedicated db folder if it doesn't exist
def create_db_folder(folder_path='db'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Define ORM base and engine
Base = declarative_base()
db_path = os.path.join('db', 'database.db')
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# Create a new base class using the declarative_base factory function
Session = sessionmaker(bind=engine)
session = Session()

# Define the User class
class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    uploads = relationship('Upload', back_populates='user', cascade='all, delete, delete-orphan')

    @validates('email')
    def validate_email(self, key, address):
        try:
            v = validate_email(address)
            return v["email"]
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email: {e}")

# Define the Upload class
class Upload(Base):
    __tablename__ = 'Uploads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, default=func.now())
    finish_time = Column(DateTime)
    status = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'))
    user = relationship('User', back_populates='uploads')
    error_message = Column(String)

    @property
    def upload_path(self):
        return os.path.join('uploads', self.uid)

    @validates('status')
    def validate_status(self, key, value):
        valid_statuses = ['pending', 'processing', 'done', 'failed']
        if value not in valid_statuses:
            raise ValueError(f"Invalid status: {value}. Must be one of {valid_statuses}.")
        return value

    @validates('finish_time')
    def validate_finish_time(self, key, value):
        if self.status == 'done' and value is None:
            value = datetime.utcnow()
        return value

# Create all tables in the database
def setup_database():
    create_db_folder()
    Base.metadata.create_all(engine)
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()
