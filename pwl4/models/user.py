# import bcrypt
from sqlalchemy import Column, Integer, Text, VARCHAR

from .meta import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    role = Column(Text, nullable=False, default="user")

    # def set_password(self, setted_password):
    #     password_hashed = bcrypt.hashpw(
    #         setted_password.encode("utf8"), bcrypt.gensalt()
    #     )
    #     self.password_hash = password_hashed.decode("utf8")

    # def check_password(self, setted_password):
    #     if self.password_hash is not None:
    #         expected_hash = self.password_hash.encode("utf8")
    #         return bcrypt.checkpw(setted_password.encode("utf8"), expected_hash)
    #     return False
