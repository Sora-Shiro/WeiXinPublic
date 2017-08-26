# -*- coding: utf-8 -*-
# filename: player.py


class Player:
    def __init__(self):
        # 使能 #不知道有啥用 但感觉有用
        self.boolEnable = True
        # 得票数
        self.intVotes = 0
        # 名字
        self.strName = ''
        # 机构 organization
        self.strOrg = ''
        # 性别
        self.strSex = ''
        # 年龄
        self.strAge = ''
        # 以下可以继续增加属性


def default_players():
    listResult = []

    a = Player()
    a.boolEnable = True
    a.intVotes = 0
    a.strName = 'Leo'
    a.strOrg = 'Nari'
    a.strSex = 'Male'
    a.strAge = '30'
    listResult.append(a)

    b = Player()
    b.boolEnable = True
    b.intVotes = 0
    b.strName = 'Sora'
    b.strOrg = 'SoraShiroGame'
    b.strSex = 'Male'
    b.strAge = '20'
    listResult.append(b)

    c = Player()
    c.boolEnable = True
    c.intVotes = 0
    c.strName = u'糊糊'
    c.strOrg = 'Huhu'
    c.strSex = 'Male'
    c.strAge = '20'
    listResult.append(c)

    d = Player()
    d.boolEnable = True
    d.intVotes = 0
    d.strName = 'ForgetAll'
    d.strOrg = 'FA'
    d.strSex = 'Male'
    d.strAge = '20'
    listResult.append(d)

    e = Player()
    e.boolEnable = True
    e.intVotes = 0
    e.strName = 'Alice White'
    e.strOrg = 'AW'
    e.strSex = 'Female'
    e.strAge = '20'
    listResult.append(e)

    return listResult
