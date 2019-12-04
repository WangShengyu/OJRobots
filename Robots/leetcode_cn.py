from requests_html import HTMLSession
from Struct.user_info import UserRobotInfo
import json
def get_user_robot_info(user_oj_account):
    session = HTMLSession()
    d = {"operationName":"userPublicProfile","variables":{"userSlug":""},"query":"query userPublicProfile($userSlug: String!) {\n  userProfilePublicProfile(userSlug: $userSlug) {\n    profile {\n      realName\n    }\n    submissionProgress {\n      totalSubmissions\n      waSubmissions\n      acSubmissions\n      reSubmissions\n      otherSubmissions\n      acTotal\n      questionTotal\n      __typename\n    }\n    __typename\n  }\n}\n"}
    d["variables"]["userSlug"] = user_oj_account
    r = session.post("https://leetcode-cn.com/graphql/", json=d)
    val = json.loads(r.text)
    try:
        sub = val["data"]["userProfilePublicProfile"]["submissionProgress"]
        prof = val["data"]["userProfilePublicProfile"]["profile"]

        user_robot_info = UserRobotInfo()
        user_robot_info.nick_name = prof["realName"]
        user_robot_info.ac_total = sub["acTotal"]
    except:
        print(user_oj_account)
        print(val)
        return None

    return user_robot_info

if __name__ == "__main__":
    u = get_user_robot_info("wangshengyu")
    print(u.nick_name, u.ac_total)
