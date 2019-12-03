import time
from db_helper import DBHelper
from data_center import DataCenter
from Utils import utils

if __name__ == "__main__":
    db = DBHelper()
    db.cursor.execute("delete from users")
    db.cursor.execute("delete from solved_problems")
    db = DBHelper()
    dc = DataCenter(db)
    last_day = ""
    while True:
        if last_day == "":
            last_day = db.get_max_day()

        day = str(utils.today())
        if day != last_day:
            dc.record(day)
            last_day = day
        break

        time.sleep(60)


