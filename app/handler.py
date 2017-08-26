# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import codecs

import reply
import receive

import sys
sys.path.append('/root/PycharmProjects/GitWeiXinPublic/WeiXinPublic')
from secret import nj_token
from app.player import default_players, Player

# reload(sys)
# sys.setdefaultencoding('utf8')

g_listPlayers = default_players()

g_listOrderNums = [str(x) for x in range(1, len(g_listPlayers) + 1)]

g_dictOrderToPlayer = dict(zip(g_listOrderNums, g_listPlayers))

g_stFansNumber = set()

g_listAdmins = ["tomatoes11", "farseerleo",
          "o_hn0s0hhaGPwHfZ9mWo8RtnWA2A",
          "o_hn0szZLZ3nhY7m-9b9mSaqWRE0"]
g_stAdminNumber = set(g_listAdmins)


class Handle(object):
    def POST(self):
        global g_listPlayers, g_stFansNumber, g_dictOrderToPlayer, g_stAdminNumber
        try:
            read_data_in_txt()
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                strShow = u""
                strToUser = recMsg.FromUserName
                strFromUser = recMsg.ToUserName
                if (recMsg.Content == 'Leo'):
                    strShow = u"Leo 超帅"
                '''
                # revote boolEnable 指令可以让发送者成为管理员
                if recMsg.Content == "revote boolEnable":
                    admin_number_set.add(strToUser)
                    strShow = u"Revote Enable"
                # revote disable 指令可以让发送者的管理员身份失效
                elif recMsg.Content == "revote disable":
                    if strToUser in admin_number_set:
                        admin_number_set.remove(strToUser)
                        strShow = u"Rovote Disable"
                '''
                # 检测是否为管理员
                if strToUser in g_stAdminNumber:
                    # 修改选手名字：alter [strOrderNum] [strName]
                    if recMsg.Content.startswith("alter"):
                        strShow = u"alter\n"
                        listProcess = recMsg.Content.split()
                        # 获取要更改的 player ，将其对应的 strName 改变
                        strOrderNum = listProcess[1]
                        strName = listProcess[2]
                        player = g_dictOrderToPlayer[strOrderNum]
                        # 更新 数据
                        player.strName = strName
                        save_data()
                    # 增加选手：add [strOrderNum] [strName]
                    elif recMsg.Content.startswith("add"):
                        strShow = u"add\n"
                        listProcess = recMsg.Content.split()
                        # 获取要添加的 player 和对应的 strOrderNum
                        strOrderNum = listProcess[1]
                        strName = listProcess[2]
                        # 更新 数据
                        if strOrderNum not in g_listOrderNums:
                            g_listOrderNums.append(strOrderNum)
                            newPlayer = Player()
                            newPlayer.strName = strName
                            newPlayer.intVotes = 0
                            g_listPlayers.append(newPlayer)
                            g_dictOrderToPlayer[strOrderNum] = newPlayer
                            save_data()
                        else:
                            strShow = u"该号数已经存在"
                    # 删除选手：del [strOrderNum]
                    elif recMsg.Content.startswith("del"):
                        strShow = u"del\n"
                        listProcess = recMsg.Content.split()
                        # 获取要删除的 nickname
                        strOrderNum = listProcess[1]
                        if strOrderNum in g_listOrderNums:
                            g_listOrderNums.remove(strOrderNum)
                            strName = g_dictOrderToPlayer[strOrderNum]
                            g_listPlayers.remove(strName)
                            del g_dictOrderToPlayer[strOrderNum]
                            save_data()
                    # 修改票数：votec [order_name] [intVotes]
                    elif recMsg.Content.startswith("votec"):
                        strShow = u"votec\n"
                        listProcess = recMsg.Content.split()
                        # 获取要修改票数的 nickname 和对应的 intVotes
                        strOrderNum = listProcess[1]
                        intVotes = int(listProcess[2])
                        # 更新 数据
                        player = g_dictOrderToPlayer[strOrderNum]
                        player.intVotes = intVotes
                        save_data()
                    # 复位票数和已投票粉丝：
                    elif recMsg.Content.startswith("reset"):
                        init_all_data()
                        save_data()
                    # 投票检验
                    else:
                        strOrderNum = recMsg.Content
                        if strOrderNum in g_listOrderNums:
                            player = g_dictOrderToPlayer[strOrderNum]
                            player.intVotes += 1
                            strShow = u"已经成功投给%s号选手%s！" % (strOrderNum, player.strName)
                            save_data()
                        else:
                            strShow = u"没有这个号数的选手哦(⊙□⊙)\n"
                else:
                    # 检测该非管理员人员是否已经投票
                    if strToUser in g_stFansNumber:
                        strShow = u"您已经投过票，谢谢参与！(*´▽｀* )\n"
                    # 投票检验
                    else:
                        strOrderNum = recMsg.Content
                        if strOrderNum in g_listOrderNums:
                            g_stFansNumber.add(strToUser)
                            player = g_dictOrderToPlayer[strOrderNum]
                            player.intVotes += 1
                            strShow = u"已经成功投给%s号选手%s！" % (strOrderNum, player.strName)
                            save_data()
                        else:
                            strShow = u"没有这个号数的选手哦(⊙□⊙)\n"
                # 展示结果
                for strOrderNum in g_listOrderNums:
                    player = g_dictOrderToPlayer[strOrderNum]
                    strShow += u"%s号，%s得票数为：%d" % (strOrderNum, player.strName, player.intVotes)
                    if g_listOrderNums[-1] != strOrderNum:
                        strShow += "\n"
                # 格式化最终字符串
                strContent = strShow.encode('utf-8')
                replyMsg = reply.TextMsg(strToUser, strFromUser, strContent)
                #save_data()
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment


def init_all_data(strOrderNum=None, players=None, dictOrderToPlayer=None):

    global g_listOrderNums, g_listPlayers, g_dictOrderToPlayer, g_stFansNumber

    if players is None:
        players = default_players()
    if strOrderNum is None:
        strOrderNum = [str(y) for y in range(1, len(g_listPlayers) + 1)]
    if dictOrderToPlayer is None:
        dictOrderToPlayer = dict(zip(g_listOrderNums, g_listPlayers))

    g_listPlayers = players
    g_listOrderNums = strOrderNum
    g_dictOrderToPlayer = dictOrderToPlayer
    g_stFansNumber = set()


def save_data():
    save_data_in_txt()
    return ""


def save_data_in_txt():
    with codecs.open('/root/PycharmProjects/GitWeiXinPublic/intVotes.txt', 'w', 'utf-8') as f:
        line_str = ""
        for strOrderNum in g_listOrderNums:
            player = g_dictOrderToPlayer[strOrderNum]
            line_str += strOrderNum + ":" + player.strName + ":" + str(player.intVotes) + "\n"
        f.write(line_str)
    return "save_ok"


def read_data_in_txt():
    with codecs.open('/root/PycharmProjects/GitWeiXinPublic/intVotes.txt', 'r', 'utf-8') as f:
        global g_listPlayers, g_listOrderNums, g_dictOrderToPlayer
        g_listPlayers = []
        g_listOrderNums = []
        for line in f.readlines():
            # 数据格式：[strOrderNum] [strName] [intVotes]
            strProcess = line.split(":")
            strOrderNum = strProcess[0]
            strName = strProcess[1]
            intVotes = int(strProcess[2])
            newPlayer = Player()
            newPlayer.strName = strName
            newPlayer.intVotes = intVotes
            g_listPlayers.append(newPlayer)
            g_listOrderNums.append(strOrderNum)
        g_dictOrderToPlayer = dict(zip(g_listOrderNums, g_listPlayers))
    return "read_ok"
