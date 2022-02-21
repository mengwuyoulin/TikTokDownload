# @File    : get_tiktok_data
# @Description:
# @Author  : yangbh
# @Department:研发-测试
# @Time    : 2022/2/21 12:13
import os
import re
import requests
from bs4 import BeautifulSoup as bs

codeMap = {
            '\ue603': '0', '\ue60d': '0', '\ue616': '0',
            '\ue602': '1', '\ue60E': '1', '\ue618': '1',
            '\ue605': '2', '\ue610': '2', '\ue617': '2',
            '\ue604': '3', '\ue611': '3', '\ue61a': '3',
            '\ue606': '4', '\ue60c': '4', '\ue619': '4',
            '\ue607': '5', '\ue60f': '5', '\ue61b': '5',
            '\ue608': '6', '\ue612': '6', '\ue61f': '6',
            '\ue60a': '7', '\ue613': '7', '\ue61c': '7',
            '\ue60b': '8', '\ue614': '8', '\ue61d': '8',
            '\ue609': '9', '\ue615': '9', '\ue61e': '9'
          }

def filter_common_params(url):
    """
    删除冗余的参数
    :param url: 抖音接口
    :return: 删除冗余参数后的接口
    """
    url = re.sub('(device_id=[^&]+&?|iid=[^&]+&?|uuid=[^&]+&?|openudid=[^&]+&?|ts=[^&]+&?|_rticket=[^&]+&?|as=[^&]+&?|cp=[^&]+&?|mas=[^&]+&?|mcc_mnc=[^&]+&?|ac=[^&]+&?|channel=[^&]+&?|aid=[^&]+&?|app_name=[^&]+&?|version_code=[^&]+&?|version_name=[^&]+&?|device_platform=[^&]+&?|ssmix=[^&]+&?|device_type=[^&]+&?|device_brand=[^&]+&?|language=[^&]+&?|os_api=[^&]+&?|os_version=[^&]+&?|manifest_version_code=[^&]+&?|resolution=[^&]+&?|dpi=[^&]+&?|update_version_code=[^&]+&?|retry_type=[^&]+&?|js_sdk_version=[^&]+&?)', '', url).rstrip('&')
    print(url)
    r = requests.get(url=url)
    print(r)
    return url

def getHtml(uid):
    url = 'https://www.iesdouyin.com/share/user/{}?sec_uid=MS4wLjABAAAAWxLpO0Q437qGFpnEKBIIaU5-xOj2yAhH3MNJi-AUY04&timestamp=1582709424&utm_source=copy&utm_campaign=client_share&utm_medium=android&share_app_name=douyin'.join(
        uid)
    header = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"}
    try:
        response = requests.get(url=url,  headers=header)
        return bs(response.text, 'lxml')
    except:
        print('网址错误')
        quit()

def get_nickname(soup):
    nickname = soup.find(name='p', attrs={'class': 'nickname'}).string
    uid = soup.find(name='span', attrs={'class': 'focus-btn go-author'})['data-id']
    shortid = getInfo(soup, 'p', 'shortid')
    return nickname,uid,shortid

def getAvatar(soup, nickname):
    avatarAddr = soup.find(name='img', attrs={'class': 'avatar'})['src']
    avatar = requests.get(avatarAddr)
    if not os.path.exists('avatar'): # 判断目录是否存在，如果不存在，则创建
        os.makedirs('avatar')
    try:
        with open('.\\avatar\\'+nickname+'.jpeg', 'wb') as img:
            img.write(avatar.content)
        print('头像保存成功 avatar\\'+nickname+'.jpeg')
    except:
        print('头像保存失败')

def code2commStr(code):
    retStr = ''
    for c in code:
        if c in codeMap:
            retStr += codeMap[c]
        else:
            retStr += c
    return retStr

def getInfo(soup, tag, attr):
    element = soup.find(name=tag, attrs={'class': attr})
    return code2commStr(element.text.split())

if __name__ == '__main__':
    filter_common_params('https://v.douyin.com/Lc3mow3/')
    userId = '3853572362'
    getHtml(userId)

