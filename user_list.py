import csv
import copy
def get_user_list():
    user_path = "./Resources/user_list.csv"
    user_list = {}
    with open(user_path, "r") as f:
        csv_reader = csv.reader(f, delimiter = ',')
        is_first_line = True
        oj_name = None
        for row in csv_reader:
            if is_first_line:
                oj_name = copy.deepcopy(row)
                is_first_line = False
            else:
                user_oj = {}
                for i in range(1, len(row)):
                    if row[i] == '':
                        continue
                    user_oj[oj_name[i]] = row[i]
                user_list[row[0]] = user_oj

    return user_list

if __name__ == "__main__":
    print(get_user_list())

