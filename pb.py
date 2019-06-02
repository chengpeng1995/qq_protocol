# -*- coding: utf-8 -*-

import Protobuf,re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def UnMessageSvcPbGetMsg(data):
    data = data[8:]
    PB = Protobuf.protobuf(data)
    msglist = []
    targetQQ = PB.decode('->2a->10')
    list = PB.getWireTypeValueList('22',PB.decode('->2a'))
    for item in list:
        retdata = Friend_Message(targetQQ,item)
        if retdata:
            msglist.append(retdata)
    print msglist
    return msglist

def Friend_add_request(data):
    PB = Protobuf.protobuf(data)
    try:
        targetQQ = PB.decode('->0a->78')
        return targetQQ
    except:
        pass
def Friend_Message(targetQQ,data):
    PB = Protobuf.protobuf(data)
    MsgID = PB.decode('->0a->28')
    type = PB.decode('->0a->18')
    type1 = PB.decode('->0a->20')
    if type == 166 and type1 == 11:
        messagedata = ''
        list = PB.getWireTypeValueList('12',PB.decode('->1a->0a'))
        for item in list:
            PB1 = Protobuf.protobuf(item)
            if item[:2] == '0a':#文字消息
                message = PB1.decode('->0a->0a').decode('hex')
                messagedata += '['+message+']'
            elif item[:2] == '22':#图片消息
                imgdata =  PB1.decode('->22->7a').decode('hex')
                Imageurl = u'http://183.232.95.26'+imgdata
                messagedata += '['+Imageurl+']'
            elif item[:2] == '12':#表情消息
                code = PB1.decode('->12->08')
                messagedata += '['+str(code)+']'
        value = {'MsgID':MsgID,'QQfrom':targetQQ,'message':messagedata,'MsgType':1}
        return value
    elif type == 187 and type1 == 0:
        targetQQ = Friend_add_request(data)
        value = {'MsgID':MsgID,'QQfrom':targetQQ,'MsgType':1001}
        return value
    elif type == 84 and type1 == 0:
        GroupCode = PB.decode('->0a->08')
        targetQQ = Friend_add_request(data)
        value = {'MsgID':MsgID,'QQfrom':targetQQ,'GroupCode':GroupCode,'MsgType':2001}
        return value
def UnOnlinePushPbPushGroupMsg(data):

    data = data[8:]
    PB = Protobuf.protobuf(data)
    targetQQ = PB.decode('->0a->0a->08')
    target_nickname = PB.decode('->0a->0a->4a->22')
    MsgID = PB.decode('->0a->0a->28')
    groupQQ = PB.decode('->0a->0a->4a->08')
    group_nickname = PB.decode('->0a->0a->4a->42')
    messagedata = ''
    list = PB.getWireTypeValueList('12',PB.decode('->0a->1a->0a'))
    for item in list:
        PB1 = Protobuf.protobuf(item)
        if item[:2] == '0a':
            message = PB1.decode('->0a->0a').decode('hex')
            messagedata += '['+message+']'
        elif item[:2] == '12':
            emoticonCode = PB1.decode('->12->08')
            messagedata += '['+str(emoticonCode)+']'
        elif item[:2] == '42':
            img = PB1.decode('->42->82').decode('hex')
            ImageUrl = 'http://gchat.qpic.cn'+img
            messagedata += '['+ImageUrl+']'
    dict = {'targetQQ':targetQQ,'targetnickname':target_nickname.decode('hex'),'groupQQ':groupQQ,'groupnickname':group_nickname.decode('hex'),'message':messagedata,'MsgID':MsgID}
    return dict






