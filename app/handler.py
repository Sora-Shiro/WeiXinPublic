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
                # revote enable 指令可以让发送者成为管理员
                if recMsg.Content == "revote enable":
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
                    # 修改选手名字：alter [order_num] [name]
                    if recMsg.Content.startswith("alter"):
                        strShow = u"alter\n"
                        str_process = recMsg.Content.split()
                        # 获取要更改的 player ，将其对应的 name 改变
                        order_num = str_process[1]
                        name = str_process[2]
                        player = g_dictOrderToPlayer[order_num]
                        # 更新 数据
                        player.name = name
                    # 增加选手：add [order_num] [name]
                    elif recMsg.Content.startswith("add"):
                        strShow = u"add\n"
                        str_process = recMsg.Content.split()
                        # 获取要添加的 player 和对应的 order_num
                        order_num = str_process[1]
                        name = str_process[2]
                        # 更新 数据
                        if order_num not in g_listOrderNums:
                            g_listOrderNums.append(order_num)
                            player_new = Player()
                            player_new.name = name
                            player_new.votes = 0
                            g_listPlayers.append(player_new)
                            g_dictOrderToPlayer[order_num] = player_new
                        else:
                            strShow = u"该号数已经存在"
                    # 删除选手：del [nickname]
                    elif recMsg.Content.startswith("del"):
                        strShow = u"del\n"
                        str_process = recMsg.Content.split()
                        # 获取要删除的 nickname
                        order_num = str_process[1]
                        if order_num in g_listOrderNums:
                            g_listOrderNums.remove(order_num)
                            name = g_dictOrderToPlayer[order_num]
                            g_listPlayers.remove(name)
                            del g_dictOrderToPlayer[order_num]
                    # 修改票数：votec [order_name] [votes]
                    elif recMsg.Content.startswith("votec"):
                        strShow = u"votec\n"
                        str_process = recMsg.Content.split()
                        # 获取要修改票数的 nickname 和对应的 votes
                        order_num = str_process[1]
                        votes = int(str_process[2])
                        # 更新 数据
                        player = g_dictOrderToPlayer[order_num]
                        player.votes = votes
                    # 复位票数和已投票粉丝：
                    elif recMsg.Content.startswith("reset"):
                        init_all_data()
                    # 投票检验
                    else:
                        order_num = recMsg.Content
                        if order_num in g_listOrderNums:
                            player = g_dictOrderToPlayer[order_num]
                            player.votes += 1
                            strShow = u"已经成功投给%s号选手%s！" % (order_num, player.name)
                        else:
                            strShow = u"没有这个号数的选手哦(⊙□⊙)\n"
                else:
                    # 检测该非管理员人员是否已经投票
                    if strToUser in g_stFansNumber:
                        strShow = u"您已经投过票，谢谢参与！(*´▽｀* )\n"
                    # 投票检验
                    else:
                        order_num = recMsg.Content
                        if order_num in g_listOrderNums:
                            g_stFansNumber.add(strToUser)
                            player = g_dictOrderToPlayer[order_num]
                            player.votes += 1
                            strShow = u"已经成功投给%s号选手%s！" % (order_num, player.name)
                        else:
                            strShow = u"没有这个号数的选手哦(⊙□⊙)\n"
                # 展示结果
                for order_num in g_listOrderNums:
                    player = g_dictOrderToPlayer[order_num]
                    strShow += u"%s号，%s得票数为：%d" % (order_num, player.name, player.votes)
                    if g_listOrderNums[-1] != order_num:
                        strShow += "\n"
                # 格式化最终字符串
                strContent = strShow.encode('utf-8')
                replyMsg = reply.TextMsg(strToUser, strFromUser, strContent)
                save_data()
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment


def init_all_data(o=None, p=None, ntp_map=None):

    global g_listOrderNums, g_listPlayers, g_dictOrderToPlayer, g_stFansNumber

    if p is None:
        p = default_players()
    if o is None:
        o = [str(y) for y in range(1, len(g_listPlayers) + 1)]
    if ntp_map is None:
        ntp_map = dict(zip(g_listOrderNums, g_listPlayers))

    g_listPlayers = p
    g_listOrderNums = o
    g_dictOrderToPlayer = ntp_map
    g_stFansNumber = set()


def save_data():
    save_data_in_txt()
    return ""


def save_data_in_txt():
    with codecs.open('/root/PycharmProjects/GitWeiXinPublic/votes.txt', 'w', 'utf-8') as f:
        line_str = ""
        for o in g_listOrderNums:
            player = g_dictOrderToPlayer[o]
            line_str += o + ":" + player.name + ":" + str(player.votes) + "\n"
        f.write(line_str)
    return "save_ok"


def read_data_in_txt():
    with codecs.open('/root/PycharmProjects/GitWeiXinPublic/votes.txt', 'r', 'utf-8') as f:
        global g_listPlayers, g_listOrderNums, g_dictOrderToPlayer
        g_listPlayers = []
        g_listOrderNums = []
        for line in f.readlines():
            # 数据格式：[order_num] [name] [votes]
            process_str = line.split(":")
            order_num = process_str[0]
            name = process_str[1]
            votes = int(process_str[2])
            player_new = Player()
            player_new.name = name
            player_new.votes = votes
            g_listPlayers.append(player_new)
            g_listOrderNums.append(order_num)
        g_dictOrderToPlayer = dict(zip(g_listOrderNums, g_listPlayers))
    return "read_ok"
