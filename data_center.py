import time
from user_list import get_user_list
from db_helper import DBHelper
from Robots import leetcode

class DataCenter():
    def __init__(self, db):
        self._db = db

    def record(self, day):
        user_list = get_user_list()
        for user_name in user_list:
            user_info = leetcode.get_user_info(user_name)
            if user_info == None:
                continue
            self._db.insert_user_info(user_info.id, user_info.name)
            self._db.insert_solved_problems(day, user_info.id, user_info.problem_count)
        self._db.commit()


