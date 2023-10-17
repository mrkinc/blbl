import json
import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown
import requests
import toml


class blbl():
    def __init__(self):
        config = toml.load("config.toml")
        self.session = requests.Session()
        self.cookie = config["global"]["cookie"]
        self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
        self.mail = config["global"]["mail"]
        self.token = config["global"]["token"]

    def sendEmail(self,Subject, data):
        flag = True
        tar = []
        for i in data:
            if data[i]:
                tar.append(i)
                flag = False
        if flag:
            print("邮件无需发送")
            return False

        mail = self.mail  # 发送方邮箱
        passwd = self.token  # 的授权码

        msg = MIMEMultipart()
        md_content = ""
        for i in tar:
            md_content += f"# {i}\n"
            for j in data[i]:
                md_content += f"- {j[0]} 价格: {j[1]}\n"

        # md_content = """
        #    # This is a title
        #
        #    - Item1
        #    - Item2
        #    - Item3
        #    - Item4
        #    - Item5
        #    """
        # 把内容加进去
        content = markdown.markdown(md_content)
        msg.attach(MIMEText(content, 'html', 'utf-8'))

        # 设置邮件主题
        msg['Subject'] = Subject

        # 发送方信息
        msg['From'] = mail

        # 通过SSL方式发送，服务器地址和端口
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        s.login(mail , passwd)
        # 开始发送
        s.sendmail(mail , mail , msg.as_string())
        print("邮件发送成功")
        return True

    def _requests(self, method, url, decode_level=2, retry=10, timeout=15, **kwargs):
        if method in ["get", "post"]:
            for _ in range(retry + 1):
                response = getattr(self.session, method)(url, timeout=timeout, **kwargs)
                return response.json() if decode_level == 2 else response.content if decode_level == 1 else response
        return None

    def TestCookie(self):
        url = f"https://api.bilibili.com/x/space/myinfo"
        headers = {'Host': "api.bilibili.com",
                   'cookie': self.cookie}
        response = self._requests("get", url, headers=headers)
        if response and response.get("code") != -101:
            print("Cookie仍有效")
            return True
        else:
            print("Cookie已失效")
            return False

    def VipPurchase(self,allId):
        url = "https://mall.bilibili.com/mall/noah/search/category/v2"
        headers = {'Host': "mall.bilibili.com",
                   'User-Agent': self.UA
                   }
        res = {}
        for name, _id in allId.items():
            postData = {
                "keyword": "",
                "filters": "",
                "priceFlow": "",
                "priceCeil": "",
                "sortType": "totalrank",
                "sortOrder": "",
                "pageIndex": 1,
                "userId": "",
                "state": "",
                "scene": "",
                "termQueries": [{"field": "ip", "values": [_id]}],
                "rangeQueries": [],
                "extra": []
            }
            res[name] = []
            if os.path.exists("savedData.json"):
                with open('savedData.json', 'r') as f:
                    savedData = json.load(f)
                    if name not in savedData:
                        savedData[name] = []
            else:
                savedData = {}
                savedData[name] = []

            for _ in range(1,20):
                postData["pageIndex"] = _
                response = self._requests("post", url,json=postData ,headers=headers)
                data = response["data"]["list"]
                flag = True
                for i in data:
                    if (i["itemsType"] == 1 or i["itemsType"] == 2) and (i["itemsId"] not in savedData[name]):
                        flag = False
                        res[name].append([i["name"],i["price"]])
                        savedData[name].append(i["itemsId"])
                if flag and _ not in [1,2]:
                    break

            with open('savedData.json', 'w') as f:
                json.dump(savedData, f)

        self.sendEmail("会员购",res)


if __name__ == '__main__':
    tar = blbl()
    # tar.TestCookie()
    dic = {
        "lyc" : "0_3101837",
        "eva" : "0_3000035"
    }
    tar.VipPurchase(dic) # ly
