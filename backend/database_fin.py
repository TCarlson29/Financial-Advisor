from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

database_url = 'sqlite:///financial_advisor.db'

engine = create_engine(database_url)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable = False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_user = User(username='Tanner', email='carlsont3@carleton.edu', password='password')
session.add(new_user)
session.commit()

all_users = session.query(User).all()
print("All users: ", all_users)

user = session.query(User).filter_by(username='Tanner').first()
print("User: ", user.username, user.email)

session.close()