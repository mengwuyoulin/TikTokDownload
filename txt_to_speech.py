# @File    : txt_to_speech
# @Description:
# @Author  : yangbh
# @Department:研发-测试
# @Time    : 2022/2/18 9:11
import os

from aip import AipSpeech

class BaiduAPi:
    def __init__(self,dir:str=None):
        APP_ID = '19252021'
        API_KEY = 'HYzgPp9tilWzSWa9zkPoW6Ui'
        SECRET_KEY = 'xaoM9A5acYq5ZzNtv1lIgbzUf1V9hdaL'
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
        self.dir = dir
        self.per = 3  # 发音人选择 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为 0 普通女声
        self.spd = 7  # 速度
        self.vol = 7  # 音量
        self.reset = False

    # 按指定字节数分割字符串
    def byte_split(self, seq):
        list = []
        while seq:
            if len(seq) >= 1024:
                list.append(seq[:1024])
                seq = seq[1024:]
            else:
                list.append(seq)
                seq = []
        return list

    def voice_type_dict(self,per):
        if per==1:
            per_type='男声'
        elif per==3:
            per_type='度逍遥'
        elif per==4:
            per_type='度丫丫'
        else:
            per_type = '女声'
        return per_type

    def reset_deal(self,vedio_name):
        file_path = os.path.join(self.dir, '%s_%s.mp3' % (vedio_name, self.voice_type_dict(self.per)))
        if os.path.exists(file_path):
            if self.reset:
                os.remove(file_path)
        return file_path

    def vedio_write(self, data_arr, vedio_name):
        '''
             @desc 写入音频
             @param data_arr list 文件数组
             @param vedio_name string 音频文件名
             @return 音频文件名
            '''
        file_path = self.reset_deal(vedio_name)
        for i in data_arr:
            # 请求百度接口，获取语音二进制
            result = self.client.synthesis(i, 'zh', 1, {
                'per': self.per,  # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为 0 普通女声
                'spd': self.spd,  # 速度
                'vol': self.vol  # 音量
            })

            # 判断是否翻译成功-成功则写入,失败则打印错误信息
            if not isinstance(result, dict):
                with open(file_path, 'ab') as f:
                    f.write(result)
            else:
                print(result)
        else:
            pass
        return file_path

    def deal_file(self,file_path):
        # 读取文本文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            data = f.read()

        # 按字符串拆分成数组
        data_arr = self.byte_split(data)
        # 写入音频，返回音频文件名
        vedio = self.vedio_write(data_arr, os.path.splitext(file_path)[0])
        print(vedio)

    def batch_dealfile(self,targetType='.txt'):
        for root, dirs, files in os.walk(self.dir):
            # root 所指的是当前正在遍历的这个文件夹的本身的地址
            # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
            # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
            for i in range(len(files)):
                file = files[i]
                bool = file.endswith(targetType)  # 判断是否目标文件文件
                if bool:
                    file_path=os.path.join(self.dir, file)
                    self.deal_file(file_path)
                else:
                    pass

if __name__ == '__main__':
    BaiduAPi('F:\\project\\TikTokDownload\\CaptionFile').batch_dealfile()
