from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///kodibot.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Citizens(Base):
    __tablename__ = "citizens"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True)
    citizen_id = Column(String(50), unique=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100))
    address = Column(Text)
    date_of_birth = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    taxes = relationship("Taxes", back_populates="citizen")
    chat_logs = relationship("ChatLogs", back_populates="citizen")
    parcels = relationship("Parcels", back_populates="citizen")

class LinkedUsers(Base):
    __tablename__ = "linked_users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True)
    citizen_id = Column(String(50), ForeignKey("citizens.citizen_id"))
    otp_code = Column(String(6))
    otp_expires_at = Column(DateTime)
    is_linked = Column(Boolean, default=False)
    linked_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class Taxes(Base):
    __tablename__ = "taxes"
    
    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(String(50), ForeignKey("citizens.citizen_id"))
    tax_type = Column(String(100))  # foncière, professionnelle, etc.
    amount_due = Column(Float)
    amount_paid = Column(Float)
    due_date = Column(DateTime)
    status = Column(String(50))  # paid, pending, overdue
    tax_year = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    citizen = relationship("Citizens", back_populates="taxes")

class Procedures(Base):
    __tablename__ = "procedures"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    description = Column(Text)
    steps = Column(Text)  # JSON string with procedure steps
    required_documents = Column(Text)  # JSON string
    estimated_duration = Column(String(100))
    cost = Column(Float)
    department = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class Parcels(Base):
    __tablename__ = "parcels"
    
    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(String(50), ForeignKey("citizens.citizen_id"))
    parcel_number = Column(String(100))
    property_type = Column(String(100))  # terrain, maison, appartement
    address = Column(Text)
    area_sqm = Column(Float)
    estimated_value = Column(Float)
    status = Column(String(50))  # active, sold, disputed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    citizen = relationship("Citizens", back_populates="parcels")

class ChatLogs(Base):
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20))
    citizen_id = Column(String(50), ForeignKey("citizens.citizen_id"), nullable=True)
    message_text = Column(Text)
    direction = Column(String(10))  # IN or OUT
    intent = Column(String(100), nullable=True)
    confidence = Column(Float, nullable=True)
    response_accuracy = Column(Float, nullable=True)  # 0-100%
    session_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    citizen = relationship("Citizens", back_populates="chat_logs")

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 