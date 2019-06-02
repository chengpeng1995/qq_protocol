# -*- coding: utf-8 -*-
import time,re,zlib,wx,traceback
import threading
import random
from mode import PB
from mode import UnProtobuf
from mode import JceFactory
from mode import JceOutput as out
from mode import Packet
from mode import UnPacket
from Tools import Coder
from Tools import MD5
from Tools import TEA
from Tools import HexPacket
from Tools import Img
import Keys
from Tlv import Tlv
from RawSocket import RawSocket
import config,socket
# import wx.lib.pubsub as pubsub
class AndroidQQ:
    '''android qq'''
    def __init__(self, qqnum, qqpwd,window):

        self.window = window
        # self.ipserver = socket.gethostbyname('msfwifi.3g.qq.com')
        self.ipserver = '14.215.138.105'

        self.socket = RawSocket(self.ipserver,8080)
        if not self.socket.connect():
            raise Exception('socket connect error!')
        #QQ
        self.Addvalidation = '你好！' #好友添加验证
        self.qqnum = qqnum
        self.qqpwd = qqpwd
        self.vcode = ''
        self.qqHexstr = Coder.str2hexstr(qqnum)
        self.pwdMd5 = MD5.md5_hex(qqpwd)
        self.uin = Coder.qqnum2hexstr(qqnum)
        self.HEART_INTERVAL = 3*60 #心跳时间间隔 如果在手机QQ上注销/退出帐号后，一般10分钟左右您的QQ号就不会显示在线了
        self.server_time = Coder.num2hexstr(int(time.time()), 4)
        self.alive = False
        self.verify = False
        self.addfriendlist = []
        self.friendMsgIDList = []
        self.GroupMsgIDList = []
        #Android
        self.seq = 10000
        self.appId = Coder.num2hexstr(537042771, 4)
        self.extBin = Coder.trim('')
        self.msgCookies = Coder.trim('F9 83 8D 80')
        self.msgCookies2 = Coder.trim('B6 CC 78 FC')
        self.imei = Coder.str2hexstr('866413457644252')
        self.ksid = Coder.trim('93 AC 68 93 96 D5 7E 5F 94 96 B8 15 36 AA FE 91')
        self.extBin = Coder.trim('')
        self.ver = Coder.str2hexstr('5.8.0.157158')
        self.os_type = Coder.str2hexstr('android')
        self.os_version = Coder.str2hexstr('4.4.4')
        self.network_type = Coder.str2hexstr('')
        self.sim_operator_name = Coder.str2hexstr('CMCC')
        self.apn = Coder.str2hexstr('wifi')
        self.device = Coder.str2hexstr('Lenovo A820t')
        self.device_product = Coder.str2hexstr('Lenovo')
        self.package_name = Coder.str2hexstr('com.tencent.mobileqq')
        self.wifi_name = Coder.str2hexstr('OOOOOOOOO')

        #cmd
        self.loginCmd = Coder.str2hexstr('wtlogin.login')

        #Keys
        self.defaultKey = '00'*16
        self.randomKey = Coder.genBytesHexstr(16)
        self.keyId = random.randint(0, len(Keys.pubKeys)-1)
        self.pubKey = Keys.pubKeys[self.keyId]
        self.shareKey = Keys.shareKeys[self.keyId]
        self.pwdKey = Coder.hash_qqpwd_hexstr(qqnum, qqpwd)
        self.tgtKey = Coder.genBytesHexstr(16)
        self.sessionKey = ''
        self.qqkey = ''
        #debug
        print 'uin: ', self.uin
        print 'pwdMd5: ', self.pwdMd5
        print 'randomKey: ', self.randomKey
        print 'pubKey: ', self.pubKey
        print 'shareKey: ', self.shareKey
        print 'pwdKey: ', self.pwdKey
        print 'tgtKey: ', self.tgtKey
    def FunSend(self,value):

        self.socket.sendall(value)
        self.seq += 1

    def Fun_recv(self):
        list = []
        ret = self.socket.recv()

        if ret:
            if ret == '0':
                return
            try:
                retdata = Coder.str2hexstr(ret)
                while retdata:
                    n = retdata[:8]
                    long = Coder.hexstr2num(n)*2
                    list.append(retdata[:long])
                    retdata = retdata[long:]
                    for item in list:
                        qq = self.qqHexstr+'(.*)'
                        data1 = re.findall(qq,item)[0]

                        data = TEA.detea_hexstr(data1,self.qqkey)
                        pack = HexPacket(data)
                        head = pack.shr(Coder.hexstr2num(pack.shr(4))-4)
                        body = pack.remain(1)

                        #head
                        pack = HexPacket(head)
                        Coder.hexstr2num(pack.shr(4)) #seq
                        pack.shr(4)
                        pack.shr(Coder.hexstr2num(pack.shr(4))-4)
                        cmd = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(4))-4)) #cmd

                        print '##################',cmd,'#####################'
                        pack.shr(Coder.hexstr2num(pack.shr(4))-4)


                        self.unpack(cmd,body)
            except:
                traceback.print_exc()
        else:
            print '返回包为空'











    def unpack(self,cmd,data):
        if cmd == 'OidbSvc.0x7a2_0':
            pass
        elif cmd == 'StatSvc.register':
            print '上线成功！'
            wx.CallAfter(self.window.log,u'['+self.qqnum+u']--登录成功！')
        elif cmd == 'StatSvc.get':
            print '心跳包'
            wx.CallAfter(self.window.log,u'心跳包')
        elif cmd == 'ConfigPushSvc.PushDomain':
            print data
        elif cmd == 'ConfigPushSvc.PushReq':
            pass
        elif cmd == 'MessageSvc.PushNotify':
            print '您有新的消息'
            self.getmessage()
            #wx.CallAfter(self.window.log,u'你有新的消息')
            #self.FunSend(Coder.hexstr2str(self.Pack_MessageSvc_offlinemsg(296603528,'123')))
        elif cmd == 'MessageSvc.PushReaded':
            print '在其他地方查看此消息了'
            #wx.CallAfter(self.window.log,u'在其他地方查看此消息了')
        elif cmd == 'friendlist.getFriendGroupList':
            print data
            list = UnPacket.Un_friendlistgetFriendGroupList(data)
            self.friendlist = list
            wx.CallAfter(self.window.log,u'################'+u'共获取到'+str(len(self.friendlist))+u'个好友'+u'################')
            print '################','共获取到'+str(len(self.friendlist))+'个好友','################'
            for item in self.friendlist:
                a =  u'qq号 :“'+str(item['friendUin'])+u'”   昵称 :“'+item['name']+u'”'
                wx.CallAfter(self.window.log,a)
        elif cmd == 'OnlinePush.PbC2CMsgSync':
            print data
        elif cmd == 'MessageSvc.PbGetMsg':
            print data

            Msglist = UnProtobuf.UnMessageSvcPbGetMsg(data)
            for item in Msglist:
                if not item['MsgID'] in self.friendMsgIDList:
                    self.Msgprocessing(item)
                    self.friendMsgIDList.append(item['MsgID'])

        elif cmd =='OnlinePush.PbPushGroupMsg':

            dict = UnProtobuf.UnOnlinePushPbPushGroupMsg(data)
            if not dict['MsgID'] in self.GroupMsgIDList:
                self.GroupMsgIDList.append(dict['MsgID'])
                wx.CallAfter(self.window.log,str(dict['groupQQ'])+u'['+dict['groupnickname']+u']'+u'-群消息：'+str(dict['targetQQ'])+u'['+dict['targetnickname']+u']'+u'说：'+dict['message'])
        elif cmd == 'MessageSvc.offlinemsg':
            print '发送成功'
        elif cmd == 'FriendList.GetTroopListReqV2':
            self.GroupInfoLsit = UnPacket.Un_FriendListGetTroopListReqV2(data)
            print self.GroupInfoLsit
            a =  u'################ 共获取到'+str(len(self.GroupInfoLsit))+u'个群 ################'
            print a
            wx.CallAfter(self.window.log,a)
            for item in self.GroupInfoLsit:
                retmsg =  u'qq群号：“'+str(item['GroupNumber'])+u'”  qq群名称：“'+str(item['GroupName'])+u'”  qq群Code：“'+str(item['GroupCode'])+u'”'
                print retmsg
                wx.CallAfter(self.window.log,retmsg)
        elif cmd == 'friendlist.getUserAddFriendSetting':
            print data
            [my_qqnumber,add_qqnumber,verify_type,question] = UnPacket.Un_Pack_RequestPacket(data)
            if verify_type == 0 or verify_type == 1:
                req = Packet.Pack_AddFriendReq(self,my_qqnumber,add_qqnumber,verify_type,self.Addvalidation)
                self.FunSend(Coder.hexstr2str(req))
            elif verify_type == 3:
                print '问题：'+question
                wx.CallAfter(self.window.log,u'需要回答问题：'+question)
            elif verify_type == 101:
                print '已经是好友了'
                wx.CallAfter(self.window.log,u'已经是好友了')
        elif cmd == 'SQQzoneSvc.getApplist':
            value = re.findall('73745d0001(.*?)6d0001',data)
            if value:
                print 'ret:',value
            else:
                print '目标设置了访问权限'
        elif cmd == 'friendlist.getTroopMemberList':
            print data
            self.GroupMemberInfo = UnPacket.Un_friendlistgetTroopMemberList(data)
            a = u'################'+u'共获取到'+str(len(self.GroupMemberInfo))+u'个成员'+u'################'
            wx.CallAfter(self.window.log,a)
            for item in self.GroupMemberInfo:
                Member = u'成员QQ号：“'+str(item['GroupMemberNumber'])+u'” 年龄：“'+str(item['GroupMemberAge'])+u'” 性别：“'+str(item['GroupMemberGender'])+u'” 成员昵称：“'+item['GroupMemberNickName']+u'” 成员备注名：“'+item['GroupMemberRemarkName']+u'”'
                wx.CallAfter(self.window.log,Member)
        elif cmd == 'EncounterSvc.ReqGetEncounter':
            PeopleNearbyList = UnPacket.Un_EncounterSvcReqGetEncounter(data)
        elif cmd == 'ProfileService.ReqBatchProcess':
            pbdata = UnPacket.Un_ProfileServiceReqBatchProcess(data)
            retdata = UnProtobuf.UnGroupManager(pbdata)
            FounderQQ = retdata['FounderQQ']
            print '群主QQ：'+FounderQQ
            ManagerQQList = retdata['ManagerQQList']
            print '管理员QQ:'
            for item in ManagerQQList:
                print item
        elif cmd == 'OnlinePush.ReqPush':
            dict = UnPacket.Un_friendlistSetGroupReq(data)
            if dict:
                id = dict['id']
                pbdata = dict['pbdata']
                code = dict['code']
                req = Packet.Pack_OnlinePushRespPush(self,id,pbdata,code)
                self.FunSend(Coder.hexstr2str(req))

        else:
            print data
    def online(self):

        self.FunSend(Coder.hexstr2str(self.Pack_OidbSvc_0x7a2_0()))
        self.Fun_recv()

        self.FunSend(Coder.hexstr2str(self.Pack_StatSvc_Register(self.qqnum,7,11,0)))
        self.Fun_recv()

    def login(self, verifyCode=None):
        '''登录'''
        #发送登录请求
        packet = ''
        #包头
        packet += Coder.trim('00 00 00 08 02 00 00 00 04 00')
        packet += Coder.num2hexstr(len(self.qqHexstr)/2+4, 4)
        packet += self.qqHexstr
        #TEA加密的包体
        packet += self.packSendLoginMessage(verifyCode)


        #总包长
        packet = Coder.num2hexstr(len(packet)/2+4, 4) + packet
        #发送请求
        self.FunSend(Coder.hexstr2str(packet))
        #接收请求
        ret = self.socket.recv()
        print 'abc:',Coder.str2hexstr(ret)
        pack = HexPacket(Coder.str2hexstr(ret))
        #返回包头
        pack.shr(4)
        pack.shr(8)
        pack.shr(2 + len(self.qqHexstr)/2)
        #返回包体

        self.unpackRecvLoginMessage(pack.remain())

        if self.alive:

            self.Start()

             #心跳
            return True
        elif self.verify: #需要验证码
            pass
        else:
            return False
    def unpackRecvLoginMessage(self, data):
        data = TEA.detea_hexstr(data, self.defaultKey)
        print 'undata:',data
        pack = HexPacket(data)
        head = pack.shr(Coder.hexstr2num(pack.shr(4))-4)
        body = pack.remain(1)
        #head
        pack = HexPacket(head)
        Coder.hexstr2num(pack.shr(4)) #seq
        pack.shr(4)
        pack.shr(Coder.hexstr2num(pack.shr(4))-4)
        Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(4))-4)) #cmd
        pack.shr(Coder.hexstr2num(pack.shr(4))-4)
        #body
        pack = HexPacket(body)
        pack.shr(4 + 1 + 2 + 10 + 2)
        retCode = Coder.hexstr2num(pack.shr(1))
        if retCode == 0: #登录成功
            self.unpackRecvLoginSucceedMessage(pack.remain())
            print u'登录成功: ', self.nickname
            print 'qqkey',self.qqkey
            self.alive = True
            self.verify = False
        elif retCode == 2: #需要验证码
            self.unpackRecvLoginVerifyMessage(pack.remain())
            print self.verifyReason
            self.alive = False
            self.verify = True
            print self.verifyPicHexstr
            code = self.window.SetVerification(self.verifyPicHexstr)
            print code
            self.login(Coder.str2hexstr(code))
        else: #登录失败
            pack = HexPacket(TEA.detea_hexstr(pack.remain(), self.shareKey))
            pack.shr(2 + 1 + 4 + 2)
            pack.shr(4) #type
            title = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(2))))
            msg = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(2))))
            print title, ': ', msg
            self.alive = False
            self.verify = False

    def unpackRecvLoginVerifyMessage(self, data):
        data = TEA.detea_hexstr(data, self.shareKey)
        pack = HexPacket(data)
        pack.shr(3)
        tlv_num = Coder.hexstr2num(pack.shr(2))
        for i in xrange(tlv_num):
            tlv_cmd = pack.shr(2)
            tlv_data = pack.shr(Coder.hexstr2num(pack.shr(2)))
            self.decodeTlv(tlv_cmd, tlv_data)
    def unpackRecvLoginSucceedMessage(self, data):
        data = TEA.detea_hexstr(data, self.shareKey)
        print 'shareKeydecode:',data
        pack = HexPacket(data)
        pack.shr(2 + 1 + 4)
        print 'adata',data
        data = pack.shr(Coder.hexstr2num(pack.shr(2)))

        #TLV解包
        print 'adata',data
        data = TEA.detea_hexstr(data, self.tgtKey)
        pack = HexPacket(data)
        tlv_num = Coder.hexstr2num(pack.shr(2))
        for i in xrange(tlv_num):
            tlv_cmd = pack.shr(2)
            tlv_data = pack.shr(Coder.hexstr2num(pack.shr(2)))
            self.decodeTlv(tlv_cmd, tlv_data)
    def decodeTlv(self, cmd, data):
        if cmd == Coder.trim('01 6A'):
            pass
        elif cmd == Coder.trim('01 06'):
            pass
        elif cmd == Coder.trim('01 0C'):
            pass
        elif cmd == Coder.trim('01 0A'):
            self.token004c = data
            print self.token004c
        elif cmd == Coder.trim('01 0D'):
            pass
        elif cmd == Coder.trim('01 14'):
            pack = HexPacket(data)
            pack.shr(6)
            self.token0058 = pack.shr(Coder.hexstr2num(pack.shr(2)))
            print self.token0058
        elif cmd == Coder.trim('01 0E'):
            self.mst1Key = data
        elif cmd == Coder.trim('01 03'):
            self.stweb = data
        elif cmd == Coder.trim('01 1F'):
            pass
        elif cmd == Coder.trim('01 38'):
            pass
        elif cmd == Coder.trim('01 1A'):
            pack = HexPacket(data)
            pack.shr(2 + 1 + 1)
            self.nickname = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(1))))
        elif cmd == Coder.trim('01 20'):
            self.skey = data
            print self.skey
        elif cmd == Coder.trim('01 36'):
            self.vkey = data
            print self.vkey
        elif cmd == Coder.trim('01 1A'):
            pass
        elif cmd == Coder.trim('01 20'):
            pass
        elif cmd == Coder.trim('01 36'):
            pass
        elif cmd == Coder.trim('03 05'):
            self.sessionKey = data
            self.qqkey = self.sessionKey
        elif cmd == Coder.trim('01 43'):
            self.token002c = data
            print self.token002c
        elif cmd == Coder.trim('01 64'):
            self.sid = data

        elif cmd == Coder.trim('01 18'):
            pass
        elif cmd == Coder.trim('01 63'):
            pass
        elif cmd == Coder.trim('01 30'):
            pack = HexPacket(data)
            pack.shr(2)
            self.server_time = pack.shr(4)
            self.ip = Coder.hexstr2ip(pack.shr(4))
        elif cmd == Coder.trim('01 05'):
            pack = HexPacket(data)
            self.verifyToken1 = pack.shr(Coder.hexstr2num(pack.shr(2)))
            self.verifyPicHexstr = pack.shr(Coder.hexstr2num(pack.shr(2)))

        elif cmd == Coder.trim('01 04'):
            self.verifyToken2 = data
        elif cmd == Coder.trim('01 65'):
            pack = HexPacket(data)
            pack.shr(4)
            title = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(1))))
            msg = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(4))))
            self.verifyReason = title + ": " + msg
        elif cmd == Coder.trim('01 08'):
            self.ksid = data
        elif cmd == Coder.trim('01 6D'):
            self.superKey = data
        elif cmd == Coder.trim('01 6C'):
            self.psKey = data
        else:
            print 'unknown tlv: '
            print cmd, ': ', data
    def packSendLoginMessage(self, verifyCode=None):
        #MessageHead
        msgHeader = ''
        msgHeader += Coder.num2hexstr(self.seq, 4)
        msgHeader += self.appId
        msgHeader += self.appId
        msgHeader += Coder.trim('01 00 00 00 00 00 00 00 00 00 00 00')
        msgHeader += Coder.num2hexstr(len(self.extBin)/2+4, 4) + self.extBin
        msgHeader += Coder.num2hexstr(len(self.loginCmd)/2+4, 4) + self.loginCmd
        msgHeader += Coder.num2hexstr(len(self.msgCookies)/2+4, 4) + self.msgCookies
        msgHeader += Coder.num2hexstr(len(self.imei)/2+4, 4) + self.imei
        msgHeader += Coder.num2hexstr(len(self.ksid)/2+4, 4) + self.ksid
        msgHeader += Coder.num2hexstr(len(self.ver)/2+2, 2) + self.ver
        msgHeader = Coder.num2hexstr(len(msgHeader)/2+4, 4) + msgHeader
        #Message
        msg = ''
        msg += Coder.trim('1F 41')
        msg += Coder.trim('08 10 00 01')
        msg += self.uin
        msg += Coder.trim('03 07 00 00 00 00 02 00 00 00 00 00 00 00 00')
        if self.pubKey:
            ext_bin_null = False
            msg += Coder.trim('01 01')

        else:
            msg += Coder.trim('01 02')
            ext_bin_null = True
        msg += self.randomKey
        msg += Coder.trim('01 02')
        msg += Coder.num2hexstr(len(self.pubKey)/2, 2)

        if ext_bin_null:
            msg += Coder.trim('00 00')
        else:
            msg += self.pubKey
        #TEA加密的TLV

        msg += self.packSendLoginTlv(verifyCode)
        msg += Coder.trim('03')
        msg = Coder.num2hexstr(len(msg)/2+2+1, 2) + msg
        msg = Coder.trim('02') + msg
        msg = Coder.num2hexstr(len(msg)/2+4, 4) + msg

        packet = msgHeader + msg
        packet = TEA.entea_hexstr(packet, self.defaultKey)

        return packet
    def packSendLoginTlv(self, verifyCode=None):
        if verifyCode == None:
            tlv = ''
            tlv += Coder.trim('00 09')
            tlv += Coder.trim('00 14') #tlv包个数
            #tlv组包
            tlv += Tlv.tlv18(self.uin)
            tlv += Tlv.tlv1(self.uin, self.server_time)
            tlv += Tlv.tlv106(self.uin, self.server_time, self.pwdMd5, self.tgtKey, self.imei, self.appId, self.pwdKey)
            tlv += Tlv.tlv116()
            tlv += Tlv.tlv100()
            tlv += Tlv.tlv107()
            tlv += Tlv.tlv144(self.tgtKey, self.imei, self.os_type, self.os_version, self.network_type, self.sim_operator_name, self.apn, self.device, self.device_product)
            tlv += Tlv.tlv142(self.package_name)
            tlv += Tlv.tlv145(self.imei)
            tlv += Tlv.tlv154(self.seq)
            tlv += Tlv.tlv141(self.sim_operator_name, self.network_type, self.apn)
            tlv += Tlv.tlv8()
            tlv += Tlv.tlv16b()
            tlv += Tlv.tlv147()
            tlv += Tlv.tlv177()
            tlv += Tlv.tlv187()
            tlv += Tlv.tlv188()
            tlv += Tlv.tlv191()
            tlv += Tlv.tlv194()
            tlv += Tlv.tlv202(self.wifi_name)
            tlv = TEA.entea_hexstr(tlv, self.shareKey)
            return tlv
        else:
            tlv = ''
            tlv += Coder.trim('00 02')
            tlv += Coder.trim('00 04')
            #tlv组包
            tlv += Tlv.tlv2(verifyCode, self.verifyToken1)
            tlv += Tlv.tlv8()
            tlv += Tlv.tlv104(self.verifyToken2)
            tlv += Tlv.tlv116()
            tlv = TEA.entea_hexstr(tlv, self.shareKey)
            return tlv
    def Pack_StatSvc_Register(self,Uin,Bid,Status,timeStamp):

        data = JceFactory.Write_SvcReqRegister(Uin,Bid,Status,timeStamp)

        bin = out.WriteJceStruct(Coder.hexstr2str(data),0)

        map = config.JceMap()
        map.key_type = config.TYPE_STRING1
        map.value_type = config.TYPE_SIMPLE_LIST
        map.key = "SvcReqRegister"
        map.value = Coder.hexstr2str(bin)
        value = out.WriteMap(map,0)
        bin = self.Write_RequestPacket(3,0,'PushService','SvcReqRegister',Coder.hexstr2str(value))
        aaa = self.Make_login_sendSsoMsg('StatSvc.register',bin)

        return self.pack(aaa,1)
    def Write_RequestPacket(self,Version,RequestId,ServantName,FuncName,Bin):


        data = ''
        data += out.WriteShort(Version,1)
        data += out.WriteShort(0, 2)
        data += out.WriteShort(0, 3)
        data += out.WriteInt(RequestId, 4)
        data += out.WriteStringByte(ServantName, 5)
        data += out.WriteStringByte(FuncName, 6)
        data += out.WriteSimpleList(Bin, 7)
        data += out.WriteInt(0, 8)
        data += Coder.trim('98 0C')
        data += Coder.trim('A8 0C')
        print 'test:',data
        return data
    def Make_login_sendSsoMsg(self,cmd,bin):
        #MessageHead
        cmd = Coder.str2hexstr(cmd)
        msgHeader = ''
        msgHeader += Coder.num2hexstr(self.seq, 4)
        msgHeader += self.appId
        msgHeader += self.appId
        msgHeader += Coder.trim('01 00 00 00 00 00 00 00 00 00 00 00')
        msgHeader += Coder.num2hexstr(len(self.token004c)/2+4, 4) + self.token004c
        msgHeader += Coder.num2hexstr(len(cmd)/2+4, 4) + cmd
        msgHeader += Coder.num2hexstr(len(self.msgCookies2)/2+4, 4) + self.msgCookies2
        msgHeader += Coder.num2hexstr(len(self.imei)/2+4, 4) + self.imei
        msgHeader += Coder.num2hexstr(len(self.ksid)/2+4, 4) + self.ksid
        msgHeader += Coder.num2hexstr(len(self.ver)/2+2, 2) + self.ver
        Header = Coder.num2hexstr(len(msgHeader)/2+4, 4) + msgHeader


        body = Header+Coder.num2hexstr(len(bin)/2+4, 4)+bin
        data = TEA.entea_hexstr(body,self.qqkey)
        return data
    def Pack_OidbSvc_0x7a2_0(self):
        bin = Coder.trim('08 A2 0F 10 00 18 00 22 02 08 00')
        data = self.Make_login_sendSsoMsg('OidbSvc.0x7a2_0',bin)
        pack = self.pack(data,1)
        return pack
    def pack(self,bin,type):
        req = ''
        if type == 0:
            req += Coder.trim('00 00 00 08 02 00 00 00 04')
        elif type == 1:
            req += Coder.trim('00 00 00 08 01 00 00')
            req += Coder.num2hexstr(len(self.token002c)/2+4,2) + self.token002c
        else:
            req += Coder.trim('00 00 00 09 01')
            req += Coder.num2hexstr(self.seq, 4)
        req += Coder.trim('00 00 00')
        req += Coder.num2hexstr(len(self.qqHexstr)/2+4,2)
        req += self.qqHexstr

        req += bin
        data = Coder.num2hexstr(len(req)/2+4,4) + req
        return data
    def Pack_StatSvc_get(self):
        msg = ''
        msg += out.WriteInt(self.qqnum, 0)
        msg += out.WriteByte(7, 1)
        msg += out.WriteStringByte('', 2)
        msg += out.WriteByte(11, 3)
        msg += out.WriteByte(0, 4)
        msg += out.WriteByte(0, 5)
        msg += out.WriteByte(0, 6)
        msg += out.WriteByte(0, 7)
        msg += out.WriteByte(0, 8)
        msg += out.WriteByte(0, 9)
        msg += out.WriteByte(0, 10)
        msg += out.WriteByte(0, 11)
        return msg

    def startHeart(self):

        #''开始心跳'''
        while True:
            self.FunSend(Coder.hexstr2str(self.HeartMessage()))
            time.sleep(self.HEART_INTERVAL)

    def HeartMessage(self):
        msg = self.Pack_StatSvc_get()
        data = self.Make_sendSsoMsg('StatSvc.get',self.Pack_sendSsoMsg_simple(msg))

        Heart = self.pack(data,2)
        return Heart

    def Pack_sendSsoMsg_simple(self,bin):


        msg = ''
        msg += out.WriteJceStruct(Coder.hexstr2str(bin),0) ##十六进制转换字符串

        map = config.JceMap()
        map.key_type = config.TYPE_STRING1
        map.value_type = config.TYPE_SIMPLE_LIST
        map.key = 'SvcReqGet'
        map.value = Coder.hexstr2str(msg)##十六进制转换字符串
        value = out.WriteMap(map,0)

        data = ''
        data += self.Write_RequestPacket(3,1819559151,'PushService','SvcReqGet',Coder.hexstr2str(value))
        reee = Coder.num2hexstr(len(data)/2+4,4) + data
        return reee
    def Make_sendSsoMsg(self,cmd,bin):
        serviceCmd = Coder.str2hexstr(cmd)
        msg = ''
        msg += Coder.num2hexstr(len(serviceCmd)/2+4,4) + serviceCmd
        msg += Coder.num2hexstr(len(self.msgCookies2)/2+4,4)+self.msgCookies2

        data = ''
        data += Coder.num2hexstr(len(msg)/2+4,4) + msg
        data += bin
        value = TEA.entea_hexstr(data,self.qqkey)
        return value
    def Start(self):
        self.online()
        threading.Thread(target=self.startHeart).start() #心跳
        self.getFriendGroupList()
        print 'group-----------------------'
        self.getGroupList()

        while True:
            self.Fun_recv()
            time.sleep(1)






    def getFriendGroupList(self):
        value = Packet.Pack_friendlist_getFriendGroupList(self,0,20)
        self.FunSend(Coder.hexstr2str(value))

    def getmessage(self):
        k = '00000023000000174d6573736167655376632e50624765744d73670000000854e96b10'
        pb = k + PB.getmsg()+'01'
        body = TEA.entea_hexstr(pb,self.qqkey)
        value = self.pack(body,2)
        self.FunSend(Coder.hexstr2str(value))
    def GetQzoneAppList(self,targetQQ):
        data = Packet.Pack_QzoneNewService_getApplist(self,targetQQ)
        self.FunSend(Coder.hexstr2str(data))
    def getGroupList(self):
        """
        获取群列表
        """
        req = Packet.Pack_FriendListService_GetTroopListReqV2(self)
        self.FunSend(Coder.hexstr2str(req))

    def sendMsg(self,qqnumber,text):
        data = Packet.Pack_MessageSvc_offlinemsg(self,qqnumber,text)
        self.FunSend(Coder.hexstr2str(data))

    def Addfriend(self,addqqnum,msg):
        self.Addvalidation = msg
        data = Packet.Pack_friendlist_getUserAddFriendSetting(self,addqqnum)
        self.FunSend(Coder.hexstr2str(data))
    def AddGroup(self,addgroupnum,msg):
        data = Packet.Pack_ProfileService_GroupMngReq(self,addgroupnum,msg)
        self.FunSend(Coder.hexstr2str(data))
    def SendGroupMsg(self,qqgroup_number,msg):
        data = Packet.Pack_MessageSvc_SendGroupMsg(self,qqgroup_number,msg)
        self.FunSend(Coder.hexstr2str(data))
    def GetfriendWidget(self):
        data = Packet.Pack_QzoneNewService_getWidget(self)
        self.FunSend(Coder.hexstr2str(data))
    def GetSearchkey(self,key):
        data = Packet.Pack_SummaryCardServantObj_ReqCondSearch(self,key)
        self.FunSend(Coder.hexstr2str(data))
    def SendGroupMemberImageMsg(self,GroupQQ,targetQQ,ImgName,ImgPath):
        #GroupQQ = '574240651'
        #targetQQ = '296603528'
        #ImgName = '936ee06bd035095c991c5a2572614ae4'
        ImaFileName = ImgName +'.jpg'
        #ImgPath = '/7b9da5a3-8b5b-462f-a03c-eb9c6f37ebb8A'
        data = Packet.SendImageMsg(self,GroupQQ,targetQQ,ImgName,ImaFileName,ImgPath)
        self.FunSend(Coder.hexstr2str(data))
    def SendFriendImageMsg(self,targetQQ,ImgName,ImgPath):

        ImaFileName = ImgName+'.jpg'

        data = Packet.SendImageMsg(self,'',targetQQ,ImgName,ImaFileName,ImgPath)
        self.FunSend(Coder.hexstr2str(data))
    def AutoReceiveFriends(self,targetQQ):
        if config.AutoAgreeAddFriend == True:
            data = Packet.Pack_friendlistGetAutoInfoReq(self,targetQQ)
            self.FunSend(Coder.hexstr2str(data))
            time.sleep(1)
            data1 = Packet.Pack_ProfileServicePbReqSystemMsgActionFriend(self,targetQQ)
            self.FunSend(Coder.hexstr2str(data1))
    def AutoReceiveAddGroup(self,targetQQ,GroupNumber):
        if config.AutoAgreeGroup == True:
            # data = Packet.ProfileServicePbReqSystemMsgNewGroup(self)
            # self.FunSend(Coder.hexstr2str(data))
            # data1 = Packet.Pack_GetSimpleInfo(self,targetQQ)
            # self.FunSend(Coder.hexstr2str(data1))
            # data2 = Packet.Pack_ProfileServicePbReqSystemMsgActionGroup(self,targetQQ,GroupNumber)
            # self.FunSend(Coder.hexstr2str(data2))
            data = Packet.Pack_AutoReceiveGroupRequests(self,targetQQ,GroupNumber)
            self.FunSend(Coder.hexstr2str(data))
    def Msgprocessing(self,data):
        if data['MsgType'] == 1:
            retdata = u'“'+str(data['targetQQ'])+u'” 说：“'+data['message']+u'”'
            wx.CallAfter(self.window.log,retdata)
        elif data['MsgType'] == 1001:
            targetQQ = data['targetQQ']
            if not targetQQ in self.addfriendlist:
                self.AutoReceiveFriends(targetQQ)
        elif data['MsgType'] == 2001:
            GroupCode = data['GroupCode']
            targetQQ = data['targetQQ']
            for item in self.GroupInfoLsit:
                if item['GroupCode'] == GroupCode:
                    GroupNumber = item['GroupNumber']
                    self.AutoReceiveAddGroup(targetQQ,GroupNumber)
    def p(self,GroupNumber):
        data = Packet.Pack_FriendListServiceServantObj_GetTroopMemberListReq(self,GroupNumber)
        self.FunSend(Coder.hexstr2str(data))
    def GroupRemovesMember(self,targetQQ,GroupNumber):
        data = Packet.Pack_GroupRemovesMember(self,targetQQ,GroupNumber)
        self.FunSend(Coder.hexstr2str(data))
    def GetNearPeople(self,longitude,latitude):
        long = int(str(longitude*1000000)[:9])
        lat = int(str(latitude*1000000)[:8])
        data = Packet.Pack_EncounterSvc_ReqGetEncounter(self,long,lat)
        self.FunSend(Coder.hexstr2str(data))

    def AddfriendGroup(self,name):
        data = Packet.Pack_friendlistSetGroupReq(self,name)
        self.FunSend(Coder.hexstr2str(data))
    def SetGroupCardName(self,name,groupname):
        data = Packet.Pack_friendlistModifyGroupCardReq(self,name,groupname)
        self.FunSend(Coder.hexstr2str(data))
    def GetGroupInfo(self, GroupNumber):
        data = Packet.Pack_FriendListServiceServantObj_GetTroopMemberListReq(self, GroupNumber)
        self.FunSend(Coder.hexstr2str(data))
    def GetGroupManager(self,GroupNumbar):
        data = Packet.Pack_ProfileServiceReqBatchProcess(self,GroupNumbar)
        self.FunSend(Coder.hexstr2str(data))
    def GetQQnumber(self,phone):
        data = Packet.Pack_SummaryCardReqSummaryCard(self,phone,self.qqnum)
        print data
        self.FunSend(Coder.hexstr2str(data))

