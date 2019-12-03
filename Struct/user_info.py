class ProblemHistory():
    def __init__(self, day = 0, problem_count = 0):
        self.day = day
        self.problem_count = problem_count

class UserProblemHistoryInfo():
    def __init__(self, user_id):
        self.id = user_id
        self.name = ""
        # type = ProblemHistory
        self.problem_history = []

class UserInfo():
    def __init__(self, user_id):
        self.id = user_id
        self.name = ""
        self.problem_count = 0

