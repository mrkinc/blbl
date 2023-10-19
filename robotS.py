import json
import os.path
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from io import BytesIO

import markdown
import requests
import toml
from PIL import Image


class blbl():
    def __init__(self):
        config = toml.load("config.toml")
        self.session = requests.Session()
        self.cookie = config["global"]["cookie"]
        self.UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
        self.mail = config["global"]["mail"]
        self.token = config["global"]["token"]

    def getImage(self, url):
        res = requests.get(url)
        if res.status_code == 200:
            buffer = BytesIO()
            img = Image.open(BytesIO(res.content))
            img = img.convert('RGB')
            img.save(buffer, format="JPEG", quality=60)
            return buffer.getvalue()

        else:
            print("请求失败，状态码：", res.status_code)


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
                image_data = self.getImage(j[2])
                image_id = j[3]
                # 作为附件添加图片
                image_mime = MIMEBase('image', 'jpeg')
                image_mime.set_payload(image_data)
                encoders.encode_base64(image_mime)
                image_mime.add_header('Content-ID', f'<{image_id}>')
                image_mime.add_header('Content-Disposition', 'inline', filename=f"{image_id}.jpg")
                msg.attach(image_mime)
                # 在HTML正文中引用图片
                md_content += f'<img src="cid:{image_id}" alt="Image"/><br/>'

        content = markdown.markdown(md_content)

        msg.attach(MIMEText(content, 'html', 'utf-8'))
        msg['Subject'] = Subject
        msg['From'] = mail
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(mail , passwd)
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
                        res[name].append([i["name"],i["price"],i["itemsImg"],i["itemsId"]])
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
