import werobot
import configparser
import re
from msghandler.texthandler import *
from utils.sqlutils import getlastperiod

config = configparser.ConfigParser()
config.read('../config/wechat.conf')

robot = werobot.WeRoBot(config['WECHAT']['token'])
robot.config['APP_ID'] = config['WECHAT']['app_id']
robot.config['APP_SECRET'] = config['WECHAT']['app_secret']

@robot.text
def texthandle(msg , session):
    if re.match('\d{6}',msg.content) and msg.content[0:2]!='20' and (session['ifperiod']==False or session.get('ifperiod')==False):
        print('进入首次查询分支')
        str=querybyqhdm(msg.content,getlastperiod())
        return str
    elif re.match('201(8|7)(0([0-9])|1([0-2]))',msg.content):
        print('someone input a period')
        period=msg.content
        session['ifperiod']=True
        session['period']=period
        return '时期已切换为'+period[0:4]+'年'+period[4:6]+'月'
    elif session['ifperiod']==True:
        print('进入时期切换分支')
        str=querybyqhdm(msg.content,session['period'])
        print(len(str))
        #session['ifperiod']=False
        if len(str)<960:
            return str
        else:
            return str[0:930]
    elif msg.content in ['/help','/帮助']:
        return help()
    elif msg.content in ['/about','/关于']:
        return 'chiwei presents'
    else:
        return singleindexquery(msg.content)

@robot.subscribe
def hello(msg):
    return '欢迎关注民政统计，请输入6位区划代码查询该地区最新季度数据，输入时期以切换相应时期数据，时期格式\
    类似“201806”，“201803”。如需帮助，输入/帮助、/help查看帮助。\n当前整体功能完成度约20%，后续内容正在开发中。\nChi'

@robot.voice

def sendimageTest():
    return
robot.config['HOST'] = '127.0.0.1'
robot.config['PORT'] = 80
robot.run()
