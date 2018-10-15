import json

import requests
import pandas as pd


def login(session, stuid, passwd):
    login_url = "http://zhjw.scu.edu.cn/j_spring_security_check"
    payload = {
        "j_username": stuid,
        "j_password": passwd,
        "j_captcha1": "error"
    }
    # print(payload)
    r = session.post(login_url, data=payload)

    if "方案名称" in r.text:
        print("login success")
        return "success", session
    else:
        print("login failed")
        return "登录失败", session
        # exit(1)


def parse(session, stuid, out_file_name):
    new = session.get("http://zhjw.scu.edu.cn/student/integratedQuery/scoreQuery/coursePropertyScores/callback")
    j = json.loads(new.text)
    # with open("ex.json", 'w', encoding="utf8") as f:
    #     f.write(json.dumps(j, ensure_ascii=False, indent=2))

    # filename = "ex.json"
    # j = json.load(open(filename, encoding='utf8'))

    dic = {}
    for class_type in j:
        # 成绩类型
        courses = []
        for course in class_type['cjList']:
            info = [
                course["courseName"],
                course["courseAttributeName"],
                course["id"]['courseNumber'],
                course["credit"],
            ]
            courses.append(info)

        cjlx = class_type['cjlx']

        dic.update({cjlx: courses})

    source = pd.DataFrame()
    for lx in dic:
        df = pd.DataFrame(dic[lx], columns=["课程名", '课程属性', '课程号', '学分'])
        source = pd.concat([source, df])

    # 重设数据类型
    # source['课程号'] = source['课程号'].astype("str")
    source['学分'] = source['学分'].astype(float)

    # 添加新行
    source.loc[len(source)] = ['修读课程总数', len(source), '修读课程总分', source['学分'].sum()]

    source.to_excel(out_file_name, index=False)

    return out_file_name


def spider(stuid, passwd):
    session = requests.Session()
    session = login(session, stuid, passwd)
    parse(session, stuid, out_file_name="test.xls")


if __name__ == "__main__":

    stuid = "2015666666666"
    passwd = "1111"
    spider(stuid, passwd)
    # session = requests.Session()

    # session = login(session, stuid, passwd)

    # parse(session, stuid)
