# @File    : TikTok_userInfo
# @Description:
# @Author  : yangbh
# @Department:研发-测试
# @Time    : 2022/2/17 11:32
import gzip
import json
import time
from urllib import request

import requests

class TikTok_UserInfo:
    # 初始化
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }
        self.file_path = 'uidList.txt'

    def construct_header(self,user_id, sec_user_id, cookie, query, token, user_agent, _rticket, ts):
        """
        构造请求头，需要传入的参数如下
        :param user_id: 要爬取的用户的uid
        :param sec_user_id: 要爬取的用户的加密的id
        :param cookie: cookie
        :param query: 请求的query
        :param token: 你的token
        :param user_agent: 请求的user_agent
        :param _rticket: 时间戳（毫秒级）
        :param ts: 时间戳（秒级）
        :return: 构造好的请求头：headers
        """
        api = self.construct_api(user_id, _rticket, ts, sec_user_id)

        headers = {
            "Host": "aweme-eagle.snssdk.com",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "Accept-Encoding": "gzip",
            "X-SS-QUERIES": query,
            "X-SS-REQ-TICKET": _rticket,
            "X-Tt-Token": token,
            "sdk-version": "1",
            "User-Agent": user_agent
        }
        x_gorgon = self.get_gorgon(api, cookie, token, query)
        headers["X-Khronos"] = ts
        headers["X-Gorgon"] = x_gorgon
        print(headers)
        return headers

    def get_gorgon(self,url, cookies, token, query):
        """
        获取headers里面的X-Gorgon
        :param url: 请求的api
        :param cookies: 你的cookie
        :param token: 你的token
        :param query: 你的query
        :return: gorgon
        """
        # 发起请求获取X-Gorgon
        headers = {
            "dou-url": url,  # 填写对应的请求的api
            "dou-cookies": cookies,  # 填写你的cookies
            "dou-token": token,  # 填写你的token
            "dou-queries": query  # 填写你的请求的queries
        }
        gorgon_host = "http://8.131.59.252:8080"
        res = requests.get(gorgon_host, headers=headers)
        gorgon = ""
        if res.status_code == 200:
            print("请求成功")
            res_gorgon = json.loads(res.text)
            if res_gorgon.get("status") == 0:
                print("成功获取 X-Gorgon")
                print(res_gorgon.get("X-gorgon"))  # 你就可以用来爬数据了
                gorgon = res_gorgon.get("X-gorgon")
            else:
                print("获取 X-Gorgon 失败")
                print(res_gorgon.get("reason"))
                raise ValueError(res_gorgon.get("reason"))

        else:
            print("请求发送错误/可能是你的网络错误，也可能是我的错误，但是大概率是你那边的错误")
            raise ValueError("请求发送错误/可能是你的网络错误，也可能是我的错误，但是大概率是你那边的错误")
        return gorgon

    def construct_api(self,user_id, _rticket, ts, sec_user_id):
        """
        api 构造函数
        :param user_id: 用户的id
        :param _rticket: 时间戳
        :param ts: 时间戳
        :param sec_user_id: 用户的加密的id
        :return: api
        """
        api = "https://aweme-eagle.snssdk.com" \
              "/aweme/v1/user/?" \
              "user_id={}" \
              "&retry_type=no_retry" \
              "&iid=1846815477740845" \
              "&device_id=47012747444" \
              "&ac=wifi&channel=wandoujia_aweme1" \
              "&aid=1128&app_name=aweme" \
              "&version_code=630" \
              "&version_name=6.3.0" \
              "&device_platform=android" \
              "&ssmix=a&device_type=HUAWEI+NXT-AL10" \
              "&device_brand=HUAWEI&language=zh" \
              "&os_api=26&os_version=8.0.0" \
              "&openudid=b202a24eb8c1538a" \
              "&manifest_version_code=630" \
              "&resolution=1080*1812" \
              "&dpi=480&update_version_code=6302" \
              "&_rticket={}" \
              "&js_sdk_version=1.16.3.5" \
              "&ts={}" \
              "&sec_user_id={}" \
              "".format(user_id, _rticket, ts, sec_user_id)
        return api

    def get_user_detail_info(self,cookie, query, token, user_agent, user_id, sec_user_id):
        """
        爬取用户数据
        :param cookie: 你自己的cookie
        :param query: 你自己的query
        :param token: 你自己的token
        :param user_agent: 你自己的User-Agent
        :param user_id: 用户的uid
        :param sec_user_id: 用户的加密的uid
        :return: response
        """
        _rticket = str(time.time() * 1000).split(".")[0]
        ts = str(time.time()).split(".")[0]

        api = self.construct_api(user_id, _rticket, ts, sec_user_id)
        headers = self.construct_header(user_id, sec_user_id, cookie, query, token, user_agent, _rticket, ts)
        print(api)
        req = request.Request(api)
        for key in headers:
            req.add_header(key, headers[key])

        with request.urlopen(req) as f:
            data = f.read()
        return gzip.decompress(data).decode()

if __name__ == '__main__':
    cookie = "ttwid=1%7C7Km71EuBl3JRncu9rhWyjW-w6XPncvAwKYjUK8YdTIU%7C1644995217%7C0b967bd93a23325ff5355621d72058b1783f7901d067701a5895a60b7a9ef925; _tea_utm_cache_6383=undefined; home_can_add_dy_2_desktop=0; _tea_utm_cache_1300=undefined; ttcid=e38d9f7cc9634adba3ec7f7d075009f216; THEME_STAY_TIME=299988; IS_HIDE_THEME_CHANGE=1; MONITOR_WEB_ID=d479fc76-9ac1-4a13-8915-a42bf34bb9ef; s_v_web_id=verify_kzp9g3x1_j4o6KLfC_54Tu_46DO_Bplz_UsGKlvQyadV1; passport_csrf_token_default=3c7d93e07e00445f5a0347440f92efda; passport_csrf_token=3c7d93e07e00445f5a0347440f92efda; AB_LOGIN_GUIDE_TIMESTAMP=1644998189817; msToken=VTm6ziPnDBzwbrv4k1dFf219q-eIELBxxJ1cmlhJKYoxibZ8MXqFVSYOh5s8rTfN6Ucfg85MVlURbV7MZNGFSIU5pYTM8EHGdCf7oMAaDTQeBomCVPCHhQ==; tt_scid=zZ7A2QP1AIe6p8M6E10RrBKT0EZmAixGE0h7wp16V6T-Hpz6AKzOEbwTLo4yyAr80dc1; msToken=m978Qo7EtcCvfg-MSYOodtwWnzs96h0O5MT2JtSlFkkKvLypJDNJk_MYrWbhDQGI3TrwmKkwDPBKMTefS8w590PVENuCYtEX-VbbzF-gzaif_p-IU3oj3g==; __ac_nonce=0620dfb54004837aa5d7f; __ac_signature=_02B4Z6wo00f01ZZJ29AAAIDCo-pfC2YBAmGWbd9AAAeg8SVV6hvQebtNEsIbX7vEVg1y-guoHej7GtrdXPLGl88n.WFVMNgurVGMzvxXMITB8diz9AdLcoZ22Oq5bbS7VlueRbsRwCiOsafD6c" # 你自己的cookie
    token = "" # 你自己的token
    query = "" # 你自己的query
    user_agent = "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66" # 你自己的user-agent

    user_id = 3597224220560461
    sec_user_id = 'MS4wLjABAAAAYTfGGeeNe-lR_zQ7TodIkhAE54-T2i18CmcKqUTZyWSzVijBkX26-E7e9ESQ0P_R'

    res = TikTok_UserInfo().get_user_detail_info(cookie,query, token, user_agent, user_id, sec_user_id)
    print(res)