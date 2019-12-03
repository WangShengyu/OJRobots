import pymysql
import db_config
from Struct.user_info import UserProblemHistoryInfo, ProblemHistory

insert_user_info_sql = "replace into users(id, name) values(%s, %s)"
insert_solved_problems_sql = "insert into solved_problems(time, id, problem_count) values(%s, %s, %s)"
max_day_sql = "select time from solved_problems order by time desc limit 1"
get_user_sql = "select id, name from users"
get_solved_problems_sql = "select time, id, problem_count from solved_problems order by time"
class DBHelper():
    def __init__(self, db = db_config.db):
        self.db = pymysql.connect(db_config.host, db_config.name, db_config.password)
        self.cursor = self.db.cursor()
        self.cursor.execute('use ' + db)

        self._user_info = {}
        self._init_data()

    def __del__(self):
        self.commit()

    def print(self):
        for user in self._user_info.values():
            print(user.id, user.name)
            for p in user.problem_history:
                print("p: ", p.day, p.problem_count)

    def _init_data(self):
        self.cursor.execute(get_user_sql)
        rows = self.cursor.fetchall()
        for row in rows:
            user_info = UserProblemHistoryInfo(row[0])
            user_info.name = row[1]
            self._user_info[user_info.id] = user_info

        self.cursor.execute(get_solved_problems_sql)
        rows = self.cursor.fetchall()
        for row in rows:
            user_info = self._user_info[row[1]]
            v = ProblemHistory(int(row[0]), int(row[2]))
            user_info.problem_history.append(v)

    def insert_user_info(self, user_id, user_name, commit = False):
        if user_id not in self._user_info:
            self._user_info[user_id] = UserProblemHistoryInfo(user_id)
        self._user_info[user_id].name = user_name

        self.cursor.execute(insert_user_info_sql, (user_id, user_name))
        if commit:
            self.commit()

    def insert_solved_problems(self, time, user_id, problem_count, commit = False):
        if user_id not in self._user_info:
            self._user_info[user_id] = UserProblemHistoryInfo(user_id)
        user_info = self._user_info[user_id]
        v = ProblemHistory(time, problem_count)
        user_info.problem_history.append(v)

        self.cursor.execute(insert_solved_problems_sql, (time, user_id, problem_count))
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
test_tables = ["users", "solved_problems"]
def create_test_db():
    test_clear_db()
    return DBHelper(test_db_name)

def test_clear_db():
    db = pymysql.connect(db_config.host, db_config.name, db_config.password)
    cursor = db.cursor()
    cursor.execute('use ' + test_db_name)
    for t in test_tables:
        cursor.execute("delete from " + t)
    db.commit()
            
def test_max_day():
    w = create_test_db()
    assert(w.get_max_day() == -1)
    w.insert_solved_problems("2019-12-03", "wqe", 123)
    assert(w.get_max_day() == "2019-12-03")
    w.insert_solved_problems("2019-12-04", "wqe", 223)
    assert(w.get_max_day() == "2019-12-04")
    w.insert_solved_problems("2018-12-04", "wqe", 323)
    assert(w.get_max_day() == "2019-12-04")

def test_data():
    w = create_test_db()
    w.insert_user_info("q001", "q")
    w.insert_solved_problems("2019-8-23", "q001", 123)
    w.insert_solved_problems("1223", "q001", 125)
    w.insert_user_info("q002", "w")
    w.insert_user_info("q003", "e")
    w.insert_solved_problems("qweqwe", "q003", 925)
    w.print()

def test():
    test_max_day()
    test_data()

if __name__ == "__main__":
    test()


