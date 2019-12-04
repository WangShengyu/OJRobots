import pymysql
import db_config
from Struct.user_info import UserInfo, ProblemHistory

insert_user_sql = "replace into users(name) values(%s)"
insert_oj_sql = "replace into ojs(name) values(%s)"
insert_user_oj_account_sql = "replace into user_oj_account(user_id, oj_id, account) values(%s, %s, %s)"
insert_problem_count_sql = "replace into problem_count(time, user_id, oj_id, problem_count) values(%s, %s, %s, %s)"

max_day_sql = "select time from problem_count order by time desc limit 1"
get_one_user_sql = "select id from users where name=%s"
get_user_sql = "select id, name from users"
get_one_oj_sql = "select id from ojs where name=%s"
get_oj_sql = "select id, name from ojs"
get_user_oj_account_sql = "select user_id, oj_id, account from user_oj_account"
get_problem_count_sql = "select time, user_id, oj_id, problem_count from problem_count order by time"
class DBHelper():
    def __init__(self, db = db_config.db):
        self.db = pymysql.connect(db_config.host, db_config.name, db_config.password)
        self.cursor = self.db.cursor()
        self.cursor.execute('use ' + db)

        self._users = {}
        self._users_remap = {}
        self._ojs = {}
        self._ojs_remap = {}
        self._init_data()

    def __del__(self):
        self.commit()

    def print(self):
        for oj_id in self._ojs:
            print("OJ: ", oj_id, self._ojs[oj_id])

        for user_id in self._users:
            user = self._users[user_id]
            print("User: ", user_id, user.name)
            for oj_id in user.oj_account:
                print("Account: ", oj_id, user.oj_account[oj_id])
            for history in user.history:
                print("History: ", history.day, history.oj_id, history.problem_count)

    def _init_data(self):
        self.cursor.execute(get_user_sql)
        rows = self.cursor.fetchall()
        for row in rows:
            user_id = row[0]
            user_name = row[1]

            self._add_user_in_cache(user_id, user_name)

        self.cursor.execute(get_oj_sql)
        rows = self.cursor.fetchall()
        for row in rows:
            oj_id = row[0]
            oj_name = row[1]
            self._add_oj_in_cache(oj_id, oj_name)

        self.cursor.execute(get_user_oj_account_sql)
        rows = self.cursor.fetchall()
        for row in rows:
            user_id = row[0]
            oj_id = row[1]
            account = row[2]
            self._users[user_id].oj_account[oj_id] = account

        self.cursor.execute(get_problem_count_sql)
        rows = self.cursor.fetchall()
        for row in rows:
            time = row[0]
            user_id = row[1]
            oj_id = row[2]
            problem_count = int(row[3])
            user_info = self._users[user_id]
            v = ProblemHistory(time, oj_id, problem_count)
            user_info.history.append(v)

    def _add_oj_in_cache(self, oj_id, oj_name):
        if oj_id in self._ojs:
            return
        self._ojs[oj_id] = oj_name
        self._ojs_remap[oj_name] = oj_id

    def _add_user_in_cache(self, user_id, user_name):
        if user_id in self._users:
            return
        self._users[user_id] = UserInfo(user_id)
        self._users[user_id].name = user_name
        self._users_remap[user_name] = user_id

    def _get_user(self, user_name):
        if user_name not in self._users_remap:
            self.cursor.execute(insert_user_sql, user_name)
            self.db.commit()
            self.cursor.execute(get_one_user_sql, user_name)
            v = self.cursor.fetchall()
            assert(len(v) == 1)
            user_id = v[0][0]
            self._add_user_in_cache(user_id, user_name)

        user_id = self._users_remap[user_name]
        return self._users[user_id]

    def _get_oj_id(self, oj_name):
        if oj_name not in self._ojs_remap:
            self.cursor.execute(insert_oj_sql, oj_name)
            self.db.commit()
            self.cursor.execute(get_one_oj_sql, oj_name)
            v = self.cursor.fetchall()
            assert(len(v) == 1)
            oj_id = v[0][0]
            self._add_oj_in_cache(oj_id, oj_name)
        return self._ojs_remap[oj_name]

    def insert_user_oj_account(self, user_name, oj_name, user_oj_account, commit = False):
        user = self._get_user(user_name)
        oj_id = self._get_oj_id(oj_name)
        user.oj_account[oj_id] = user_oj_account

        self.cursor.execute(insert_user_oj_account_sql, (user.id, oj_id, user_oj_account))
        if commit:
            self.commit()

    def insert_problem_count(self, time, user_name, oj_name, problem_count, commit = False):
        user = self._get_user(user_name)
        oj_id = self._get_oj_id(oj_name)
        user.history.append(ProblemHistory(time, oj_id, problem_count))

        self.cursor.execute(insert_problem_count_sql, (time, user.id, oj_id, problem_count))
        if commit:
            self.commit()

    def get_max_day(self):
        self.cursor.execute(max_day_sql)
        v = self.cursor.fetchall()
        if len(v) == 0:
            return -1
        else:
            return v[0][0]

    def commit(self):
        self.db.commit()

test_db_name = "leetcode_test"
test_tables = ["users", "ojs", "user_oj_account", "problem_count"]
def create_test_db():
    test_clear_db()
    return DBHelper(test_db_name)

def test_clear_db():
    clear_db(test_db_name)

def clear_db(db_name):
    db = pymysql.connect(db_config.host, db_config.name, db_config.password)
    cursor = db.cursor()
    cursor.execute('use ' + db_name)
    for t in test_tables:
        cursor.execute("delete from " + t)
    db.commit()
            
def test_max_day():
    w = create_test_db()
    assert(w.get_max_day() == -1)
    w.insert_problem_count("2019-12-03", "wqe", "leetcode-cn", 123)
    assert(w.get_max_day() == "2019-12-03")
    w.insert_problem_count("2019-12-04", "wqe", "leetcode-cn", 223)
    assert(w.get_max_day() == "2019-12-04")
    w.insert_problem_count("2018-12-04", "wqe", "leetcode-cn", 323)
    assert(w.get_max_day() == "2019-12-04")

def test_data():
    w = create_test_db()
    w.insert_user_oj_account("q001", "leetcode-cn", "hahaha")
    w.insert_problem_count("2019-8-23", "q001", "leetcode-cn", 123)
    w.insert_problem_count("2029-8-23", "q001", "leetcode-cn", 323)
    w.insert_user_oj_account("q002", "leetcode-cn", "oooo")
    w.insert_user_oj_account("q003", "leetcode-cn", "plapsd")
    w.insert_problem_count("2039-8-23", "q003", "leetcode-cn", 723)
    w.print()

def test():
    test_max_day()
    test_data()

import sys
if __name__ == "__main__":
    if sys.argv[1] == "clear":
        clear_db("leetcode")
    else:
        test()


