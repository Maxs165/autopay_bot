from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy.orm import relationship

from database.base import Base


# from sqlalchemy.orm import relationship
# from typing import List

user_program = Table(
    "user_program",
    Base.metadata,
    Column("user_tguid", ForeignKey("user.tguid")),
    Column("program_num", ForeignKey("program.num")),
)


class User(Base):
    __tablename__ = "user"

    tguid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    number: Mapped[str]
    name: Mapped[str]
    day: Mapped[int] = mapped_column(Integer, nullable=True)
    programs: Mapped[List["Program"]] = relationship(secondary=user_program)


class Program(Base):
    __tablename__ = "program"

    num: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    month: Mapped[int]


# class UserProgram(Base):
#     __tablename__ = "user_program"

#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     user_tguid: Mapped[int] = mapped_column(BigInteger)
#     program_num: Mapped[int] = mapped_column(Integer)
