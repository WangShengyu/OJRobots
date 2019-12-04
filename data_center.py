import time
from user_list import get_user_list
from db_helper import DBHelper
import Robots

class DataCenter():
    def __init__(self, db):
        self._db = db

    def record(self, day):
        user_list = get_user_list()
        for user_name in user_list:
            user_oj_info = user_list[user_name]
            print("user: ", user_name)
            for oj_name in user_oj_info:
                print("  oj: ", oj_name)
                user_oj_account = user_oj_info[oj_name]
                robot = Robots.get_robot(oj_name)
                if robot == None:
                    print("No robot for oj [%s]" % oj_name)
                    continue
                user_robot_info = robot.get_user_robot_info(user_oj_account)
                if user_robot_info == None:
                    print("User name [%s], no account [%s] in OJ [%s]" % (user_name, user_oj_account, oj_name))
                    continue
                self._db.insert_user_oj_account(user_name, oj_name, user_oj_account)
                self._db.insert_problem_count(day, user_name, oj_name, user_robot_info.ac_total)
        self._db.commit()


