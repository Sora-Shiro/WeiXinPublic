# -*- coding: utf-8 -*-
# filename: player.py


class Player:
    def __init__(self):
        # 使能 #不知道有啥用 但感觉有用
        self.enable = True
        # 得票数
        self.votes = 0
        # 名字
        self.name = ''
        # 机构 organization
        self.org = ''
        # 性别
        self.sex = ''
        # 年龄
        self.age = ''
        # 以下可以继续增加属性


def default_players():
    result_list = []

    a = Player()
    a.enable = True
    a.votes = 0
    a.name = 'Leo'
    a.org = 'Nari'
    a.sex = 'Male'
    a.age = '30'
    result_list.append(a)

    b = Player()
    b.enable = True
    b.votes = 0
    b.name = 'Sora'
    b.org = 'SoraShiroGame'
    b.sex = 'Male'
    b.age = '20'
    result_list.append(b)

    c = Player()
    c.enable = True
    c.votes = 0
    c.name = u'糊糊'
    c.org = 'Huhu'
    c.sex = 'Male'
    c.age = '20'
    result_list.append(c)

    d = Player()
    d.enable = True
    d.votes = 0
    d.name = 'ForgetAll'
    d.org = 'FA'
    d.sex = 'Male'
    d.age = '20'
    result_list.append(d)

    e = Player()
    e.enable = True
    e.votes = 0
    e.name = 'Alice White'
    e.org = 'AW'
    e.sex = 'Female'
    e.age = '20'
    result_list.append(e)

    return result_list
