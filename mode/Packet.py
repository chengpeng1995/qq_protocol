# -*- coding: utf-8 -*-
import os
import random, PB

import zlib

from Tools import TEA
from JceFactory import *
import config, time


def Make_sendSsoMsg(self, cmd, bin):
    """
    SsoMsg二次组包使用 qqkey 加密 (完整) || **--> Pack_sendSsoMsg_simple -> this ||
    """
    serviceCmd = Coder.str2hexstr(cmd)
    msg = ''
    msg += Coder.num2hexstr(len(serviceCmd) / 2 + 4, 4) + serviceCmd
    msg += Coder.num2hexstr(len(config.msgCookies) / 2 + 4, 4) + config.msgCookies

    data = ''
    data += Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    data += bin
    value = TEA.entea_hexstr(data, self.qqkey)
    return value


def Pack(self, bin, type):
    """
    Pack组包
    """
    req = ''
    if type == 0:
        req += Coder.trim('00 00 00 08 02 00 00 00 04')
    elif type == 1:
        req += Coder.trim('00 00 00 08 01 00 00')
        req += Coder.num2hexstr(len(self.token002c) / 2 + 4, 2) + self.token002c
    else:
        req += Coder.trim('00 00 00 09 01')
        req += Coder.num2hexstr(self.seq, 4)
    req += Coder.trim('00 00 00')
    req += Coder.num2hexstr(len(self.qqHexstr) / 2 + 4, 2)
    req += self.qqHexstr

    req += bin
    data = Coder.num2hexstr(len(req) / 2 + 4, 4) + req
    return data


def Pack_sendSsoMsg_simple(bin, mapkey, iversion, RequestId, ServerName, FuncName):
    """
    SsoMsg一次组包
    """
    msg = ''
    msg += out.WriteJceStruct(Coder.hexstr2str(bin), 0)  ##十六进制转换字符串

    map = config.JceMap()
    map.key_type = config.TYPE_STRING1
    map.value_type = config.TYPE_SIMPLE_LIST
    map.key = mapkey
    map.value = Coder.hexstr2str(msg)  ##十六进制转换字符串
    value = out.WriteMap(map, 0)

    data = ''
    data += Write_RequestPacket(iversion, RequestId, ServerName, FuncName, Coder.hexstr2str(value))
    reee = Coder.num2hexstr(len(data) / 2 + 4, 4) + data
    return reee


def Pack_friendlist_getFriendGroupList(self, startIndex, getfriendCount):
    """
    获取群成员（完整）|| Write_FL -> Pack_sendSsoMsg_simple -> Make_sendSsoMsg -> Pack ||
    """
    msg = Write_FL(3, 1, self.qqnum, startIndex, getfriendCount, 1)
    d1 = Pack_sendSsoMsg_simple(msg, 'FL', 3, 2014428573, 'mqq.IMService.FriendListServiceServantObj',
                                'GetFriendListReq')
    d2 = Make_sendSsoMsg(self, 'friendlist.getFriendGroupList', d1)
    data = Pack(self, d2, 2)
    return data


def Pack_MessageSvc_offlinemsg(self, qqnumber, text):
    """
    发送消息
    """
    msg = ''
    msg += out.WriteLong(self.qqnum, 0)
    msg += out.WriteLong(self.qqnum, 1)
    msg += out.WriteLong(qqnumber, 2)
    msg += out.WriteLong(int(time.time()), 3)
    msg += out.WriteStringByte(text, 4)
    msg += out.WriteStringByte('', 5)
    msg += out.WriteInt(0, 6)
    msg += out.WriteInt(0, 7)
    msg += out.WriteInt(1, 8)
    msg += out.WriteSimpleList(text, 9)
    msg += out.WriteInt(0, 10)
    msg += out.WriteInt(0, 11)
    msg += out.WriteInt(0, 12)
    msg += out.WriteInt(0, 14)

    msg1 = ''
    msg1 += out.WriteJceStruct(Coder.hexstr2str(msg), 0)  ##十六进制转换字符串
    map = config.JceMap()
    map.key_type = config.TYPE_STRING1
    map.value_type = config.TYPE_SIMPLE_LIST
    map.key = 'req_offlinemsg'
    map.value = Coder.hexstr2str(msg1)  ##十六进制转换字符串
    value = out.WriteMap(map, 0)

    data = ''
    data += self.Write_RequestPacket(3, self.seq, 'MessageSvc', 'offlinemsg', Coder.hexstr2str(value))
    reee = Coder.num2hexstr(len(data) / 2 + 4, 4) + data
    req = self.Make_sendSsoMsg('MessageSvc.offlinemsg', reee)
    return Pack(self, req, 2)


def Pack_FriendListService_GetTroopListReqV2(self):
    """
    获取群列表
    """
    msg = ''
    msg += out.WriteLong(self.qqnum, 0)
    msg += out.WriteInt(0, 1)
    msg += out.WriteInt(0, 4)
    msg += out.WriteInt(5, 5)

    value = Pack_sendSsoMsg_simple(msg, 'GetTroopListReqV2', 3, self.seq, 'mqq.IMService.FriendListServiceServantObj',
                                   'GetTroopListReqV2')
    value1 = Make_sendSsoMsg(self, 'FriendList.GetTroopListReqV2', value)
    return Pack(self, value1, 2)


def Pack_friendlist_getUserAddFriendSetting(self, addqqnum):
    """
    获取添加好友设置信息

    """
    msg = ''
    msg += out.WriteInt(self.qqnum, 0)
    msg += out.WriteInt(addqqnum, 1)
    msg += out.WriteShort(3001, 2)
    msg += out.WriteByte(0, 3)
    msg += out.WriteByte(1, 5)
    n = random.randint(100000, 1000000)
    value = Pack_sendSsoMsg_simple(msg, 'FS', 3, n, 'mqq.IMService.FriendListServiceServantObj',
                                   'GetUserAddFriendSettingReq')
    value1 = Make_sendSsoMsg(self, 'friendlist.getUserAddFriendSetting', value)
    return Pack(self, value1, 2)


def Pack_AddFriendReq(self, my_qqnumber, add_qqnumber, verify_type, message):
    """
    添加好友

    """
    msg = ''
    msg += out.WriteInt(my_qqnumber, 0)
    msg += out.WriteInt(add_qqnumber, 1)
    msg += out.WriteShort(verify_type, 2)
    msg += out.WriteByte(1, 3)
    msg += out.WriteByte(1, 4)
    msg += out.WriteByte(len(message), 5)
    messageHex = message
    msg += out.WriteStringByte(messageHex, 6)
    msg += out.WriteByte(0, 7)
    msg += out.WriteByte(1, 8)
    msg += out.WriteShort(3001, 10)
    msg += out.WriteByte(0, 11)
    msg += out.WriteByte(0, 15)
    n = random.randint(100000, 1000000)
    value = Pack_sendSsoMsg_simple(msg, 'AF', 3, n, 'mqq.IMService.FriendListServiceServantObj', 'AddFriendReq')
    value1 = Make_sendSsoMsg(self, 'friendlist.addFriend', value)
    return Pack(self, value1, 2)


def Pack_ProfileService_GroupMngReq(self, group_number, message):
    data = ''
    data += Coder.num2hexstr(int(group_number), 4)
    data += Coder.num2hexstr(int(self.qqnum), 4)
    data += Coder.num2hexstr(len(message), 2)
    data += Coder.str2hexstr(message)
    msg = ''
    msg += out.WriteLong(1, 0)
    msg += out.WriteLong(self.qqnum, 1)
    msg += out.WriteSimpleList(Coder.hexstr2str(data), 2)
    msg += out.WriteByte(0, 3)
    msg += out.WriteStringByte('', 4)
    msg += out.WriteByte(0, 5)
    msg += out.WriteInt(3001, 6)
    msg += out.WriteShort(0, 7)
    n = random.randint(1, 345543)
    value = Pack_sendSsoMsg_simple(msg, 'GroupMngReq', 3, n, 'KQQ.ProfileService.ProfileServantObj', 'GroupMngReq')
    value1 = Make_sendSsoMsg(self, 'ProfileService.GroupMngReq', value)
    return Pack(self, value1, 2)


def Pack_MessageSvc_SendGroupMsg(self, group_number, message):
    msg = ''
    msg += out.WriteLong(self.qqnum, 0)
    msg += out.WriteLong(group_number, 1)
    msg += out.WriteStringByte(message, 2)
    msg += out.WriteInt(1, 3)
    msg += out.WriteSimpleList(message, 4)
    msg += out.WriteInt(0, 5)
    msg += out.WriteInt(0, 6)
    msg += out.WriteInt(0, 7)
    msg += out.WriteInt(0, 8)
    msg += out.WriteInt(0, 9)
    msg += out.WriteInt(0, 10)
    msg += out.WriteInt(0, 11)
    msg += out.WriteInt(0, 12)
    msg += out.WriteInt(0, 13)
    value = Pack_sendSsoMsg_simple(msg, 'req_SendGroupMsg', 3, self.seq, 'MessageSvc', 'SendGroupMsg')
    value1 = Make_sendSsoMsg(self, 'MessageSvc.SendGroupMsg', value)
    return Pack(self, value1, 2)


def Pack_QzoneNewService_getWidget(self):
    """
    未完成
    :param self:
    :return:
    """
    print Coder.qqnum2hexstr(self.qqnum)
    msg = ''
    msg += Coder.trim(
        '00 00 00 2C 00 00 00 20 53 51 51 7A 6F 6E 65 53 76 63 2E 67 65 74 4E 65 77 41 63 74 69 76 65 46 65 65 64 73 00 00 00 08 31 61 D2 53 00 00 01 CF 01 37 5D 12 00 0F 42 5B 22')
    msg += Coder.qqnum2hexstr(self.qqnum)
    msg += Coder.trim(
        '36 19 56 31 5F 41 4E 44 5F 53 51 5F 35 2E 37 2E 31 5F 32 35 38 5F 59 59 42 5F 44 46 21 51 7A 6F 6E 65 4E 65 77 53 65 72 76 69 63 65 2E 67 65 74 4E 65 77 41 63 74 69 76 65 46 65 65 64 73 56 75 69 3D 38 36 30 38 34 31 30 32 33 36 37 36 34 36 39 26 6D 61 63 3D 30 30 3A 31 36 3A 36 64 3A 66 30 3A 32 39 3A 63 36 26 6D 3D 38 31 39 30 51 26 6F 3D 34 2E 31 2E 32 26 61 3D 31 36 26 73 63 3D 31 26 73 64 3D 30 26 70 3D 35 34 30 2A 39 36 30 26 66 3D 59 75 4C 6F 6E 67 26 6E 3D 77 69 66 69 26 6C 6F 6E 67 69 74 75 64 65 3D 26 6C 61 74 69 74 75 64 65 3D 6A 00 40 1D 00 0C 28 00 01 00 01 1D 00 00 01 00 0B 7A 0C 1C 2C 3D 00 00 06 00 00 00 00 00 00 0B 8D 00 00 5A')
    p1 = Coder.trim(
        '08 00 02 06 09 67 65 74 57 69 64 67 65 74 18 00 01 06 1D 4E 53 5F 4D 4F 42 49 4C 45 5F 57 49 44 47 45 54 2E 47 65 74 57 69 64 67 65 74 52 65 71 1D 00 00 0D 0A 00 FF 12')
    p2 = ''
    p3 = Coder.trim('20 08 36 00 0B 06 07 68 6F 73 74 75 69 6E 18 00 01 06 05 69 6E 74 36 34 1D 00 00 05 02')
    p4 = Coder.qqnum2hexstr(self.qqnum)
    msg += Coder.str2hexstr(zlib.compress(Coder.hexstr2str(p1 + p2 + p3 + p4)))
    msg += Coder.trim(
        '9D 00 00 3C 08 00 01 06 0B 62 75 73 69 43 6F 6D 70 43 74 6C 18 00 01 06 1B 51 4D 46 5F 50 52 4F 54 4F 43 41 4C 2E 51 6D 66 42 75 73 69 43 6F 6E 74 72 6F 6C 1D 00 00 08 0A 00 01 10 5D 20 01 0B AC BC CA 0C 1C 23 00 00')
    msg += '0' + Coder.qqnum2hexstr(int(time.time() * 1000)) + '0b'
    print msg
    return Pack(self, TEA.entea_hexstr(msg, self.qqkey), 2)


def Pack_QzoneNewService_getApplist(self, targetQQ):
    """
    获取指定qq号说说列表(完成)
    """
    msg = ''
    msg += Coder.trim(
        '00 00 00 25 00 00 00 19 53 51 51 7A 6F 6E 65 53 76 63 2E 67 65 74 41 70 70 6C 69 73 74 00 00 00 08 71 72 5A A3 00 00 01 BE 02 00 00 C4 27 12 00 0F 42 5B 22')
    msg += Coder.qqnum2hexstr(self.qqnum)
    msg += Coder.trim(
        '36 19 56 31 5F 41 4E 44 5F 53 51 5F 35 2E 38 2E 30 5F 32 36 34 5F 59 59 42 5F 44 46 1A 51 7A 6F 6E 65 4E 65 77 53 65 72 76 69 63 65 2E 67 65 74 41 70 70 6C 69 73 74 56 75 69 3D 38 36 30 38 34 31 30 32 33 36 37 36 34 36 39 26 6D 61 63 3D 30 30 3A 31 36 3A 36 64 3A 66 30 3A 32 39 3A 63 36 26 6D 3D 38 31 39 30 51 26 6F 3D 34 2E 31 2E 32 26 61 3D 31 36 26 73 63 3D 31 26 73 64 3D 30 26 70 3D 35 34 30 2A 39 36 30 26 66 3D 59 75 4C 6F 6E 67 26 6E 3D 77 69 66 69 26 6C 6F 6E 67 69 74 75 64 65 3D 26 6C 61 74 69 74 75 64 65 3D 6A 00 40 1D 00 0C 28 00 01 00 01 1D 00 00 01 00 0B 7A 0C 1C 2C 3D 00 00 06 00 00 00 00 00 00 0B 8D 00 01 00 88')
    p1 = Coder.trim(
        '08 00 03 06 05 72 65 66 65 72 18 00 01 06 06 73 74 72 69 6E 67 1D 00 00 0D 06 0B 67 65 74 4D 61 69 6E 50 61 67 65 06 0A 67 65 74 41 70 70 6C 69 73 74 18 00 01 06 22 4E 53 5F 4D 4F 42 49 4C 45 5F 46 45 45 44 53 2E 6D 6F 62 69 6C 65 5F 61 70 70 6C 69 73 74 5F 72 65 71 1D 00 00 12 0A 02')
    p2 = Coder.qqnum2hexstr(targetQQ)
    p3 = Coder.trim(
        '11 01 37 20 0A 36 00 4C 50 01 6C 0B 06 07 68 6F 73 74 75 69 6E 18 00 01 06 05 69 6E 74 36 34 1D 00 00 05 02')
    p4 = Coder.qqnum2hexstr(self.qqnum)
    msg += Coder.str2hexstr(zlib.compress(Coder.hexstr2str(p1 + p2 + p3 + p4)))
    msg += Coder.trim(
        '9D 00 00 3D 08 00 01 06 0B 62 75 73 69 43 6F 6D 70 43 74 6C 18 00 01 06 1B 51 4D 46 5F 50 52 4F 54 4F 43 41 4C 2E 51 6D 66 42 75 73 69 43 6F 6E 74 72 6F 6C 1D 00 00 09 0A 00 01 11 00 8B 20 01 0B AC BC CA 0C 1C 23 00 00')
    msg += '0' + Coder.qqnum2hexstr(int(time.time() * 1000)) + '0b'

    data1 = TEA.entea_hexstr(msg, self.qqkey)
    return Pack(self, data1, 2)


def Pack_SummaryCardServantObj_ReqCondSearch(self, message):
    alllong = Coder.num2hexstr(149 + len(message))
    msglong = Coder.num2hexstr(len(message))
    mainlong = Coder.num2hexstr(89 + len(message))
    erlong = Coder.num2hexstr(50 + len(message))
    msg = ''
    msg += Coder.trim(
        '00 00 00 29 00 00 00 1D 53 75 6D 6D 61 72 79 43 61 72 64 2E 52 65 71 43 6F 6E 64 53 65 61 72 63 68 00 00 00 08 E6 FC 95 13 00 00 00')
    msg += alllong
    msg += Coder.trim(
        '10 03 2C 3C 42 7A 15 57 12 56 15 53 75 6D 6D 61 72 79 43 61 72 64 53 65 72 76 61 6E 74 4F 62 6A 66 0D 52 65 71 43 6F 6E 64 53 65 61 72 63 68 7D 00 00')
    msg += mainlong
    msg += Coder.trim(
        '08 00 02 06 07 52 65 71 48 65 61 64 1D 00 00 04 0A 00 02 0B 06 0D 52 65 71 43 6F 6E 64 53 65 61 72 63 68 1D 00 00')
    msg += erlong
    msg += Coder.trim('0A 0C 1C')
    msg += Coder.trim('20 01 36')
    msg += msglong
    msg += Coder.str2hexstr(message)
    msg += Coder.trim(
        '4C 5D 00 00 10 00 00 00 31 00 00 00 00 00 00 00 00 00 00 00 00 6C 7D 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0B 8C 98 0C A8 0C')
    data = TEA.entea_hexstr(msg, self.qqkey)
    return Pack(self, data, 2)


def Pack_SummaryCardServantObj_ReqCondSearch_again(self, message, n):
    alllong = Coder.num2hexstr(151 + len(message))
    msglong = Coder.num2hexstr(len(message))
    mainlong = Coder.num2hexstr(91 + len(message))
    erlong = Coder.num2hexstr(52 + len(message))
    COUNT = Coder.num2hexstr(n)
    msg = ''
    msg += Coder.trim(
        '00 00 00 29 00 00 00 1D 53 75 6D 6D 61 72 79 43 61 72 64 2E 52 65 71 43 6F 6E 64 53 65 61 72 63 68 00 00 00 08 E4 A7 76 B4 00 00 00')
    msg += alllong
    msg += Coder.trim(
        '10 03 2C 3C 42 7A 15 57 8D 56 15 53 75 6D 6D 61 72 79 43 61 72 64 53 65 72 76 61 6E 74 4F 62 6A 66 0D 52 65 71 43 6F 6E 64 53 65 61 72 63 68 7D 00 00')
    msg += mainlong
    msg += Coder.trim(
        '08 00 02 06 07 52 65 71 48 65 61 64 1D 00 00 04 0A 00 02 0B 06 0D 52 65 71 43 6F 6E 64 53 65 61 72 63 68 1D 00 00')
    msg += erlong
    msg += Coder.trim('0A 00')
    msg += COUNT
    msg += Coder.trim('10 01')
    msg += Coder.trim('20 01 36')
    msg += msglong
    msg += Coder.str2hexstr(message)
    msg += Coder.trim(
        '4C 5D 00 00 10 00 00 00 31 00 00 00 00 00 00 00 00 00 00 00 00 6C 7D 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0B 8C 98 0C A8 0C')
    data = TEA.entea_hexstr(msg, self.qqkey)
    return Pack(self, data, 2)


def Pack_friendlistGetAutoInfoReq(self, targetQQ):
    msg = ''
    msg += '10032c3c422ab7e6ac56296d71712e494d536572766963652e467269656e644c6973745365727669636553657276616e744f626a660e4765744175746f496e666f5265717d00002108000106064741495245511d0000120a02'
    msg += Coder.qqnum2hexstr(self.qqnum)
    msg += '12' + Coder.qqnum2hexstr(targetQQ)
    msg += '20013127144c0b8c980ca80c'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    value = Make_sendSsoMsg(self, 'friendlist.GetAutoInfoReq', data)
    return Pack(self, value, 2)


def Pack_ProfileServicePbReqSystemMsgActionFriend(self, targetQQ):
    hex16time = str(int(time.time())) + '000000'
    msg = ''
    msg += '080110'
    msg += PB.encode_Varints(int(hex16time))
    msg += '18'
    msg += PB.encode_Varints(int(targetQQ))
    msg += '2001280130003800420f0802980300a20300b2030408001000'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    value = Make_sendSsoMsg(self, 'ProfileService.Pb.ReqSystemMsgAction.Friend', data)
    return Pack(self, value, 2)


def Pack_GetSimpleInfo(targetQQ):
    msg = ''
    msg += '10032c3c423e5722a656244b51512e50726f66696c65536572766963652e50726f66696c6553657276616e744f626a660d47657453696d706c65496e666f7d0000'
    qqq = '0a1c260039000103' + Coder.num2hexstr(targetQQ, 8) + '400150016c7c8c9001ac0b'
    qqq1 = Coder.num2hexstr(len(qqq) / 2) + qqq
    qqq2 = '08000106037265711d0000' + qqq1
    msg += Coder.num2hexstr(len(qqq2) / 2) + qqq2
    msg += '8c980ca80c'
    return msg


def Pack_EncounterSvc_ReqGetEncounter(self, long, lat):
    """
    获取附近的人
    """
    # 0000002c00000020456e636f756e7465725376632e526571476574456e636f756e74657200000008844cd92b000001ff
    msg = ''
    msg += Coder.trim(
        '00 00 00 2C 00 00 00 20 45 6E 63 6F 75 6E 74 65 72 53 76 63 2E 52 65 71 47 65 74 45 6E 63 6F 75 6E 74 65 72 00 00 00 08 D7 1C 77 15 00 00 01 88')
    msg += Coder.trim('10 03 2C 3C 42')
    self.qq00001 = random.randint(10000000, 99999999)
    msg += str(self.qq00001)
    msg += Coder.trim(
        ' 56 0C 45 6E 63 6F 75 6E 74 65 72 4F 62 6A 66 13 43 4D 44 5F 47 45 54 5F 45 4E 43 4F 55 4E 54 45 52 56 32 7D 00 01 01 4E 08 00 02 06 09 52 65 71 48 65 61 64 65 72 1D 00 00 13 0A 00 02 12')
    msg += Coder.trim(Coder.qqnum2hexstr(self.qqnum))
    msg += Coder.trim('22 20 02 9A A9 3C 40 02 5C 6C 0B 06 11')
    msg += Coder.trim('52 65 71 47 65 74 45 6E 63 6F 75 6E 74 65 72 56 32 1D 00 01 01 11 0A 0A 0A 02')
    msg += Coder.num2hexstr(lat, 4)
    msg += Coder.trim('12')
    msg += Coder.num2hexstr(long, 4)
    msg += Coder.trim(
        '2C 30 01 0B 19 0C 29 0C 36 16 42 31 5F 51 51 5F 4E 65 69 67 68 62 6F 72 5F 61 6E 64 72 6F 69 64 46 08 4E 7A 56 4B 5F 71 47 45 5C 6C 0B 1A 0C 12 35 A4 E9 00 22 35 A4 E9 00 3C 4C 56 00 0B 20 00 30 FF 5D 00 00 01 00 6C 71 07 D0 80 FF 9C BD 00 00 72 00 00 00 72')
    msg += Coder.trim(
        '10 03 2C 3C 40 01 56 1C 50 75 62 41 63 63 6F 75 6E 74 53 76 63 2E 6E 65 61 72 62 79 5F 70 75 62 61 63 63 74 66 0E 6E 65 61 72 62 79 5F 70 75 62 61 63 63 74 7D 00 00 31 08 00 01 06 0E 6E 65 61 72 62 79 5F 70 75 62 61 63 63 74 1D 00 00 1A 0A 00 02 1D 00 0C 20 02 3A 0A 02 01 78 40 64 12 06 1D 64 AD 2C 30 01 0B 0B 0B 8C 98 0C A8 0C CC D0 00 EC FC 0F FC 10 F1 11 01 E0 FC 12 FC 13 FC 14 F0 15 00 FC 16 FA 17 0A 02 01 78 40 64 12 06 1D 64 AD 2C 30 01 0B 19 0C 29 0C 36 00 46 00 50 01 6C 0B F0 18 0F FD 19 00 0C FC 1A FC 1B 0B 8C 98 0C A8 0C')
    print msg
    data = TEA.entea_hexstr(msg, self.qqkey)
    return Pack(self, data, 2)


def Pack_EncounterSvc_ReqGetEncounter2(self):
    msg = ''
    msg += '10032c3c42'
    msg += str(self.qq00001 + 1)
    msg += '560c456e636f756e7465724f626a6613434d445f4745545f454e434f554e54455256327d0001'
    body = '08000206095265714865616465721d0000130a000312'
    body += Coder.qqnum2hexstr(self.qqnum)
    body += '2220029f533c40025c6c0b0611526571476574456e636f756e74657256321d0001'

    body_1 = '0a0a0a0c1c20ff3c0b361642315f51515f4e65696768626f725f616e64726f696446084e7a564b5f7147455c600289'
    body_1 += '00100a030000c6850826a74b10e00b0a03000014e6e4bf7c2e10e00b0a030000586d8f6806bd10cb0b0a030000b8ee65d56cda10c40b0a0300003c8c4048eb5010cc0b0a0300003c8c4048fdd010c60b0a0300003c8c4049069010c50b0a0300003c8c40490f6010b30b0a0300003c8c4048f7d010b80b0a0300003c8c404902e010b40b0a0300003c8c4048ed7010b00b0a030000246968a5359c10b50b0a0300003c8c404910e010af0b0a0300003c8c4049033010ab0b0a0300003c8c404907c010a90b0a0300003c8c4049085010af0b'
    body_1 += '9900010a0101cc100121361f31179240ff0b0b1a02'
    body_1 += Coder.num2hexstr(int(time.time()), 4)
    body_1 += '12'
    body_1 += Coder.num2hexstr(self.lat, 4)
    body_1 += '22'
    body_1 += Coder.num2hexstr(self.long, 4)
    body_1 += '3c43'
    body_1 += '01c9d64000b778c0'
    body_1 += '56'
    city = Coder.str2hexstr('浙江省杭州市')
    body_1 += Coder.num2hexstr(len(city) / 2) + city
    body_1 += '6d0000130d000c1c2301c9c38000b785403c4c50ff6c7c0b200130ff5d000001006c7107d080ff9cccd001ecfc0ffc10f11101e0fc12fc13fc14f01501fc16f0180ffd1900000e1800200028003000380040004a00fc1afc1bfc1cf61d'
    j = '{"dtype":1,"muid":"8DF9E26F89DDC39EEA9F32691174D17C","carrier":2,"conn":1,"posw":216,"posh":150,"lat":' + str(
        self.lat) + ',"lng":' + str(self.long) + ',"c_os":"android","c_osver":"5.1.1"}'
    jsondata = Coder.str2hexstr(j)
    body_1 += Coder.num2hexstr(len(jsondata) / 2) + jsondata
    body_1 += 'f01e3ffc1ff020030b'

    body += Coder.num2hexstr(len(body_1) / 2, 2) + body_1
    msg += Coder.num2hexstr(len(body) / 2, 2) + body

    msg += '8c980ca80c'
    print msg
    d1 = '0000002c00000020456e636f756e7465725376632e526571476574456e636f756e746572'
    d1 += Coder.trim('00 00 00 08 D7 1C 77 15')
    d2 = d1 + Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    data = TEA.entea_hexstr(d2, self.qqkey)
    return Pack(self, data, 2)


def Pack_ProfileServicePbReqSystemMsgActionGroup(targetQQ, GroupNumber):
    hex16time = str(int(time.time())) + '000000'
    msg = ''
    msg += '080210'
    msg += PB.encode_Varints(int(hex16time))
    msg += '18'
    msg += PB.encode_Varints(int(targetQQ))
    msg += '200128013005380142'
    data = '080b10' + PB.encode_Varints(int(GroupNumber))
    msg += PB.encode_Varints(int(len(data) / 2)) + data
    return msg
    # print msg
    # data = Coder.num2hexstr(len(msg)/2+4,4) + msg
    # value = Make_sendSsoMsg(self,'ProfileService.Pb.ReqSystemMsgAction.Group',data)
    # return Pack(self,value,2)


def Pack_AutoReceiveGroupRequests(self, targetQQ, GroupNumber):
    """
    同意申请加入群（压缩）暂未完成
    """
    number = random.uniform(10000, 99999)
    msg = ''
    msg += '08' + PB.encode_Varints(int(number))
    msg += '121c50726f66696c65536572766963652e47657453696d706c65496e666f187222'
    GetSimpleInfo = Pack_GetSimpleInfo(targetQQ)
    msg += Coder.num2hexstr(len(GetSimpleInfo) / 2) + GetSimpleInfo + '2801'
    d1 = '0a' + PB.encode_Varints(int(len(msg) / 2)) + msg
    msg1 = ''
    msg1 += '08' + PB.encode_Varints(int(number + 1))
    msg1 += '122a50726f66696c65536572766963652e50622e52657153797374656d4d7367416374696f6e2e47726f7570'
    ActionGroup = Pack_ProfileServicePbReqSystemMsgActionGroup(targetQQ, GroupNumber)
    msg1 += '182722' + PB.encode_Varints(int(len(ActionGroup) / 2)) + ActionGroup + '2801'
    d2 = '0a' + PB.encode_Varints(int(len(msg1) / 2)) + msg1
    msg2 = ''
    msg2 += '08' + PB.encode_Varints(int(number + 2))
    msg2 += '122850726f66696c65536572766963652e50622e52657153797374656d4d7367526561642e47726f7570180f220b10'
    hex16time = str(int(time.time())) + '123123'
    msg2 += PB.encode_Varints(int(hex16time)) + '20032801'
    d3 = '0a' + PB.encode_Varints(int(len(msg2) / 2)) + msg2
    data = d1 + d2 + d3
    print data
    gzip = zlib.compress(data.decode('hex'))
    gzipdata = gzip.encode('hex')
    retdata = Coder.num2hexstr(len(gzipdata) / 2 + 4, 4) + gzipdata
    value = Make_sendSsoMsg(self, 'SSO.LoginMerge', retdata)
    return Pack(self, value, 2)


def Pack_FriendListServiceServantObj_GetTroopMemberListReq(self, GroupNumber):
    msg = ''
    msg += Coder.trim(
        '00 00 00 2D 00 00 00 21 66 72 69 65 6E 64 6C 69 73 74 2E 67 65 74 54 72 6F 6F 70 4D 65 6D 62 65 72 4C 69 73 74 00 00 00 08 31 61 D2 53 00 00 00 7D')
    msg += Coder.trim(
        '10 03 2C 3C 42 2F 42 20 DF 56 29 6D 71 71 2E 49 4D 53 65 72 76 69 63 65 2E 46 72 69 65 6E 64 4C 69 73 74 53 65 72 76 69 63 65 53 65 72 76 61 6E 74 4F 62 6A 66 15 47 65 74 54 72 6F 6F 70 4D 65 6D 62 65 72 4C 69 73 74 52 65 71 7D 00 00 25 08 00 01 06 04 47 54 4D 4C 1D 00 00 18 0A 02')
    msg += Coder.qqnum2hexstr(self.qqnum)
    msg += Coder.trim('12')
    msg += Coder.qqnum2hexstr(GroupNumber)
    msg += Coder.trim('2C 33 00 00 00 00 9D 3F C2 21 40 02 0B 8C 98 0C A8 0C')
    data = TEA.entea_hexstr(msg, self.qqkey)
    data = TEA.entea_hexstr(msg, self.qqkey)
    return Pack(self, data, 2)


def Pack_GroupRemovesMember(self, targetQQ, GroupNumber):
    msg = ''
    msg += '08a0111000180022'
    data = '080510' + PB.encode_Varints(int(GroupNumber)) + '1800'
    d1 = '08' + PB.encode_Varints(int(targetQQ)) + '12' + PB.encode_Varints(len(data) / 2) + data
    msg += PB.encode_Varints(len(d1) / 2) + d1
    print msg
    retdata = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    value = Make_sendSsoMsg(self, 'OidbSvc.0x8a0_0', retdata)
    return Pack(self, value, 2)


def Pack_friendlistModifyGroupCardReq(self, name, GroupNumber):
    msg = ''
    msg += '10032c3c42122a4b9e56296d71712e494d536572766963652e467269656e644c6973745365727669636553657276616e744f626a66124d6f6469667947726f7570436172645265717d0000'
    msg1 = '08000106064d47435245511d0000'
    msg2 = '0a0c12' + Coder.qqnum2hexstr(GroupNumber)
    msg2 += '2c3900010a02' + Coder.qqnum2hexstr(self.qqnum)
    msg2 += '100126'
    msg3 = Coder.str2hexstr(name)
    msg2 += Coder.num2hexstr(len(msg3) / 2) + msg3
    msg2 += '30ff4600560066000b0b'
    msg1 += Coder.num2hexstr(len(msg2) / 2) + msg2
    msg += Coder.num2hexstr(len(msg1) / 2) + msg1 + '8c980ca80c'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    value = Make_sendSsoMsg(self, 'friendlist.ModifyGroupCardReq', data)
    return Pack(self, value, 2)


def Pack_friendlistSetGroupReq(self, name):
    msg = '10032c3c42122a4ba956296d71712e494d536572766963652e467269656e644c6973745365727669636553657276616e744f626a660b53657447726f75705265717d0000'
    msg1 = '080001060b53657447726f75705265711d0000'
    msg2 = '0a0c12' + Coder.qqnum2hexstr(self.qqnum) + '2d0000'
    namehex = Coder.str2hexstr(name)
    msg3 = '04' + Coder.num2hexstr(len(namehex) / 2) + namehex
    msg2 += Coder.num2hexstr(len(msg3) / 2) + msg3
    msg1 += Coder.num2hexstr(len(msg2) / 2) + msg2 + '0b'
    msg += Coder.num2hexstr(len(msg1) / 2) + msg1 + '8c980ca80c'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    value = Make_sendSsoMsg(self, 'friendlist.SetGroupReq', data)
    return Pack(self, value, 2)


def Pack_OnlinePushRespPush(self, id, pbdata, code):
    msg = '10032c3c42d57947ad560a4f6e6c696e6550757368660e53766352657370507573684d73677d0000'
    msg1 = '0800010604726573701d0000'
    msg2 = '0a02' + Coder.qqnum2hexstr(self.qqnum)
    msg2 += '1900010a02' + Coder.qqnum2hexstr(self.qqnum)
    msg2 += '1c21' + Coder.num2hexstr(id, 2) + '3d0000'
    msg3 = pbdata
    msg2 += Coder.num2hexstr(len(msg3) / 2) + msg3 + '0b22' + Coder.num2hexstr(code, 4) + '0b'
    msg1 += Coder.num2hexstr(len(msg2) / 2) + msg2
    msg += Coder.num2hexstr(len(msg1) / 2) + msg1 + '8c980ca80c'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    value = Make_sendSsoMsg(self, 'OnlinePush.RespPush', data)
    return Pack(self, value, 2)


def Pack_ProfileServiceReqBatchProcess(self, groupnumber):
    PB1 = '088d1110012240089484af5f123908' + PB.encode_Varints(int(
        groupnumber)) + '122f08001000180020002800300040007a008a0100920100a00200a80200b00200c20200ca02023000d202023200b803001800'
    PB2 = '0899111001221208' + PB.encode_Varints(int(groupnumber)) + '100018022a02080030063800'
    msg = '10032c3c42047dfcfc560e50726f66696c6553657276696365660f526571426174636850726f636573737d0001'
    msg1 = '080001060f526571426174636850726f636573731d0000'
    msg2 = '0a090002'
    msg2_1 = '0a00011c2d0000' + Pack_Len(PB1) + '0b'
    msg2_2 = '0a00011c2d0000' + Pack_Len(PB2) + '0b'
    msg2 += msg2_1 + msg2_2 + '0b'
    msg1 += Pack_Len(msg2)
    msg += Pack_Len(msg1, 2) + '8c980ca80c'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    value = Make_sendSsoMsg(self, 'ProfileService.ReqBatchProcess', data)
    return Pack(self, value, 2)


def Pack_Len(packdatahex, n=1, k=0):
    return Coder.num2hexstr(len(packdatahex) / 2 + k, n) + packdatahex


def Pack_LongConnOffPicUp(self, qqnumber, targetQQ, imgname):
    imgnamehex = (imgname + '.jpg').encode('hex')
    msg = '080112'
    msg1 = '08' + PB.encode_Varints(int(qqnumber))
    msg1 += '10' + PB.encode_Varints(int(targetQQ))
    msg1 += '18002210' + imgname + '28b6ea0132'
    msg1 += Coder.num2hexstr(len(imgnamehex) / 2) + imgnamehex
    msg1 += '3805400950006001680070d00578c0078001eb078a0109352e382e302e323634'
    msg += Coder.num2hexstr(len(msg1) / 2) + msg1 + '5003'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    value = Make_sendSsoMsg(self, 'LongConn.OffPicUp', data)
    return Pack(self, value, 2)


def pack_PicUpDataUp(self, hex1, hex2, hex3, imgdata):
    msg = '1a0c50696355702e446174615570209939280030b424388020400112b0011097f4031800208020328001'
    msg += hex1 + '4210'
    msg += hex2 + '4a10'
    msg += hex3
    msg += imgdata
    return Pack(self, msg, 2)


def SendfriendImageMsg(self, targetQQ, imgnamehex, ):
    # 1085db041a252f35336236353830352d633831392d343333332d623035392d62343333663835313135346428eb073a10ca391533c21daa0db3fbaa6e5e3bddc240c00748d00552252f35336236353830352d633831392d343333332d623035392d6234333366383531313534646800800103c0019466c801e7ad02208d830128bbb0a79505322408c4c08bc20510c4c08bc205288ad4979c0248a5af96c60558c6c38f8e0b68c4c08bc2054000
    QQpbdata = PB.encode_Varints(int(targetQQ))
    msg = '0a080a0608' + QQpbdata
    msg += '120808011000188d8301'
    msg1 = '0a24' + imgnamehex


def SendImageMsg(self, GroupQQ, targetQQ, ImgName, ImaFileName, ImgPath):
    ImgNameHex = ImgName
    ImaFileNameHex = ImaFileName.encode('hex')
    ImgPathHex = ImgPath.encode('hex')
    PBtarget = PB.encode_Varints(int(targetQQ))
    if GroupQQ:
        PBGroup = PB.encode_Varints(int(GroupQQ))
        PB_0A_1 = '08' + PBGroup + '10' + PBtarget
    else:
        PB_0A_1 = '08' + PBtarget
    PB_0A_2 = '1a' + PB.encode_Varints(len(PB_0A_1) / 2) + PB_0A_1
    PB_0A_3 = PB.encode_Varints(len(PB_0A_2) / 2) + PB_0A_2
    PB_0A = '0a' + PB_0A_3
    PB_12_D = int(random.uniform(1000000000, 9999999999))
    PB_12 = '120a0801100018'+PB.encode_Varints(PB_12_D)
    PB_Send_MSG_0A = '0a' + PB.encode_Varints(len(ImaFileNameHex) / 2) + ImaFileNameHex
    PB_Send_MSG_10 = '10b9d203'
    PB_Send_MSG_1a = '1a' + PB.encode_Varints(len(ImgPathHex) / 2) + ImgPathHex
    PB_Send_MSG_28 = '28eb07'
    PB_Send_MSG_3a = '3a' + PB.encode_Varints(len(ImgNameHex) / 2) + ImgNameHex
    PB_Send_MSG_40 = '40c007'
    PB_Send_MSG_48 = '48d005'
    PB_Send_MSG_52 = '52' + PB.encode_Varints(len(ImgPathHex) / 2) + ImgPathHex
    PB_Send_MSG_68 = '6800'
    PB_Send_MSG_8001 = '800103'
    PB_Send_MSG_C001 = 'c001a18e01'
    PB_Send_MSG_C801 = 'c801868902'
    PB_Send_MSG = PB_Send_MSG_0A + PB_Send_MSG_10 + PB_Send_MSG_1a + PB_Send_MSG_28 + PB_Send_MSG_3a + PB_Send_MSG_40 + PB_Send_MSG_48 + PB_Send_MSG_52 + PB_Send_MSG_68 + PB_Send_MSG_8001 + PB_Send_MSG_C001 + PB_Send_MSG_C801
    PB_1A_1 = '22' + PB.encode_Varints(len(PB_Send_MSG) / 2) + PB_Send_MSG
    PB_1A_2 = '12' + PB.encode_Varints(len(PB_1A_1) / 2) + PB_1A_1
    PB_1A_3 = '0a' + PB.encode_Varints(len(PB_1A_2) / 2) + PB_1A_2
    PB_1A = '1a' + PB.encode_Varints(len(PB_1A_3) / 2) + PB_1A_3
    PB_20_D = int(random.uniform(10000, 99999))
    PB_20 = '20'+PB.encode_Varints(PB_20_D)
    PB_28_D = int(random.uniform(1000000000, 9999999999))
    PB_28 = '28'+PB.encode_Varints(PB_28_D)
    PB_32_MSG = PB.msg()
    PB_32 = '32' + PB.encode_Varints(len(PB_32_MSG) / 2) + PB_32_MSG
    PB_40 = '4000'
    PB_DATA = PB_0A + PB_12 + PB_1A + PB_20 + PB_28 + PB_32 + PB_40
    data = Coder.num2hexstr(len(PB_DATA) / 2 + 4, 4) + PB_DATA
    value = Make_sendSsoMsg(self, 'MessageSvc.PbSendMsg', data)
    return Pack(self, value, 2)

hex1 = Coder.trim(
    '39 33 36 45 45 30 36 42 44 30 33 35 30 39 35 43 39 39 31 43 35 41 32 35 37 32 36 31 34 41 45 34 2E 6A 70 67')
hex2 = Coder.trim('93 6E E0 6B D0 35 09 5C 99 1C 5A 25 72 61 4A E4 ')
pathhex = Coder.trim('2f39666337326266342d393833332d343835642d623437382d346464646265396361336230')
#SendGroupMemberImageMsg('', '511973728', '2080670497', hex2, hex1, pathhex)


# print Pack_ProfileServiceReqBatchProcess('1','296603528')
# print PB.encode_Varints(len('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')/2)
def randomhex(number):
    abc = ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(number / 2)))
    return 'b' * (number - len(abc)) + abc

    # print Pack_LongConnOffPicUp('123','3108153230','296603528')

def Pack_ttt111(number,qqnumber):

    numberhex = str(number).encode('hex')
    #qqnumberhex = Coder.num2hexstr(str(qqnumber),8)
#00d0
# 530000005310032c3c4c56115151536572766963652e47616d65537663660f5265714c61737447616d65496e666f7d00001d080001060f5265714c61737447616d65496e666f1d0000050a00011c0b8c980ca80ccd
# 10032c3c4c56084d43617264537663660571756572797d00002508000106037265711d0000190a00011300000000b942a78e2c3605352e382e304011506d0b8c980ca80ce90cfc0f0b     8c980ca80c
    msg = '10032c3c4200078781561553756d6d6172794361726453657276616e744f626a660e52657153756d6d617279436172647d0001'

    msg1 = '080002060e52657153756d6d617279436172641d0001'
    msg2 = '0a0c10112c3c4c5c6d0000010076'+Pack_Len(numberhex)
    msg2 += '810e34912714ad00000100bd0000'
    data1 = Coder.trim('00 00 00 53 10 03 2C 3C 4C 56 11 51 51 53 65 72 76 69 63 65 2E 47 61 6D 65 53 76 63 66 0F 52 65 71 4C 61 73 74 47 61 6D 65 49 6E 66 6F 7D 00 00 1D 08 00 01 06 0F 52 65 71 4C 61 73 74 47 61 6D 65 49 6E 66 6F 1D 00 00 05 0A 00 01 1C 0B 8C 98 0C A8 0C')
    data2 = '0000004810032c3c4c56084d43617264537663660571756572797d00002508000106037265711d0000190a000113'+Coder.num2hexstr(int(qqnumber),8)+'2c3605352e382e304011506d0b8c980ca80c'
    print data2
    msg2 += Pack_Len(data1)
    msg2 += 'cd0000'+Pack_Len(data2)+'e90cfc0f0b'
    print msg2

    msg1 += Coder.num2hexstr(len(msg2) / 2,4) + msg2 +'0607526571486561641d0000040a00020b'
    msg += Coder.num2hexstr(len(msg1) / 2,4) + msg1 + '8c980ca80c'
    print msg

#10032c3c4200078781561553756d6d6172794361726453657276616e744f626a660e52657153756d6d617279436172647d000100f9080002060e52657153756d6d617279436172641d000100d00a0c10112c3c4c5c6d00000100760e2b38363138333538353133383039810e34912714ad00000100bd0000530000005310032c3c4c56115151536572766963652e47616d65537663660f5265714c61737447616d65496e666f7d00001d080001060f5265714c61737447616d65496e666f1d0000050a00011c0b8c980ca80ccd0000480000004810032c3c4c56084d43617264537663660571756572797d00002508000106037265711d0000190a00011300000000b942a78e2c3605352e382e304011506d0b8c980ca80ce90cfc0f0b0607526571486561641d0000040a00020b8c980ca80c
#Pack_ttt111('+8613754396670','296603528')

#0a0c10112c3c4c5c6d00000100760e2b38363133373534333936363730810e34912714ad00000100bd0000530000005310032c3c4c56115151536572766963652e47616d65537663660f5265714c61737447616d65496e666f7d00001d080001060f5265714c61737447616d65496e666f1d0000050a00011c0b8c980ca80ccd0000460000004810032c3c4c56084d43617264537663660571756572797d00002508000106037265711d0000190a0001130000000011adcf882c3605352e382e304011506d0b8c980c0607526571486561641d0000040a00020b


def Pack_SummaryCardReqSummaryCard(self,phone,qqnumber):
    print phone,qqnumber
    phonehex = ('+86'+str(phone)).encode('hex')
    msg = '10032c3c4200078781561553756d6d6172794361726453657276616e744f626a660e52657153756d6d617279436172647d000100f9080002060e52657153756d6d617279436172641d000100d00a0c10112c3c4c5c6d00000100760e'
    msg += phonehex
    msg += '810e34912714ad00000100bd0000530000005310032c3c4c56115151536572766963652e47616d65537663660f5265714c61737447616d65496e666f7d00001d080001060f5265714c61737447616d65496e666f1d0000050a00011c0b8c980ca80ccd0000480000004810032c3c4c56084d43617264537663660571756572797d00002508000106037265711d0000190a000113'
    msg += Coder.num2hexstr(int(qqnumber),8)
    msg += '2c3605352e382e304011506d0b8c980ca80ce90cfc0f0b0607526571486561641d0000040a00020b8c980ca80c'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    print data
    value = Make_sendSsoMsg(self, 'SummaryCard.ReqSummaryCard', data)
    return Pack(self, value, 2)

#Pack_SummaryCardReqSummaryCard('123','13754396670','296603528')


def Pack_ProfileServiceGetSimpleInfo(self,phone):
    phone = str(phone)
    msg = '10032c3c42632c358856244b51512e50726f66696c65536572766963652e50726f66696c6553657276616e744f626a660d47657453696d706c65496e666f7d00002708000106037265711d00001b0a1c260039000103'
    msg += Coder.num2hexstr(int(phone),8)
    msg +=  '400150016c7c8c9001ac0b8c980ca80c'
    data = Coder.num2hexstr(len(msg) / 2 + 4, 4) + msg
    print data
    value = Make_sendSsoMsg(self, 'ProfileService.GetSimpleInfo', data)
    return Pack(self, value, 2)


#print Coder.trim('03 00 00 00 00 FF FF FF FF 12 58 55 56 72 2D 00 00 1E 31 34 38 31 39 38 37 36 39 38 31 33 38 38 39 61 36 66 66 31 30 61 36 30 62 65 35 66 32 66 30 01 49 0C 59 00 05 0A 0C 10 01 26 12 49 6D 48 61 70 70 79 54 6F 73 65 65 79 6F 75 E3 82 9B 36 20 38 37 31 66 61 61 30 31 64 30 66 62 36 33 66 31 63 66 31 62 66 64 32 64 33 39 37 35 30 61 34 64 4D 00 00 0E 2B 38 36 00 00 00 00 00 00 00 00 00 00 00 50 01 60 01 70 04 80 0A 92 00 01 21 02 A0 04 B6 0D 69 50 68 6F 6E 65 36 E5 9C A8 E7 BA BF CC DD 00 0C E0 01 FC 0F FC 10 FC 11 F0 12 FF FC 13 FC 14 0B 0A 0C 10 01 26 0F E5 9B BD E6 B0 91 E8 80 81 E7 88 B8 E3 80 82 36 20 61 61 32 64 36 32 64 32 39 31 64 31 32 37 62 36 39 32 32 37 33 63 66 62 62 38 31 39 32 61 31 32 4D 00 00 0E 2B 38 36 00 00 00 00 00 00 00 00 00 00 00 50 01 60 01 70 04 80 0A 92 00 01 22 02 A0 04 B6 12 69 50 68 6F 6E 65 36 20 50 6C 75 73 E5 9C A8 E7 BA BF CC DD 00 0C E0 01 FC 0F F0 10 01 FC 11 FC 12 F0 13 01 FC 14 0B 0A 0C 10 01 26 05 23 EF BD 9E 23 36 20 66 63 39 66 35 61 64 39 32 37 31 64 36 39 34 37 ')

