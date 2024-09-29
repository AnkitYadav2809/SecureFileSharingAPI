
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base 

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50))
    is_verified = Column(Boolean, default=False)

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(255), nullable=False)
    uploaded_by = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=False)

# Database connection setup
def get_database_session():
    engine = create_engine('postgresql://postgres:justchill@localhost/fileSharingAPI')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
