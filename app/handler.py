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

players = default_players()

order_nums = [str(x) for x in range(1, len(players) + 1)]

order_to_player_map = dict(zip(order_nums, players))

fans_number_set = set()

admins = ["tomatoes11", "farseerleo",
          "o_hn0s0hhaGPwHfZ9mWo8RtnWA2A",
          "o_hn0szZLZ3nhY7m-9b9mSaqWRE0"]
admin_number_set = set(admins)



class Handle(object):
    def POST(self):
        global players, fans_number_set, order_to_player_map, admin_number_set
        try:
            read_votes_in_txt()
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                show_str = u""
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if (recMsg.Content == 'Leo'):
                    show_str = u"Leo 超帅"
                '''
                # revote enable 指令可以让发送者成为管理员
                if recMsg.Content == "revote enable":
                    admin_number_set.add(toUser)
                    show_str = u"Revote Enable"
                # revote disable 指令可以让发送者的管理员身份失效
                elif recMsg.Content == "revote disable":
                    if toUser in admin_number_set:
                        admin_number_set.remove(toUser)
                        show_str = u"Rovote Disable"
                '''
                # 检测是否为管理员
                if toUser in admin_number_set:
                    # 修改选手名字：alter [order_num] [name]
                    if recMsg.Content.startswith("alter"):
                        show_str = u"alter\n"
                        process_str = recMsg.Content.split()
                        # 获取要更改的 player ，将其对应的 name 改变
                        order_num = process_str[1]
                        name = process_str[2]
                        player = order_to_player_map[order_num]
                        # 更新 数据
                        player.name = name
                    # 增加选手：add [order_num] [name]
                    elif recMsg.Content.startswith("add"):
                        show_str = u"add\n"
                        process_str = recMsg.Content.split()
                        # 获取要添加的 player 和对应的 order_num
                        order_num = process_str[1]
                        name = process_str[2]
                        # 更新 数据
                        if order_num not in order_nums:
                            print "1"
                            order_nums.append(order_num)
                            print "2"
                            new_player = Player()
                            print "3"
                            new_player.name = name
                            print "4"
                            new_player.votes = 0
                            print "5"
                            players.append(new_player)
                            print "6"
                            new_map = {order_num: new_player}
                            print "7"
                            order_to_player_map.append(new_map)
                            print "8"
                        else:
                            show_str = u"该号数已经存在"
                    # 删除选手：del [nickname]
                    elif recMsg.Content.startswith("del"):
                        show_str = u"del\n"
                        process_str = recMsg.Content.split()
                        # 获取要删除的 nickname
                        order_num = process_str[1]
                        if order_num in order_nums:
                            order_nums.remove(order_num)
                            name = order_to_player_map[order_num]
                            players.remove(name)
                            del order_to_player_map[order_num]
                    # 修改票数：votec [nickname] [votes]
                    elif recMsg.Content.startswith("votec"):
                        show_str = u"votec\n"
                        process_str = recMsg.Content.split()
                        # 获取要修改票数的 nickname 和对应的 votes
                        order_num = process_str[1]
                        votes = int(process_str[2])
                        # 更新 数据
                        player = order_to_player_map[order_num]
                        player.votes = votes
                    # 复位票数和已投票粉丝：
                    elif recMsg.Content.startswith("reset"):
                        init_all_data()
                    # 投票检验
                    else:
                        order_num = recMsg.Content
                        if order_num in order_nums:
                            player = order_to_player_map[order_num]
                            player.votes += 1
                        else:
                            show_str = u"没有这个号数的选手哦(⊙□⊙)\n"
                else:
                    # 检测该非管理员人员是否已经投票
                    if toUser in fans_number_set:
                        show_str = u"您已经投过票，谢谢参与！(*´▽｀* )\n"
                    # 投票检验
                    else:
                        order_num = recMsg.Content
                        if order_num in order_nums:
                            fans_number_set.add(toUser)
                            player = order_to_player_map[order_num]
                            player.votes += 1
                        else:
                            show_str = u"没有这个号数的选手哦(⊙□⊙)\n"
                # 展示结果
                for order_num in order_nums:
                    player = order_to_player_map[order_num]
                    show_str += u"%s号，%s得票数为：%d" % (order_num, player.name, player.votes)
                    if order_nums[-1] != order_num:
                        show_str += "\n"
                # 格式化最终字符串
                content = show_str.encode('utf-8')
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment


def init_all_data(o=None, p=None, ntp_map=None):

    global order_nums, players, order_to_player_map, fans_number_set

    if p is None:
        p = default_players()
    if o is None:
        o = [str(y) for y in range(1, len(players) + 1)]
    if ntp_map is None:
        ntp_map = dict(zip(order_nums, players))

    players = p
    order_nums = o
    order_to_player_map = ntp_map
    fans_number_set = set()


def save_votes():
    save_votes_in_txt()
    return ""


def save_votes_in_txt():
    return ""


def read_votes_in_txt():
    import codecs
    with codecs.open('/root/PycharmProjects/GitWeiXinPublic/votes.txt', 'r', 'utf-8') as f:
        for line in f.readlines():
            # 数据格式：[nickname] [realname] [votes]
            process_str = line.split()
            nick = process_str[0]
            real = process_str[1]
            votes = process_str[2]
            print nick
            print real
            print votes
    return ""
