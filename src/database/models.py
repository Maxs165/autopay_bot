from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class UserProgram(Base):
    __tablename__ = "user_program"
    user_tguid: Mapped[int] = mapped_column(ForeignKey("user.tguid"), primary_key=True)
    program_num: Mapped[int] = mapped_column(ForeignKey("program.num"), primary_key=True)
    expire_date: Mapped[Optional[date]]
    is_sub: Mapped[Optional[bool]]
    months_left: Mapped[Optional[int]]
    program: Mapped["Program"] = relationship()


class User(Base):
    __tablename__ = "user"

    tguid: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    number: Mapped[str]
    name: Mapped[str]
    programs: Mapped[List["UserProgram"]] = relationship()


class Program(Base):
    __tablename__ = "program"

    num: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    month: Mapped[int]
    has_subscription: Mapped[bool]
