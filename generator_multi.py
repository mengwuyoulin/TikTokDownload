# @File    : generator_multi
# @Description:
# @Author  : yangbh
# @Department:研发-测试
# @Time    : 2022/2/17 13:36

# 主模块执行
import argparse
import sys

from TikTokMulti import TikTok

if __name__ == "__main__":
    # 获取命令行函数
    def get_args(user,dir,music,count,mode,digg_count):
        # 新建TK实例
        TK = TikTok()
        # 命令行传参
        TK.setting(user,music,count,dir,mode,digg_count)
        input('[  完成  ]:已完成批量下载，输入任意键后退出:')
        sys.exit(0)

    try:
        parser = argparse.ArgumentParser(description='TikTokMulti V1.2.5 使用帮助')
        parser.add_argument('--user', '-u', type=str, help='为用户主页链接，非必要参数', required=False)
        parser.add_argument('--dir','-d', type=str,help='视频保存目录，非必要参数， 默认./Download', default='./Download/')
        #parser.add_argument('--single', '-s', type=str, help='单条视频链接，非必要参数，与--user参数冲突')
        parser.add_argument('--music', '-m', type=str, help='视频音乐下载，非必要参数， 默认no可选yes', default='no')
        parser.add_argument('--count', '-c', type=int, help='单页下载的数量，默认参数 35 无须修改', default=35)
        parser.add_argument('--mode', '-M', type=str, help='下载模式选择，默认post:发布的视频 可选like:点赞视频(需要开放权限)', default='post')
        parser.add_argument('--digg_count', '-D', type=int, help='允许最低点赞数，默认50000', default=50000)
        args = parser.parse_args()
        # 获取命令行
        get_args(args.user, args.dir, args.music, args.count, args.mode,args.digg_count)
    except Exception as e:
        # print(e)
        print('[  提示  ]:未输入命令，自动退出!')
        sys.exit(0)