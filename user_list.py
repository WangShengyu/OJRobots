import csv
def get_user_list():
    user_path = "./Resources/user_list.csv"
    user_list = []
    with open(user_path, "r") as f:
        csv_reader = csv.reader(f, delimiter = ',')
        is_first_line = True
        for row in csv_reader:
            if is_first_line:
                is_first_line = False
                continue
            if row[1] != '':
                user_list.append(row[1])

    return user_list

if __name__ == "__main__":
    print(get_user_list())

