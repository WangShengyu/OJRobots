class ProblemHistory():
    def __init__(self, day, oj_id, problem_count):
        self.day = day
        self.oj_id = oj_id
        self.problem_count = problem_count

class UserInfo():
    def __init__(self, user_id):
        self.id = user_id
        self.name = ""
        self.oj_account = {}
        self.history = []

class UserRobotInfo():
    def __init__(self):
        self.nick_name = ""
        self.ac_total = 0

