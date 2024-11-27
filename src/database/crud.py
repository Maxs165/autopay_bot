from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import select

from database.models import User, Program, UserProgram
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
    def get_name(tguid: int):
        with db_session() as sess:
            user = sess.scalars(select(User).where(User.tguid == tguid)).first()
            return user.name


class CRUDProgram:

    @staticmethod
    def get_program(num: int):
        with db_session() as sess:
            type_program = sess.scalars(select(Program).where(Program.num == num)).first()
            return type_program

    @staticmethod
    def get_all():
        with db_session() as sess:
            type_program = sess.scalars(select(Program)).all()
            return type_program


class CRUDUserProgram:

    @staticmethod
    def add_prog(tguid: int, num: int, is_sub: bool):
        with db_session() as sess:
            user_program = UserProgram(user_tguid=tguid, program_num=num)
            if is_sub:
                user_program.is_sub = True
                expire_date = date.today() + relativedelta(months=1)
                program = CRUDProgram.get_program(num)
                user_program.months_left = program.month - 1
            else:
                user_program.is_sub = False
                user_program.months_left = 0
                program = CRUDProgram.get_program(num)
                expire_date = date.today() + relativedelta(months=program.month)
            user_program.expire_date = expire_date
            sess.add(user_program)
            sess.commit()

    @staticmethod
    def get_all():
        with db_session() as sess:
            users_program = sess.scalars(select(UserProgram)).all()
            users_program = [u for u in users_program]
            return users_program

    @staticmethod
    def check_and_minus_month(tguid: int, num: int):
        with db_session() as sess:
            user_program = sess.scalars(
                select(UserProgram).where(
                    UserProgram.user_tguid == tguid, UserProgram.program_num == num
                )
            ).first()
            if user_program is not None:
                user_program.months_left -= 1
                sess.commit()
                return True
