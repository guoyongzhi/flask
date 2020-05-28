from locust import HttpLocust, task, TaskSet
import json
import selenium


class BestTest(TaskSet):
    # Host = "http://211.149.163.145:3000"
    @task(1)
    def login(self):
        """1.登录"""
        params = {
            "username": "15999611026",
            "password": "123456"
        }
        responeText = self.client.post("/login", params=None, json=params)
        temp = str(responeText.content, 'utf-8')
        self.token = (json.loads(temp))["token"]

    @task(2)
    def CreateTask(self):
        """ 2.创建任务 """
        headers = {
            "Authorization": "Bearer " + self.token
        }
        jsonParams = {
            "title": "iTest"
        }
        responeText = self.client.post("/api/tasks", params=None, json=jsonParams, headers=headers)
        temp = str(responeText.content, 'utf-8')
        self.id = (json.loads(temp))["id"]

    @task(3)
    def GetAllTask(self):
        """3.获取所有任务"""
        headers = {
            "Authorization": "Bearer " + self.token
        }
        responeText = self.client.get("/api/tasks", headers=headers)
        # print(json.loads(responeText.content)[0]["id"])

    @task(4)
    def FinishTask(self):
        """完成任务"""
        headers = {
            "Authorization": "Bearer " + self.token
        }
        responeText = self.client.put("/api/tasks/" + str(self.id), headers=headers)
        temp = str(responeText.content, 'utf-8')
        print("111111111111111111%s" % temp)
        FinishID = json.loads(temp)['id']
        print("222222222222222")
        print("FinishID:", FinishID)
        print("完成任务接口报文：", json.loads(temp))
        print("数据类型：", type(json.loads(temp)))
        if FinishID == self.id:
            print("完成任务")
        else:
            print("任务失败")

    @task(5)
    def DelTask(self):
        """删除任务"""
        headers = {
            "Authorization": "Bearer " + self.token
        }
        responeText = self.client.delete("/api/tasks/" + str(self.id), headers=headers)
        temp = str(responeText.content, 'utf-8')
        DelID = json.loads(temp)["id"]
        print("删除的ID",DelID)
        print("创建的ID",self.id)
        if DelID == self.id:
            print("删除成功")
        else:
            print("删除失败")


# class BestTestIndexUser(HttpLocust):
#     task_set = BestTest


class WebsiteUser(HttpLocust):
    host = "http://localhost:8080"
    task_set = BestTest
    min_wait = 5000

# if __name__ == '__main__':
#     WebsiteUser()
