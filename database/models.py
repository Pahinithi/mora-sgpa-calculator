from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    registration_number = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)
    batch = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with SGPA records
    sgpa_records = relationship("SGPA", back_populates="user")

class SGPA(Base):
    __tablename__ = 'sgpa_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    semester = Column(String, nullable=False)
    module_code = Column(String, nullable=False)
    module_title = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    credits = Column(Float, nullable=False)
    is_gpa = Column(Boolean, default=True)
    semester_sgpa = Column(Float, nullable=True)
    semester_credits = Column(Float, nullable=True)
    final_sgpa = Column(Float, nullable=True)
    academic_standing = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with User
    user = relationship("User", back_populates="sgpa_records")

# Create database engine
engine = create_engine('sqlite:///database/sgpa.db')

# Create all tables
def init_db():
    Base.metadata.create_all(engine) 