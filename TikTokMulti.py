#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Description:TikTokMulti.py
@Date       :2022/01/29 20:23:37
@Author     :JohnserfSeed
@version    :1.2.5
@License    :(C)Copyright 2019-2022, Liugroup-NLPR-CASIA
@Github     :https://github.com/johnserf-seed
@Mail       :johnserfseed@gmail.com
'''

import argparse
import configparser
import json
import os
import re
import requests
import sys
import time


class TikTok():
    # 初始化
    def __init__(self,userId:str=None):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
        }

        # 抓获所有视频
        self.Isend = False
        self.out_Print()

        # 用户主页      # 保存路径      # 单页下载数        # 下载音频      # 下载模式      # 保存用户名            # 点赞个数           # 被赞
        self.uid = '';self.save = '';self.count = '';self.musicarg = '';self.mode = '';self.nickname = '';self.like_counts = 0;self.digg_count=0
        self.userId = userId
        # 检测配置文件
        configfile = "conf.conf"
        self.cf = self.read_configfile(configfile)
        self.data_list = []

    def read_configfile(self,configfile):
        # 实例化读取配置文件
        if os.path.isfile(configfile) == True:
            # 实例化读取配置文件
            config = configparser.ConfigParser()
        else:
            print('[  提示  ]:没有检测到配置文件，生成中!\r')
            config = self.init_configfile(configfile)
        # 用utf-8防止出错
        config.read(configfile, encoding="utf-8")
        return config

    def get_config_setting(self,uid:str=None):
        print('[  提示  ]:使用配置文件进行批量下载!')
        self.init_config(self.cf,uid)
        self.judge_link()

    def init_config(self,config,uid):
        # 读取用户主页地址
        if uid:
            pass
        else:
            self.uid = config.get("url", "uid")
        # 读取保存路径
        self.save = config.get("save", "url")
        # 读取下载视频个数
        self.count = int(config.get("count", "count"))
        # 读取下载是否下载音频
        self.musicarg = config.get("music", "musicarg")
        # 读取下载模式
        self.mode = config.get("mode", "mode")
        self.digg_count = config.get("base", 'digg_count')

    def init_configfile(self,filename):
        # 生成配置文件
        try:
            config = configparser.ConfigParser()
            # 往配置文件写入内容
            config.add_section("url")
            config.set("url", "uid", "https://v.douyin.com/JcjJ5Tq/")
            config.add_section("music")
            config.set("music", "musicarg", "yes")
            config.add_section("count")
            config.set("count", "count", "35")
            config.add_section("save")
            config.set("save", "url", ".\\Download\\")
            config.add_section("mode")
            config.set("mode", "mode", "post")
            with open(filename, "a+") as f:
                config.write(f)
            print('[  提示  ]:生成成功!\r')
        except:
            input('[  提示  ]:生成失败,正在为您下载配置文件!\r')
            r = requests.get('https://gitee.com/johnserfseed/TikTokDownload/raw/main/conf.ini')
            with open(filename, "a+") as conf:
                conf.write(r.content)
            sys.exit()
        return config

    def setting(self,uid,music,count,dir,mode,digg_count):
        """
        @description  : 设置命令行参数
        @param  : uid 用户主页,music 下载音频,count 单页下载数,dir 目录,mode 模式
        @Returns  : None
        """
        if uid:
            if uid == None:
                print('[  警告  ]:--user不能为空')
                pass
            else:
                self.uid = uid;self.save = dir;self.count=count;self.musicarg=music;self.mode=mode;self.digg_count=digg_count
                print('[  提示  ]:读取命令完成!\r')
                self.judge_link()
        # 没有接收到命令
        else:
            print('[  警告  ]:未检测到命令，将使用配置文件进行批量下载!')
            self.init_config(self.cf)
            self.judge_link()

    def out_Print(self):
        print(r'''
  ████████╗██╗██╗  ██╗████████╗ ██████╗ ██╗  ██╗██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗
  ╚══██╔══╝██║██║ ██╔╝╚══██╔══╝██╔═══██╗██║ ██╔╝██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗
     ██║   ██║█████╔╝    ██║   ██║   ██║█████╔╝ ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║
     ██║   ██║██╔═██╗    ██║   ██║   ██║██╔═██╗ ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║
     ██║   ██║██║  ██╗   ██║   ╚██████╔╝██║  ██╗██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝
     ╚═╝   ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝''')

    # 匹配粘贴的url地址
    def Find(self, string):
        # findall() 查找匹配正则表达式的字符串
        url = re.findall(
            'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
        return url

    # 判断个人主页api链接
    def judge_link(self):
        # 判断长短链
        if self.uid[0:20] == 'https://v.douyin.com':
            r = requests.get(url = self.Find(self.uid)[0])
            print('[  提示  ]:为您下载多个视频!\r')
            # 获取用户sec_uid
            for one in re.finditer(r'user/([\d\D]*?)\?',str(r.url)):
                key = one.group(1)
            # key = re.findall('/user/(.*?)\?', str(r.url))[0]
            print('[  提示  ]:用户的sec_id=%s\r' % key)
        else:
            r = requests.get(url = self.Find(self.uid)[0])
            print('[  提示  ]:为您下载多个视频!\r')
            # 获取用户sec_uid
            # 因为某些情况链接中会有?previous_page=app_code_link参数，为了不影响key结果做二次过滤
            # 原user/([\d\D]*?)([?])
            try:
                for one in re.finditer(r'user\/([\d\D]*)([?])',str(r.url)):
                    key = one.group(1)
            except:
                for one in re.finditer(r'user\/([\d\D]*)',str(r.url)):
                    key = one.group(1)
            print('[  提示  ]:用户的sec_id=%s\r' % key)

        # 第一次访问页码
        max_cursor = 0

        # 构造第一次访问链接
        api_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=PDHVOQAAXMfFyj02QEpGaDwx1S&dytk=' % ( 
                self.mode, key, str(self.count), max_cursor)

        response = requests.get(url = api_post_url, headers = self.headers)
        html = json.loads(response.content.decode())
        self.nickname = html['aweme_list'][0]['author']['nickname']
        if not os.path.exists(self.save + self.mode + "\\" + self.nickname):
                os.makedirs(self.save + self.mode + "\\" + self.nickname)
        self.get_data(api_post_url, max_cursor)
        return api_post_url,max_cursor,key

    # 获取第一次api数据
    def get_data(self, api_post_url, max_cursor):
        # 尝试次数
        index = 0
        # 存储api数据
        result = []
        while result == []:
            index += 1
            print('[  提示  ]:正在进行第 %d 次尝试\r' % index)
            time.sleep(0.3)
            response = requests.get(
                url=api_post_url, headers=self.headers)
            html = json.loads(response.content.decode())
            with open('r.json', 'wb')as f:
                f.write(response.content)
            if self.Isend == False:
                # 下一页值
                print('[  用户  ]:', str(self.nickname), '\r')
                max_cursor = html['max_cursor']
                result = self.filter_high_like_data(html['aweme_list'],self.digg_count)
                print('[  提示  ]:抓获数据成功!\r')
                # 处理第一页视频信息
                self.video_info(result, max_cursor)
            else:
                max_cursor = html['max_cursor']
                self.next_data(max_cursor)
                # self.Isend = True
                print('[  提示  ]:此页无数据，为您跳过......\r')
                break
        return result,max_cursor

    # 下一页
    def next_data(self,max_cursor):
        # 获取解码后原地址
        r = requests.get(url = self.Find(self.uid)[0])

        # 获取用户sec_uid
        key = re.findall('/user/(.*?)\?', str(r.url))[0]
        if not key:
            key = r.url[28:83]

        # 构造下一次访问链接
        api_naxt_post_url = 'https://www.iesdouyin.com/web/api/v2/aweme/%s/?sec_uid=%s&count=%s&max_cursor=%s&aid=1128&_signature=RuMN1wAAJu7w0.6HdIeO2EbjDc&dytk=' % (
            self.mode, key, str(self.count), max_cursor)

        index = 0
        result = []

        while self.Isend == False:
            # 回到首页，则结束
            if max_cursor == 0:
                self.Isend = True
                return
            index += 1
            print('[  提示  ]:正在对', max_cursor, '页进行第 %d 次尝试！\r' % index)
            time.sleep(0.3)
            response = requests.get(url = api_naxt_post_url, headers = self.headers)
            html = json.loads(response.content.decode())
            if self.Isend == False:
                # 下一页值
                max_cursor = html['max_cursor']
                result = self.filter_high_like_data(html['aweme_list'],self.digg_count)
                print('[  提示  ]:%d页抓获数据成功!\r' % max_cursor)
                # 处理下一页视频信息
                self.video_info(result, max_cursor)
            else:
                self.Isend == True
                print('[  提示  ]:%d页抓获数据失败!\r' % max_cursor)
                # sys.exit()

    def filter_high_like_data(self, content: list, digg_count:int):
        result = []
        for i in content:
            if i['statistics']['digg_count'] >= eval(digg_count):
                result.append(i)
        print('[  提示  ]:%d条数据超过%d个点赞!\r' % (len(result),eval(self.digg_count)))
        return result

    # 处理视频信息
    def video_info(self, result, max_cursor):
        # 作者信息      # 无水印视频链接    # 作品id        # 作者id        # 封面大图
        author_list = [];video_list = [];aweme_id = [];nickname = [];  # dynamic_cover = []
        for v in range(self.count):
            try:
                author_list.append(str(result[v]['desc']))
                video_list.append(str(result[v]['video']['play_addr']['url_list'][0]))
                aweme_id.append(str(result[v]['aweme_id']))
                nickname.append(str(result[v]['author']['nickname']))
                # dynamic_cover.append(str(result[v]['video']['dynamic_cover']['url_list'][0]))
                item={}
                item.update({'抖音昵称':self.nickname[0]})
                item.update({'主页地址':self.uid})
                item.update({'主页地址':self.uid})
            except Exception as error:
                # print(error)
                pass
        self.videos_download(author_list, video_list, aweme_id, nickname, max_cursor)
        return self,author_list,video_list,aweme_id,nickname,max_cursor

    # 检测视频是否已经下载过
    def check_info(self, nickname):
        if nickname == []:
            return
        else:
            v_info = os.listdir((self.save + self.mode + "\\" + nickname))
        return v_info

    # 音视频下载
    def videos_download(self, author_list, video_list, aweme_id, nickname, max_cursor):
        # 创建并检测下载目录是否存在
        try:
            os.makedirs(self.save + self.mode + "\\" + nickname[0])
        except:
            pass

        v_info = self.check_info(self.nickname)

        for i in range(self.count):
            js = None
            creat_time = None
            # 点赞视频排序
            self.like_counts += 1

            # 获取单部视频接口信息
            creat_time=self.get_vedio_createTime(aweme_id,i)
            # 每次判断视频是否已经下载过
            try:
                if creat_time + author_list[i] + '.mp4' in v_info:
                    print('[  提示  ]:', author_list[i], '[文件已存在，为您跳过]', end = "") # 开始下载，显示下载文件大小
                    for i in range(20):
                        print(">",end = '', flush = True)
                        time.sleep(0.01)
                    print('\r')
                    continue
            except:
                # 防止下标越界
                pass

            # 尝试下载音频
            self.download_music(content=js, creat_time=creat_time, author_list=author_list, nickname=nickname, count=i)
            # 尝试下载视频
            try:
                self.download_vedio(video_list, creat_time, author_list, nickname, i)
            except Exception as error:
                # print(error)
                print('[  提示  ]:该页视频资源没有', self.count, '个,已为您跳过！\r')
                break
        # 获取下一页信息
        self.next_data(max_cursor)

    def get_vedio_createTime(self,aweme_id,count):
        # 获取单部视频接口信息
        try:
            jx_url = f'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={aweme_id[count]}'  # 官方接口
            js = json.loads(requests.get(
                url=jx_url, headers=self.headers).text)

            creat_time = time.strftime("%Y-%m-%d %H.%M.%S", time.localtime(js['item_list'][0]['create_time']))
            return creat_time
        except Exception as error:
            # print(error)
            pass

    def download_music(self, content, creat_time, author_list, nickname, count):
        # 尝试下载音频
        try:
            if self.musicarg == "yes":  # 保留音频
                music_url = str(content['item_list'][0]['music']['play_url']['url_list'][0])
                music_title = str(content['item_list'][0]['music']['author'])
                music = requests.get(music_url)  # 保存音频
                start = time.time()  # 下载开始时间
                size = 0  # 初始化已下载大小
                chunk_size = 1024  # 每次下载的数据大小
                content_size = int(music.headers['content-length'])  # 下载文件总大小
                if music.status_code == 200:  # 判断是否响应成功
                    print('[  音频  ]:' + creat_time + author_list[count] + '[文件 大小]:{size:.2f} MB'.format(
                        size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小

                    if self.mode == 'post':
                        m_url = self.save + self.mode + "\\" + nickname[count] + '\\' + creat_time + re.sub(
                            r'[\\/:*?"<>|\r\n]+', "_", music_title) + '_' + author_list[count] + '.mp3'
                    else:
                        m_url = self.save + self.mode + "\\" + self.nickname + '\\' + str(
                            self.like_counts) + '、' + re.sub(
                            r'[\\/:*?"<>|\r\n]+', "_", music_title) + '_' + author_list[count] + '.mp3'

                    with open(m_url, 'wb') as file:  # 显示进度条
                        for data in music.iter_content(chunk_size=chunk_size):
                            file.write(data)
                            size += len(data)
                            print('\r' + '[下载进度]:%s%.2f%%' % (
                                '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')

                        end = time.time()  # 下载结束时间
                        print('\n' + '[下载完成]:耗时: %.2f秒\n' % (
                                end - start))  # 输出下载用时时间

        except:
            print('\r[  警告  ]:下载音频出错!\r')

    def download_vedio(self, video_list, creat_time, author_list, nickname, count):
        # 尝试下载视频
        video = requests.get(video_list[count])  # 保存视频
        start = time.time()  # 下载开始时间
        size = 0  # 初始化已下载大小
        chunk_size = 1024  # 每次下载的数据大小
        content_size = int(video.headers['content-length'])  # 下载文件总大小
        try:
            if video.status_code == 200:  # 判断是否响应成功
                print('[  视频  ]:' + creat_time + author_list[count] + '[文件 大小]:{size:.2f} MB'.format(
                    size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小

                if self.mode == 'post':
                    v_url = self.save + self.mode + "\\" + nickname[count] + '\\' + creat_time + re.sub(
                        r'[\\/:*?"<>|\r\n] + ', "_", author_list[count]) + '.mp4'
                else:
                    v_url = self.save + self.mode + "\\" + self.nickname + '\\' + str(
                        self.like_counts) + '、' + re.sub(
                        r'[\\/:*?"<>|\r\n] + ', "_", author_list[count]) + '.mp4'

                with open(v_url, 'wb') as file:  # 显示进度条
                    for data in video.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        print('\r' + '[下载进度]:%s%.2f%%' % (
                            '>' * int(size * 50 / content_size), float(size / content_size * 100)), end=' ')

                    end = time.time()  # 下载结束时间
                    print('\n' + '[下载完成]:耗时: %.2f秒\n' % (
                            end - start))  # 输出下载用时时间

        except Exception as error:
            # print(error)
            print('[  警告  ]:下载视频出错!')
            print('[  警告  ]:', error, '\r')

