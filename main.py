import os
import time

import requests



def get_exam_task(token, exam_id):
    return requests.get(
        "http://sxz.api6.zykj.org/api/services/app/Task/GetExamTaskAsync?id={}".format(exam_id),
        headers={"Authorization": "Bearer {}".format(token)},
    ).json()

def get_qst_answer_view(qst_id):
    return requests.get("http://sxz.api6.zykj.org/Question/View/{}?showAnalysis=true".format(qst_id)).text

def get_exams(token):
    resp = requests.post("http://sxz.api6.zykj.org/api/services/app/Task/GetStudentTaskListAsync", headers={"Authorization": "Bearer {}".format(token),"Content-Type": "application/json; charset=UTF-8"},data='{"maxResultCount":90,"skipCount":0,"taskListType":1}')
    return resp.json()
if __name__ == "__main__":
    token = input("token: ")
    exams = get_exams(token)["result"]["items"]
    for e in exams:
        if e["isNoStem"]:
            continue
        print("抓取 {} 中...".format(e["examName"]))
        exam_id = e["examTaskId"]
        exam = get_exam_task(token, exam_id)["result"]
        if not os.path.isdir("./answer"):
            os.mkdir("./answer")
        if not os.path.isdir("./answer/{}".format(exam["examName"])):
            os.mkdir("./answer/{}".format(exam["examName"]))
        index = 1
        for group in exam["groups"]:
            for qst in group["questions"]:
                content = get_qst_answer_view(qst["id"])
                with open("./answer/{}".format(exam["examName"])+"/{}.html".format(index), "w") as f:
                    f.write(content)
                index += 1
                time.sleep(0.3)