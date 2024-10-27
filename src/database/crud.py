from sqlalchemy import select

from database.models import User, Program
from database.base import db_session


class CRUDUser:

    @staticmethod
    def create(tguid: int, number: str, name: str):
        with db_session() as sess:
            user = User(tguid=tguid, number=number, name=name)
            sess.add(user)
            sess.commit()

    @staticmethod
    def delete(tguid: int):
        with db_session() as sess:
            user = sess.scalars(select(User).where(User.tguid == tguid)).first()
            user.delete_instanse()
            sess.commit()

    @staticmethod
    def get_all():
        with db_session() as sess:
            users = sess.scalars(select(User)).all()
            users = [u for u in users]
            return users

    @staticmethod
    def add_num(tguid: int, num: int):
        with db_session() as sess:
            user = sess.scalars(select(User).where(User.tguid == tguid)).first()
            user.num = num
            sess.commit()

    @staticmethod
    def add_day(tguid: int, day: int):
        with db_session() as sess:
            user = sess.scalars(select(User).where(User.tguid == tguid)).first()
            user.day = day
            sess.commit()

    @staticmethod
    def get_day(tguid: int):
        with db_session() as sess:
            user = sess.scalars(select(User).where(User.tguid == tguid)).first()
            return user.day

    @staticmethod
    def all_minus_day():
        with db_session() as sess:
            users = sess.scalars(select(User)).all()
            for user in users:
                if user.day > -1:
                    user.day -= 1
            sess.commit()

    @staticmethod
    def add_prog(tguid: int, num: int):
        with db_session() as sess:
            user = sess.scalars(select(User).where(User.tguid == tguid)).first()
            program = sess.scalars(select(Program).where(Program.num == num)).first()
            user.programs.append(program)
            sess.commit()


class CRUDProgram:

    @staticmethod
    def get_program(num: int):
        with db_session() as sess:
            type_program = sess.scalars(select(Program).where(Program.num == num)).first()
            return type_program


# class CRUDProgram:

#     @staticmethod
#     def get_by_title(title: str):
#         with db_session() as sess:
#             program = sess.scalars(select(Program).where(Program.title == title)).first()
#             return program


# @staticmethod
# def minus_day(tguid: int):
#     with db_session() as sess:
#         user = sess.scalars(select(User).all()
#         for u in users:
#            u.day -= 1
#            sess.commit()
