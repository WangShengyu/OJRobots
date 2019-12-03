from requests_html import HTMLSession
from Struct.user_info import UserInfo
import json
def get_user_info(user):
    session = HTMLSession()
    d = {"operationName":"userPublicProfile","variables":{"userSlug":""},"query":"query userPublicProfile($userSlug: String!) {\n  userProfilePublicProfile(userSlug: $userSlug) {\n    profile {\n      realName\n    }\n    submissionProgress {\n      totalSubmissions\n      waSubmissions\n      acSubmissions\n      reSubmissions\n      otherSubmissions\n      acTotal\n      questionTotal\n      __typename\n    }\n    __typename\n  }\n}\n"}
    d["variables"]["userSlug"] = user
    r = session.post("https://leetcode-cn.com/graphql/", json=d)
    val = json.loads(r.text)
    try:
        sub = val["data"]["userProfilePublicProfile"]["submissionProgress"]
        prof = val["data"]["userProfilePublicProfile"]["profile"]

        user_info = UserInfo(user)
        user_info.name = prof["realName"]
        user_info.problem_count = sub["acTotal"]
    except:
        print(user)
        print(val)
        return None

    return user_info

if __name__ == "__main__":
    get_user_info("wangshengyu")
