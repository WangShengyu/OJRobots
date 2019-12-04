from Robots import leetcode_cn
oj_robot = {
    "leetcode-cn": leetcode_cn
}
def get_robot(oj_name):
    if oj_name in oj_robot:
        return oj_robot[oj_name]
    else:
        return None
    
