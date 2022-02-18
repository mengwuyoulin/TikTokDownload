# @File    : txt_to_speech
# @Description:
# @Author  : yangbh
# @Department:研发-测试
# @Time    : 2022/2/18 9:11
import os

import pyttsx3
from aip import AipSpeech
from gtts import gTTS
class Txt_To_Speech:
    def pyttsx3_to_voice(self, txt):
        pp = pyttsx3.init(driverName="sapi5")
        voices = pp.getProperty('voices')
        # 0：汉语女声；1：英语男声；2：英语女声；3：日语女声；4：韩语女声；5：英语女声；6：粤语女声；7：台语女声
        pp.setProperty('voice', voices[0].id)
        # pp.setProperty('voice', "com.apple.speech.synthesis.voice.mei-jia")
        vol = pp.getProperty('volume')
        pp.setProperty('vol', vol + 0.5)
        print('准备开始语音播报...')
        pp.say(txt)
        pp.runAndWait()
        pp.stop()
        pp.save_to_file(txt, 'eee.mp3')

    def aaa(self):
        msg = '''今天我，寒夜里看雪飘过
        ​
        怀着冷却了的心窝漂远方
        ​
        风雨里追赶，雾里分不清影踪
        ​
        天空海阔你与我
        ​
        可会变（谁没在变）
        ​
        多少次，迎着冷眼与嘲笑
        ​
        从没有放弃过心中的理想
        ​
        一刹那恍惚， 若有所失的感觉
        ​
        不知不觉已变淡
        ​
        心里爱（谁明白我）
        ​
        原谅我这一生不羁放纵爱自由
        ​
        也会怕有一天会跌倒
        ​
        背弃了理想 ，谁人都可以
        ​
        哪会怕有一天只你共我
        '''
        # 模块初始化
        engine = pyttsx3.init()
        volume = engine.getProperty('volume')
        # 标准的粤语发音
        # voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")
        # 普通话发音
        # voices = engine.setProperty('voice', "com.apple.speech.synthesis.voice.ting-ting.premium")
        # 台湾甜美女生普通话发音
        # voices = engine.setProperty(
        #     'voice', "com.apple.speech.synthesis.voice.mei-jia")
        print('准备开始语音播报...')
        # 输入语音播报词语
        engine.setProperty('volume', 0.7)
        engine.say(msg)
        engine.runAndWait()
        engine.stop()

    def bbb(self,msg):
        # 语音播报模块
        # 模块初始化
        engine = pyttsx3.init()
        print('准备开始语音播报...')
        # 设置发音速率，默认值为200
        rate = engine.getProperty('rate')
        engine.setProperty('rate', rate - 50)
        # 设置发音大小，范围为0.0-1.0
        volume = engine.getProperty('volume')
        engine.setProperty('volume', 0.6)
        # 设置默认的声音：voices[0].id代表男生，voices[1].id代表女生
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        # 添加朗读文本
        # engine.say('Not everyone can become a great artist.')
        engine.say(msg)
        # 等待语音播报完毕
        engine.runAndWait()

    def ccc(self,msg):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            engine.setProperty('voice', voice.id)
            engine.say(msg)
        engine.runAndWait()

    def ddd(self):
        eng = pyttsx3.init()
        eng.save_to_file('好好学习天天向上，死亡如风，常伴吾身，面对疾风吧', 'test.mp3')
        eng.runAndWait()

    def eee(self):
        # 改变音色
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            engine.setProperty('voice', voice.id)
            engine.say('The quick brown fox jumped over the lazy dog.')
        engine.runAndWait()

    def ggg(self,text):
        tts = gTTS(text=text, lang='zh-tw')
        tts.save("ggg.mp3")

    def hhh(self,txt):
        APP_ID = '19252021'
        API_KEY = 'HYzgPp9tilWzSWa9zkPoW6Ui'
        SECRET_KEY = 'xaoM9A5acYq5ZzNtv1lIgbzUf1V9hdaL'
        client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)  # 这三个参数需要注册百度AI云平台进行获取
        # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为 0 普通女声
        result = client.synthesis(txt, 'zh', 1, {
            'spd': 7, 'vol': 5, 'per': 3
        })  # 需要转化的文字在括号内第一个属性内填写
        # vol为音量，per为声音种类

        # 识别正确返回语音二进制 错误则返回dict 参照下面错误码，生成音频
        if not isinstance(result, dict):
            with open('ex17WordToAudio_DataOut.mp3', 'wb') as f:
                f.write(result)


class BaiduAPi:
    def __init__(self):
        APP_ID = '19252021'
        API_KEY = 'HYzgPp9tilWzSWa9zkPoW6Ui'
        SECRET_KEY = 'xaoM9A5acYq5ZzNtv1lIgbzUf1V9hdaL'
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

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

    def vedio_write(self, data_arr, vedio_name):
        '''
             @desc 写入音频
             @param data_arr list 文件数组
             @param vedio_name string 音频文件名
             @return 音频文件名
            '''
        name = '.\\CaptionFile\\redio\\'+vedio_name + '.mp3'
        if os.path.exists(name):
            os.remove(name)
        for i in data_arr:
            # 请求百度接口，获取语音二进制
            result = self.client.synthesis(i, 'zh', 1, {
                'per': 3,  # 发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为 0 普通女声
                'spd': 7,  # 速度
                'vol': 7  # 音量
            })

            # 判断是否翻译成功-成功则写入,失败则打印错误信息
            if not isinstance(result, dict):
                with open(name, 'ab') as f:
                    f.write(result)
            else:
                print(result)
        return name

    def deal_file(self):
        # 文本文件
        file_name = r'CaptionFile/content.txt'
        # 音频文件名
        vedio_name = file_name.split('/')[-1].split('.')[0]

        # 读取文本文件内容
        with open(file_name, 'r', encoding='utf-8') as f:
            data = f.read()

        # 按字符串拆分成数组
        data_arr = self.byte_split(data)

        # 写入音频，返回音频文件名
        vedio = self.vedio_write(data_arr, vedio_name)
        print(vedio)


if __name__ == '__main__':
    BaiduAPi().deal_file()
#     msg = """你相信吗？
# 钱是有灵性的，它会主动为自己寻找更合适的主人。
# 这个视频要保存下来，偷偷的去看。接下来这七条灵性法则可以让你越来越有钱
# 尤其是第四条和第七条，哪怕你只做到其中的一条，你的财富也会不请自来。
# 您先点赞收藏我接着讲。
# 第一、让别人赚到钱，你才有可能赚到更多的钱。
# 既以为人己 愈有，既以与人己愈多。合作的时候先考虑对方，人生一世，小舍小得，大舍大得，不舍 不 得。
# 第二、不要占别人的便宜，
# 不该拿的拿了，不该得的得了，早晚都要加倍的还回去，这是因果定律。
# 第三、要把每一个人都当作自己的财神，
# 即便你付钱给对方，你一定要记得对方是你的财神，你付出了钱，换来了他的产品和服务，别忘了对他说声谢谢，做到这点的 评论区来告诉我。
# 第四、像亿万富翁一样说话，察觉自己内心的念头。要努力消除那些穷人的念头，比如要很辛苦才能赚到钱，好东西总是不够的，我总是没钱，我太难了等等等等。
# 第五、拒绝囤积。
# 看到打折就购物，原计划买一个，但是又担心不够，就多买几个，原本点两个菜就够，吃片药再多加几个。这体现的并不是富有，而是内心的匮乏和担忧。记住，少则得，多则惑。
# 第六、消除别人有，我也要有的自卑。
# 别人有一个苹果，我也要有，别人有一个L V，我也要有，不能少，别人去环球旅行，我也要去国外采风。记住，只有自卑才需要外在的东西去体现它的价值。
# 第七、相信自己值得拥有美好的事物。
# 试着去做一些你不曾做过的美好的事情，比如说一顿美味的野餐，一场偶像的演唱会，一次极限运动的体验，告诉自己一切美好正在发生。
# 记得以上这几条法则，会有意想不到的好事发生。"""
#     Txt_To_Speech().hhh(msg)
# Txt_To_Speech().fff()
# Txt_To_Speech().pyttsx3_to_voice(
#     1,'钱是有灵性的')
