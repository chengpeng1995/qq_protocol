import StringIO
import gzip

from  JceInputpy import JceInputStream
import re,json,zlib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class Un_Pack_Map:
    def __init__(self,data):
        self.dict = {}
        self.data = data
    def Pack(self):
        while self.data:
            self.Map()
    def Decode(self):
        self.Pack()
        return self.dict
    def getHex(self,num):
        data = self.data[:num]
        self.data = self.data[num:]
        return data
    def gethexstr(self,data):
        if len(data) <= 8:
            try:
                return int(data,16)
            except:
                return data.decode('hex')
        else:
            return data.decode('hex')
    def Map(self):
        number = self.gethexstr(self.getHex(1))
        type = self.gethexstr(self.getHex(1))
        if type == 0:
            data = self.getHex(2)
            self.dict[number] = self.gethexstr(data)
        elif type == 12:
            self.dict[number] = ""
        elif type == 2:
            data = self.getHex(8)
            self.dict[number] = self.gethexstr(data)
        elif type == 6:
            long = self.gethexstr(self.getHex(2))
            _long = long*2
            data = self.getHex(_long)
            self.dict[number] = self.gethexstr(data)
        elif type == 13:
            self.getHex(4)
            long = self.gethexstr(self.getHex(4))
            _long = long*2
            data = self.getHex(_long)
            self.dict[number] = data
        elif type == 8:
            data = self.getHex(2)
            self.dict[number] = self.gethexstr(data)
        elif type == 9:
            cont = self.gethexstr(self.getHex(4))
            self.dict[number] = self.data
            self.data = ''

def Map(data):
    try:
        value = re.findall('0a(.*?)0b',data)[0]
        return value
    except:
        return data

def DecodeMap(data):
    p1 = Un_Pack_Map(data)
    p2 = p1.Decode()
    return p2
def FriendGroupList(data):
    list = []
    value = data[7]
    friend_count = data[6]
    jce = JceInputStream(value)
    for item in range(friend_count):
        dict = {}

        jce.getHex(2) #0A
        dict['friendUin'] = jce.ReadNumber()
        dict['groupId'] = jce.ReadByte()
        dict['faceId'] = jce.ReadShort()
        dict['name'] = jce.ReadString()
        dict['sqqtype'] = jce.ReadByte()
        dict['status'] = jce.ReadByte()
        dict['memberLevel'] = jce.ReadByte()
        dict['isMqqOnLine'] = jce.ReadByte()
        dict['sqqOnLineState'] = jce.ReadByte()
        dict['isIphoneOnline'] = jce.ReadByte()
        dict['detalStatusFlag'] = jce.ReadByte()
        dict['sqqOnLineStateV2'] = jce.ReadByte()
        dict['sShowName'] = jce.ReadString()
        jce.ReadByte()
        dict['nickname'] = jce.ReadString()
        jce.getHex(2) #0B

        list.append(dict)
    return list
def AddFriendSetting(data):
    jce = JceInputStream(data)
    my_qqnumber = jce.ReadNumber()
    add_qqnumber = jce.ReadNumber()
    verify_type = jce.ReadByte()
    COUNT = jce.ReadList()
    if COUNT == 1:
        p = jce.data[2:]
        question = jce.ReadString()
    else:
        question = ''
    return [my_qqnumber,add_qqnumber,verify_type,question]
def getk(data):
    if data[:8] == '03000000':
        data = data[8:]
        return data
    else:
        return data


def Un_Pack_RequestPacket(data):
    p1 = DecodeMap(data)
    p2 = p1[7]
    p3 = DecodeMap(p2)
    tag = p3[0]
    value = p3[1]
    if tag == 'FLRESP':
        return FriendGroupList(DecodeMap(value))
    elif tag == 'FSRESP':

        return AddFriendSetting(value)
    elif tag == 'GAIRESP':
        pass
def Un_FriendListGetTroopListReqV2(data):
    GroupInfoList = []
    data = data[8:]
    print data
    jce = JceInputStream(data)
    jce.ReadByte()
    jce.ReadByte()
    jce.ReadByte()
    jce.ReadShort()
    jce.ReadString()
    jce.ReadString()
    jce.getHex(4)
    long = jce.ReadValue()
    jce.data = jce.data[:long*2]
    jce.getHex(6)
    jce.ReadString()

    jce.getHex(4)
    long2 = jce.ReadValue()

    jce.data = jce.data[:long2*2]
    print jce.data

    jce.data =  re.findall('^0a(.*?)0b$',jce.data)[0]
    jce.ReadNumber()
    jce.ReadByte()
    jce.ReadByte()
    jce.ReadByte()
    jce.ReadValue()
    jce.getHex(2)

    cont = jce.ReadValue()
    print cont
    print jce.data
    for item in range(cont):
        jce.ReadValue() #0a
        GroupCode =  jce.ReadValue() #code
        GroupNumber = jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        GroupName = jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue() #0b
        GroupInfoList.append({'GroupCode':GroupCode,'GroupName':GroupName,'GroupNumber':GroupNumber})

    return GroupInfoList
def Un_friendlistgetTroopMemberList(data):
    GroupMemberInfo = []
    data = data[8:]
    jce = JceInputStream(data)
    jce.ReadByte()
    jce.ReadByte()
    jce.ReadByte()
    jce.ReadNumber()
    jce.ReadString()
    jce.ReadString()
    jce.getHex(4)
    LONG = jce.ReadValue()
    jce.data = jce.getHex(LONG*2)
    jce.getHex(6)
    jce.ReadString()
    jce.getHex(4)
    LONG1 = jce.ReadValue()
    jce.data = jce.getHex(LONG1*2)
    jce.data = re.findall('^0a(.*?)0b$', jce.data)[0]
    jce.ReadNumber()
    jce.ReadNumber()
    jce.ReadNumber()
    jce.getHex(2)
    CONT = int(jce.getHex(4),16)
    for item in range(CONT):
        jce.getHex(2) #0A
        GroupMemberNumber = jce.ReadNumber()
        jce.ReadByte()
        GroupMemberAge = jce.ReadByte()
        Gender = jce.ReadByte()
        if Gender == 1:
            GroupMemberGender = 'Female'
        elif Gender == 0:
            GroupMemberGender = 'Male'
        else:
            GroupMemberGender = 'Unknown'
        GroupMemberNickName = jce.ReadString()
        jce.ReadByte()
        jce.ReadString()
        GroupMemberRemarkName = jce.ReadString()
        jce.ReadByte()
        jce.ReadString()
        jce.ReadString()
        jce.ReadString()
        jce.ReadString()
        jce.ReadByte()
        jce.ReadNumber()
        jce.ReadNumber()
        jce.ReadByte()
        jce.ReadByte()
        jce.ReadByte()
        jce.ReadByte()
        jce.ReadByte()
        jce.ReadByte()
        jce.ReadString()
        jce.ReadByte()
        jce.ReadString()
        jce.ReadByte()
        jce.ReadByte()
        jce.getHex(2) #0b
        GroupMemberInfo.append({'GroupMemberNumber':GroupMemberNumber,'GroupMemberAge':GroupMemberAge,'GroupMemberGender':GroupMemberGender,'GroupMemberNickName':GroupMemberNickName,'GroupMemberRemarkName':GroupMemberRemarkName})
    return GroupMemberInfo
def Un_friendlistgetFriendGroupList(data):

    list = []
    data = data[8:]
    jce = JceInputStream(data)
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.getHex(4)
    LONG = jce.ReadValue()
    jce.data = jce.data[:LONG*2]
    jce.getHex(6)
    jce.ReadValue()
    jce.getHex(4)
    LONG1 = jce.ReadValue()
    jce.data = jce.data[:LONG1*2]
    jce.data = re.findall('^0a(.*?)0b$', jce.data)[0]
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    CONT = jce.ReadList()
    for item in range(CONT):
        dict = {}
        jce.ReadValue() #0A
        dict['friendUin'] = jce.ReadValue()
        dict['groupId'] = jce.ReadValue()
        dict['faceId'] = jce.ReadValue()
        dict['name'] = jce.ReadValue()
        dict['sqqtype'] = jce.ReadValue()
        dict['status'] = jce.ReadValue()
        dict['memberLevel'] = jce.ReadValue()
        dict['isMqqOnLine'] = jce.ReadValue()
        dict['sqqOnLineState'] = jce.ReadValue()
        dict['isIphoneOnline'] = jce.ReadValue()
        dict['detalStatusFlag'] = jce.ReadValue()
        dict['sqqOnLineStateV2'] = jce.ReadValue()
        dict['sShowName'] = jce.ReadValue()
        jce.ReadValue()
        dict['nickname'] = jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        CONT1 = int(jce.getHex(4),16)
        for item1 in range(CONT1):
            jce.ReadValue()
            jce.ReadValue()
            jce.ReadValue()
            jce.ReadValue()
            jce.ReadValue()
            jce.ReadValue()
            jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadSimpleList()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        jce.ReadValue()
        list.append(dict)
    return list

def Un_EncounterSvcReqGetEncounter(data):
    list = []
    data = data[8:]
    #print data
    jce = JceInputStream(data)
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    d1 = jce.ReadValue()
    d1 = d1[6:]
    jce_1 = JceInputStream(d1)
    jce_1.ReadValue()
    jce_1.getHex(6)
    jce_1.ReadValue()
    d3 = jce_1.ReadValue()
    jce_2 = JceInputStream(d3)
    jce_2.ReadValue() #0a
    jce_2.ReadValue()
    jce_2.getHex(2)#1A
    jce_2.ReadValue()
    jce_2.ReadValue()
    jce_2.ReadValue()
    jce_2.ReadValue()
    jce_2.ReadValue()
    jce_2.ReadValue()
    jce_2.ReadValue()
    jce_2.getHex(2)#0B
    COUNT = jce_2.ReadValue()
    JCEDATA = JceInputStream(jce_2.data)
    for item in range(COUNT):
        dict = {}
        JCEDATA.ReadValue() #0A
        dict['qq_number'] = JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        dict['timestamp'] = JCEDATA.ReadValue()
        dict['time'] = JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        dict['nickname'] = JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        dict['lat'] = JCEDATA.ReadValue()
        dict['lon'] = JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()#0A
        JCEDATA.getHex(2)
        COUNT1 = int(JCEDATA.getHex(4),16)
        for item1 in range(COUNT1):
            JCEDATA.ReadValue()
            JCEDATA.ReadValue() #0A
            JCEDATA.ReadValue()
            JCEDATA.ReadValue()
            JCEDATA.ReadValue()
            JCEDATA.ReadValue()
            JCEDATA.ReadValue() #0B
        JCEDATA.ReadValue()#0B
        JCEDATA.ReadValue()#0A
        tt = JCEDATA.ReadValue() ##text


        JCEDATA.ReadValue()
        JCEDATA.ReadValue() #0B
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()

        JCEDATA.ReadValue() ##list
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        JCEDATA.ReadValue()
        list.append(dict)
    print json.dumps(list)
    return list
def Un_friendlistSetGroupReq(data):
    data = data[8:]
    jce = JceInputStream(data)
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    req = jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce_1 = JceInputStream(jce.ReadSimpleList())
    jce_1.getHex(6)
    if jce_1.ReadValue() == 'req':
        jce_1.getHex(6)
        jce_1.ReadValue()
        jce_2 = JceInputStream(jce_1.ReadSimpleList())
        jce_2.ReadValue() #0A
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.getHex(6)
        jce_2.ReadValue() #0A
        jce_2.ReadValue()
        jce_2.ReadValue()
        id = jce_2.ReadValue()
        id2 = jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadSimpleList()
        jce_2.ReadValue()
        pbdata = jce_2.ReadSimpleList()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        code = jce_2.ReadValue()
        return {'id':id2,'pbdata':pbdata,'code':code}
    else:
        return False
# #000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bf01401fd1500000908f19ed7598819b817f01601fc17f01801fc19f01a01f61b0ce6898be69cbae59ca8e7babffc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250b0a0211adcf881c2c3602c2a04c50146c7c8c9ca00abcc600dce602c2a0fc0ffd10000cfd11000cf21200012102fa1308000300011a0c1c20063c0b00021a0c1c2c3c0b00031a0c1c20063c0b0bf01401fd1500000a08889fb78d018819b817f01601fc17f01801fc19f01a01f61b0d6950686f6e6536e59ca8e7babffc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250b0a021b5352971c2100bd360ce5a4a7e98193e887b3e7ae804c50146c7c8c9ca0fabcc600dce60ce5a4a7e98193e887b3e7ae80fc0ffd10000cfd11000cf21200011002fa1308000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bfc14fd1500000a0897a5cdda018819b817fc16fc17fc18fc19fc1af61b00fc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250b0a0300000000b942a78e1c21025236022d2d4c50146c7c8c9ca014bcc600d001e6022d2dfc0ffd10000cfd11000cfc12fa1308000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bfc14fd1500000a088ecf8aca0b8819b817fc16fc17fc18fc19fc1af61b00fc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250b8c9001acbcc004d004e900040a0c160ce68891e79a84e5a5bde58f8b200430014c5c0b0a00011606e69c8be58f8b2c3c40015c0b0a00021606e5aeb6e4baba2c3c40025c0b0a00031606e5908ce5ada62c3c40035c0bfc0ffc10f01101f21257fc8caffc13f9140cfc15fc16fa17020b35cf711c2c36012d4c500b6c7c8c9ca00abcc600dce6012dfc0ffd10000cfd11000cf21200010107fa1308000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bf01401fd1500000908f19ed7598819b817f01601fc17f01801fc19f01a01f61b0ce6898be69cbae59ca8e7babffc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250bf0180108
# #000300011a0c1c20063c0b00021a0c1c2c3c0b00031a0c1c20063c0b0bf01401fd1500000a08889fb78d018819b817f01601fc17f01801fc19f01a01f61b0d6950686f6e6536e59ca8e7babffc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250b0a021b5352971c2100bd360ce5a4a7e98193e887b3e7ae804c50146c7c8c9ca0fabcc600dce60ce5a4a7e98193e887b3e7ae80fc0ffd10000cfd11000cf21200011002fa1308000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bfc14fd1500000a0897a5cdda018819b817fc16fc17fc18fc19fc1af61b00fc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250b0a0300000000b942a78e1c21025236022d2d4c50146c7c8c9ca014bcc600d001e6022d2dfc0ffd10000cfd11000cfc12fa1308000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bfc14fd1500000a088ecf8aca0b8819b817fc16fc17fc18fc19fc1af61b00fc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250b8c9001acbcc004d004e900040a0c160ce68891e79a84e5a5bde58f8b200430014c5c0b0a00011606e69c8be58f8b2c3c40015c0b0a00021606e5aeb6e4baba2c3c40025c0b0a00031606e5908ce5ada62c3c40035c0bfc0ffc10f01101f21257fc8caffc13f9140cfc15fc16fa17020b35cf711c2c36012d4c500b6c7c8c9ca00abcc600dce6012dfc0ffd10000cfd11000cf21200010107fa1308000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bf01401fd1500000908f19ed7598819b817f01601fc17f01801fc19f01a01f61b0ce6898be69cbae59ca8e7babffc1cfc1dfc1ef01f01fc20f62100f62200fc23fc24fc250bf01801

#Un_EncounterSvcReqGetEncounter('1111111178da9d9b075c536717c66f1236510cc8143522a25846124202880314ab88880c8b56459688652f47b50d8611642fd944650a22a820230c57b556b4ad6dd56a6dade466d85ad15aaa36eaf7be090ac1d0de2ffc022437516efef739e73ce7bc6fa6e1ad9c5d2d0a55823710dda282a313a31242e3d605eddcaeb77ced8a800fdd7c03dc3c97aff3f3f475f3de40db8fe096d9682078355defd0f8980f4313defd8b0d342304a736fbdd639fa4609bf75f3313c12d3da385f75ff47b8989f4a72eeefaaaefccd4e7bb693a2fc75db9c0423a33591b74051d6582935c6165b2a0aa05edac46bb0e442288c91484683a1777e5d261a433e7b0b3870f02bef212b69222f6695b22142dbcb6fdd7b1a6560c6dca2791640aca491317703d366fd34fc259671d42ea9133c825e41b150132ac837b350d21be22214489ae444f325da2ffd4009ec65343781ec3466f9e18e3ed25262f6768200404674234b572d646f0a3bf09b2dfda2f4da720884ebe0a3c8902e94f02ceda54fbd54c8438320b19998d48c8c3735487cd545ecd4588c3e6f83fe7e11104af95bee294c442325fb2e08925f81b0b9f7c80c30f5b1124d6c336b857b6e0842812ea2b1a38393bf04d47884fed117c2c22618c3091110764c41119714246162112676d2d7c90e02c85a4d36f0630ae614ca1db50ecc0fb4639e5e0e682b46fdea69744446b8f098ff5f0bb33516ece1803dc7b0c86a7bf914168df0121b4b6498c9e1833578f6740569900011e9051d020a83d60d5839bf4ed230b66e0eae63c885dfaa950f28f6ec005d7fa2156d4fabff1d49d4f5fee2d28d1cf31edd0aff9807b3e75d918277589d92826c93c191e892584a362306ca5aa141ce7cbbd4f487a9f0138bf6d82701c1dc7e0e09d366f9b9e44149771d0dc2e3eaf76887500131cc39300ce028d3910ce5cbf313808ce94ac3a918eea5b3af3e534624c065fa2e45226f885b6f2e02f51432a139cc228bc13512ec15db19f3ba6cdf6d8e9ef758afb7551ecf0a0e1b1c70fff2cbeb624d8f5f5f9b5bd3e519b3e7c3a060f376c365531bd3dcad2db3ff7ac0a49ed26a0f7308f41a2da30ed013d075948a119d920aa8c928842ce49013b15ede10ab8ed63fc8893f3d36987e2b26c86fcac3ec71460ba0495616e69da7884a39cbee31dbbf7b4f9efa6fdb70e3bbcf6e6df3eb63c722dbe27c16beba16675965e974b125e6bddc01667ea38910d9be11472522d5496d3d412cecf24f5538093b885a14bb57164024e54da18282fdc36c324ad616e0e8bec19ba273e708c1361724e338b21277635e4b43d1713270739912d4439cd686b37da902728ea1716753ceecd02f7d1da66416586a0aa0e1c11e4e689d30a1ef7268fd2bc1592856864a84a0c4ebdd8c7305fe9a5c7de74496faab8dba8e1c7fb4f5edff8a4caaeda2c52b7e6da184dcdc954a7aaab2c4dca2be61b925613a0290a62e8d26c9830a15199f2b2d314970ea05d2d686a33a6986589214bae3f64e9b37a7ccc4ec391d5e471ca8ec8802e95034ae5f7f4088bb868fd01c1d17ab4f820990c496600b69dc2ba4661790a9a57f219d9c6caeafbfe07acaeeffbadac46b9f22ae3d746ac13d6e99c5b6bd4e23ebb3dfe377b2d0da356a3c3f19e3d4f1ef9ac98fa6b476990dacf0372d1acaa90abe67a65b92e32d25b47d2f086d1ecc920d16ca890abe33bac2ef82a69b1e0f358fc6e8ef878ef102b798c2d7e72b6790f215bab5f205b13897c3e94473b7a448696a8209ae7ecd2f522ebf7d12f1a556e6f36f558fdbde08b370c566ef58dcac18067bf08fff825ab54c792d35535aeb44e5232704c25eb29019e4ecaba820e92ba05aca9c98c29541b87713515af0531697a842690c313c861d1981869de878c7c974246c48f31c5b2223e2f1be70f19096e0ede12d69d2b8d6cc9eef67ecadd9ea8fdbdf94e6f6a23b13377b1ba57eb822f3bd1313ef8c974a452ac747c86dbe2653a1239c3f894ea883a56165c703e90106ee11819d5c9c9687c04c9c4fa49aba90f1632c45118468517ff88df95ed6be53bebe7b3834eec200795ee0483bd413fbcfeb2f7c512329d25fc444b95fbcff331185ac36678190c9c3c0c8d3bcac2b07bb4e91549bb1c06d5591854d2d4cf940faae9496a1f8543e38b29ed2f898240fad220103d44ce7ba94f7417ea6fc5622e97a70cf83d05a28eea616e7e36ccf903a96845f5e3beea516efbcd3ddc59e533769d3ab7a62fb378a565f90ffd562a927bf3bffe7aabffb5a9750e2eebd8d5ba57667df6969b64ce243146481e06ff50196a26f3280412e939a4e6c720d16d1814b954e40199cde077b160be2d2ee377d5c23b87caf95d19e08ea0abebdf8cfc5b90d7d04100d2a24d2c05398429e6361056f1fb0ec344cecd01dd86e0d41190e0c1790832d2c5258dfcae1e01275f905188f6b240f60768c143218f233c764634502aaa4f0698514e9ba8b395df755041f4fa521ad6d89a872539baae3ea43a7cf5e3a5f738abef2ca6aaec23b9e60f7aa8a63aa7ffc25b7a5d75935cf44e525d6d9515acd1599570122107a2f7619028368ed409558009cbab11b05b07157d63217fdde1272861f342485e3becff70788aa89d5faebffde6fca440af2935cf841ab73fbaecf230753312f642f2f7167af3ddf9fb5c5cd2384b2e45b662a1b659596ac61f5bfb9234564187774a9af368131cdee66d0649fa687f09bf2b1b4800284850da0ab48a0eb03179620d96340be220b1a9e409fe44f53d7ff2aeaba011cc61987435c100017fb4e40cca2a13b078e0af0b4a0e8b920f8283a0a9508035bdecd33575cd695368319a268fb5bfe30d4e71af61a8df8ef56d5169babcceed4ec4139796684da1d31856e26469e09eb269c0e51ab795a4e70abb335598061c612561c81712fda419a2947cb4254f54d6273cde08828edf9786d67205190dc22ad63bb83f4dce565004d9968c40b6aa67e4122a61624225bc051b4a70139d6811f2d8a21347504e018cf8864c325978fc380374d3a05d03a10f225e9039007340790ab80ad019e6f044037d8293076407814bcc33a55229768e8e74a6a36308931e62e768ef40a307db51e8148a1d45d7df71ed2dd9f5a8fea6dae7ab86537facf8fc681abad6dd907f294bb5dcf1f7f9718f92b5c32dfe667b645f89b913f8e0c771d65b763d24e6139ccf5c65270973fe22de24691c87a9a118d6321a4daedd73c14fd9bccd38699af510bb1fad6e14b574820bc0ef3d8945e0d75e9e8117619554e02af6d80db8855c61339299d3519967648bd87d425ea1a08a3b2aeadd5b57ce35f53a4fceab7c74e7ec4fce91ab7257aa1a3f6e386accbebffbd9bc8aa81f715d9591f427a96310b54773c5448a845265453d6fb0ff0e49e706a4980f454db19f40f1dc66d00ce2dd5760695cae3df58145ecdc7dc88d90832995ce21e879846f0f2587c793831213c881e4f898c0281b0529405be8fd554aff5de4752f9bbf9573c4fe50ca52ae05e312ed6ebad6f599bbc8e501b7238a67dee8f2f94f23a062aa6c5e5dfc38f31849e72584152f85e538d10818254d1197f78b06d243042575200d6089f88a1228b66b0c080db71a93a7d4f563889c645816af3cbaf4d1d02ec7e5ad2d3e7f9dfbdd6b7d86db70bec16f592b92f11d1b4eef7d14a8c7750e4b59e03e262215c59188bfacac86ec76e89a9254610b2c768303053ad410953e3133ea0b0ea58b327ad0967a71f1c083d26af1911e701bd395fae488f42f4044ae5910113e0d93ae3612d6a07d85c01fa1958da3ce481a8d686e2b9f5787d69e04d9ef5d0d82beb3ed242c82e0f5d2e429cae904f5117a2be943057a9cf1c63ce068a7fad2696a455b70eb666f99ade7b5d82378903bc8ae402a9233fad977aaa71cb0bc495534f39a60e8711b954d823a294223920aac490febe0cc4baac809e1ab9ba4b6cad7f7416523a6d983d56e88daa211a2de9127577ff013eb0ffe2decb9047d704df9dda9322b4fa652409107771460cbf0a392a3d0568bef93a99f9eb8b130b7e143e7b35fa9c5ccecf4d7f04e7c7d89e9326cbae5d697df7c2bd7074d51884de799b281ecf6c72b5d12a11460135a327481ad84b58366374eb15e5e38e0ea3537f9f9faba7993c90b31f9a2056f203be7eb90dd96f59864ba9e40254ff812724ef27987f8bce3631689930f1ea2ec5c41d511616609acd24c3b9a238566ef406784863298f6f6810e76f614070ac5317894f3d25ac37bc53a8662b75fbdfb1b2cbe0dd9a24d484edf62bb801c6e73f83a63ee2276af674743f325e11867c23bce138de85665397f62aad74452f5029c8b6da13ced1852cbd4960bdf179467bf743a81e69e111c6f403bdb312994da0f294ff795183d35469037bfff6b797e7b4846db9230834c16751c05095ad45f087e92813d83d981550c1e28506bb07991fd83a9cf07cfd236a65ddcf3177bc8f8e077891fb5ad8ea59f9f2959d7763ef8d5cf05d3b42b09ff5974745d9465e8f857e7080907c7dadfd7c316882e1dd78e3184c9757a92aa8f9b8f87df183fed7fe977f420bf950c19bf4626b6592d61219a97223cc943cb1af9dd7928b71b184e7e578eb88885169d80cde5714035072d6814b51e550072e89c6e4118ed704f0bc3a13269730d8dbebb7af8fc974edf1497c6f2e66c3f7435e7d6d0ae59dd64546e196a548e047994fa29caa20c706c3f45523d0450defc13ca916e278f125a46a3245d611a57702003449fb82c0bd864d0ac601a852c74875c0da2645c6bb7fc1fbab496f38db34115029d99201d1a7359df0e1fb29ac0f1c7bdc95aa348bd1fb1af9a5f71d97ee44d5e41b8d5acbe670b4d2e985c5ba3517a5b3cfb4cd38c0b31b7a60c1e7a9e74452e932a5e4c98ce5516e98295614b650dfabea0770d3af31d5269a7a903de00a8c2685da6e050097803d854da22edcaeb612efd743d760b6e42200ad8a7859599fcae4c71459302290efafd9494d23627b25c7f61fb4897fe2567ba28f5758f855de3e7925c6f955d8946ccf6eaaa33e53b306446ad3a65b979659269243c9c299dc887dc983033d2c749711e2840a424a290dd02ea8128bd49587412d3ecd62616725b321f728ba561ec1f0d099a6861bdac782b20f6e3dc9fbe7c70dae84648eedf2ab7331877cfe872e736f5dcd1e8eebd1c98e11f4be471cd6a977f77ebd8fb597042c5d6325696973bfdaa2649a512f0baff37f4985407c86bdc2408771f96127d51672b68b7c5bcfc07c52d686a06e8baf83d27b0b8707f3fc8cdc81a725b6785d1f7900804109f8a88199d372bd775b9e864b242dfdc72f099da17ab2c77e6afa67ebebbc047fda577e79b6fcdac7ddd45c572e94e53a1c6d4772acbccf078720d49a51e30ab2981e98e0acda1fd388d95c8d6a6d2f305958dc2c34598b2dcea7469f52d859cd6ee577a6d408cb69ebee6bd9ff88753fb8a656b8d1feff18ebb9632fbc783815b929d1fe2f4fc8a9266b4ff64f0eb8f8a92d7847a30ad4b5940b34a9f1f26111602408d1760103a50e5831077156a4a8d3f5082b506d82e877418c190ce87224c742ce572ff0c71b9f4af73d205d947c5cda5685a275a90256695085a8b46d139fe7d0e39179fd6f9a06ee3225ecba295fbddb7bbad7e1a9e72ee6bd6aa0fc95a1106c7482fac36977e8c217f112b944677847281a46202d0dd3197361ef672a5741941ba5b01745ad0cd7667a279d998b2979374b2387333e4e7aa2abf3a37f97a025d0ea1c5681337c0063d1d5ad74796951fd14099b025033e57512da8aa7b5b45bfaddbb570697a88ff45ab7dbb7b377ec1c9159e1808bd4bbb2e5e2efcf983e7d40c8a0d19cd88345a2117a98aaba83a41e931f78bc2e7247c12a0790d0f85c880c684365645412dd04b22c42746616a43681110e28a70e97e180e26112e2098bc6d3f64b506b81f617287b8e580e279ecfaca3f0f112eb946f0ae16b077d0f47e351821310217c7d41d70eee0ecf1c8ac51bf9863aaf651f9e571f3d8510dbe3776a85176ece039921f4022c40068156dd2e875904f6fd21e6e5a12dec3668c9aeee4d428f6909aad03a4661787899a17c155c60c3ab4de7261c65170139d68e3f7e5ca166644295da3fe0d3c9b9b2d6057c2e3bc32d8d9b1aad0810ec5740d0ed532f7eaee35ab6ab8746cff5ace13d7b5d729a535cd57ad3e73d28bf865bb68eb67fd5a4d3f6fae7a9fee7b9a541eaf4be4c63d24029caff65a4a9d1d1de0b51b8b706b981b8dc56579e2f45c610667989b9f31c4ca131675825c39c4cac7a454cb179039d31832a779625df44293cb65cb0882be74417b01f0c6e29a1c414732d46c5127da9207c73927388283b5a32f63350852b8b297899bcae150a7ee34789902f26e5956d582da2d8612c91e5ee379e631ab14b2d7e5ad5ab12ed37d1b839f359c3d301cfbeb253cefd2fb23d9f7c86b472a9b0d74bd2ae824556740fed82669d74c9f50967c60ddd68143fc866cf0ce440d19587783d110085cdf1b025ff0194677684bb006ddb16c5e86769e12b3aa0060614e1b48aa702d81972338d4261b9381d318db147673d5c89efd8fd7bfde87eadcd5cf9e1751b53f69efba4fefab6b3fb9a3656758b163c91a9b94d5745fce38969334cf9a61caa25cd7be683d49a507767c9f439434ea848eef63e982b7907d40aec2ff4b856268497de2554870de7c4c92251374e14a6c6586a03895df9309bbe6d40205e2e30ed498edf9dbe02f12db857de248d5b73b77de7ca2fee8eb7b359b7ef31c4eeb71bf7269efeba9e2e052456b8713b70860f44446b0d5e41d1794b6a27959405070ef6511575052f71e4975fbd05724025c531c3496665bba7c8992ee59f5c0b489c2260722a4574284661b3021a412d404c5478197188f2d6f06954671a4532834c710f0cd74b0b7b7a350ed28db2914a6fd28d38a12ea27cb244fecae26f8e6e924847affd0b17fbd5ae882fee7bc97c628cd729b61b646e188c161d3ff1e8faf553691ae5d4f984322d001b95f52e1b0d1010e1bededc70d69576f06754af593f0b8c071055eed5f00c64bd32601029c958b790fd35c82bee8e049e1f11e717a96805bc8ef49131cca1796f52990a22627fdae0152aa5e74d1f2bcaa765193b6f0c9f980cceb6c4fb7695619be2e8ed6e70fd067540fec1e37dc9e6c6b135dd9d9f66c741d974420036e2d5152c551e4d2a074db85ea26f27af2462cfd1ded4bc86c63276466caff3766c471c840e8c275f1bc1c34734074a207dc175729ea903d17d6b6ea11d79c28e9cb284868b0dc7db9e06cfb3f673b421faa4d5993d7eb77312cd24c7feac7f7e2316c4554fb5ce949e1edce16928a3900565f2ef5e413670a21701a638066f680e2f74d197abaed7c2748d7684ffd103b754c785aff32e2ea8410b74a9b3f43436ced0d6106dc6530508a7280e161433b74a81bed2f01d542c8e3284069e69978cbfcf9cd670c937d437b93fedcf547ced6e7c5b732d33bd6fe75f9ae7b811e4bf3e1aec167ebbbe53ac3497650bc507aa3d4e62d3b48f82280b2e7bed49033e4cc8f0b4e20b5e4381b4c3b4ca805d2e5ab1c884d171b361302517caa12842bdacf11f6e728e0143275bef9f5d8543aa14c3f907970cdcaedab9af7cee91d30d71be43ebab3c2b679c75f9565849bdfe5cb5995494c62a0b2b9cdff371f7d12fe20e0f44d9c9493bd5c5518dda5a9b18d1c0d725b58e8ffe151dc5e425aa4414cb456119cc8e2e20128abba3e6165269cddb2fb80e9167554c3ee2f9ff5a00c2e018287b2fd65c3dcacaab7df0ad8ceba6df499d9a35bebda09ceb7b7feb36b59c303eebce3b70f336a0b8db7fcc4f9b3ceb5749ac1ea9b9a5b14b5d813d7f63495cd7f669d37969054da00dbca5ea977a1c8f73788042ecd6bae8a4e20c727c485c76072dcd6780877f6af10eeb4a9583f0eb08b102e6aab17959543e3c739891664a16d07c5e9d9b09bce6f442bdaa10fece981cf1635c217e4f0d0be936861b66c210bfaf18ac3fcae1ef07a415b9768a012a40421b74e9c5c2828cd019e035c29b8f82a5da05570395867bf17b6b9799e99635ceab9a47a5988dba7941fa7ab59f9dd7cca31bc5534a0f5d4bf20c812cd592a678cd4144a5d638bb229c1a64eef2449651bb492f5d2691a6d8295f4869743c303bcd95540eb63574373f2ab11fd05bc1a6b67c0aba13313e3d0d181b050b640c0efe2a107e11e23b4e024a02c3e50030b7b551dec2ea54ef3712f57014debc5b4ea91e06b83e5c68566cca7567325fe677e3bb904dd3625ec465440caa6a5266f387a357517be909b7828de964b58ae6ce270be7b2d834420029a653f48e7df139a77bcb734c1e2572cc452dcad3da5130f16e438650053ca7021e88fa688b7ad8dece3407206d3944aa15129764c470695416730ed19f68c60c7401a25884209b51bc5e9f2c783a1c54317e7be38eafacfe1b28d74cfe5bddddfeffb216751de05334a8b4fb6ca3d97fee86f7c1662c815aaf9ca8a73c6c6202712de09e0bcd70171da4f5c24644bf70108b92784ec162c44e94d90a88b741b1a918d7df9652bc14e5cda0e421a645b7145a3a0ad5d5cd624ac62c956b2e0f1b276f854e9693435032e0a75d6a3b9a7e55d3ddddec1814e6338d09876c1db8343eced83430283a58bdb0c5dbf6b5fc7cbb8eb043989b38e773e75626e1ea9fbf3e1d9afbfb2dcf3fb9aa74b79e576aaaf3726ec48deb8fa550d73c1b8fd17aa4fcd90733bf515b97ba47fd80aaf9c90558f67c966c83dfeef66c8e39c029e0e840cd0a3ac7a711717939873217aa71fa4e8bd30a327eafa3bceba2663b37d45ffeffa079f112b17dedb302723383d2264f3f52b1e6b76767eaa7a85973854ff85f3e72d0bce09d913176ce4b10c7f60336c85538aca07f11f3e27a9dd0754922f493f8bc5905b1694f6ddfa490474200d0b91d47ae9545d3a15d6c2b6af62054e87df55243a029ada22d9e42d5903886b0d5498bcda98340747a6bd9d3d8d1e440f0a056a0b01a14eb1a750b607bd4d98d3b48e5daa68e2306e44f4ef4fdabd28dd7f56405dce0f71cbfc5c67d73eaec49d5b1cb871c06afafc319a931952dcefcae6cb25777a38b29d14f98e0a77527c0c773b4e1d621d445b79e46582a3f543ac4c2c6cd70542b6534da56c2db1a54eb971bb1d5a5b2e60a78ad29bd0dc5a7e6fadb09e87729aa1cfaf680725093ddc84a6758af2fa840d99e29a1cd1c103631fe05a311873d926c3d97dabf9f57d650309cc1f8c7ebd68e8babc72289176a1d0fccd0839ed0ac1f4a5a9c97f37e779ca72a5ab6c9c46c25f025ccf0e4aebd0c4f0d5926e0452df11f8809516978885a86d8fd4edc740a29a91d8f6f37d647ec750c6e4cdc540aa9b65f39065ffca9f56cfa63dff7920bdd4b5fc4d07f983a0690bf7f6de0e5be24969698b1ff9afd055552e749dd434df7d8ed940f3dd27992d34f97d65f051560f4397cf2b0468c4c5e9c26660432a059c8195c80644db5d0d3140b437114db523f66523c42a8408515d41f05a88ca4c0487bcd278527d6be334c4c42b3236363026dcc9d6362a34302e684f40685442dc1edb1dd109c13b02130222c2e31396c6c7050724ec89095dbc2b34c82229342e3e3c3a6a31d5627b5c74e4622a8542b193de95bd844a46162034637e5fa1e8c0296b51f24170f3747511d6550b8adb04d9279c74d13e78c6a0f4c1275babc4474b5d678c0e300f74a3e93c589ab24fa31c9eb03815bcc4dd7b4742420c38bff8d8f0c8309bd8589be0e848dbd8d88098b8e890c4e08480e898d0b8c004704af1b63111817b62636d03a3a2a3f6444627c6db8647068685da6e4fdc191e15909018be333c30ca26262a4c5b0b21000a38aa49f8e87f1e94189118fdf63f8f8c0e0a8f08b50d094d080c8fb0d9911019b13420283c643195e66011b02b09bc671a53f6ee479945c68759485f40a152a91631e01e9de6c0b073a45b53e9a054d2197426838ca32da3d26cece036745ece0356a530b9033d750cc429da938256b43c6055a19c3678bc3f078ec44f83fb55d03de61c15b61fe577670a4a529db4a9346b8a1d99e2e044a1b81a0a5aea05d52568f7005ad9f3315ad9262e4c1636976d71771f7d538961c136b131e1c136c151005860b0ed8ee5eb83f6ae71f48fdd1d1e1cbafc23ba8f47a8cff2102ac32fe1437f576a78909703d52121d67f935f78a0e7de4f6ca974fa4e35413b34b6716a32f969ff48fc5da22399f682447ca94b34b540188887d79b887d59daaff4809ca723c497fac49908d11a216a4b0c5e1a42195a39af060f8cb4d5b4e0c7f95785068684c6c18ffa1b7a868687ed088a8e5b1e1d196933f61c883ca21682d7859fc6b76220da59a5c446e2ff003a3c50')


#mqq.IMService.FriendListServiceServantObjf
#mqq.IMService.FriendListServiceServantObjf
#print Un_friendlistSetGroupReq('1111111110022c3c42d57947ad560a4f6e6c696e6550757368660d537663526571507573684d73677d000101420800010603726571180001061c4f6e6c696e65507573685061636b2e537663526571507573684d73671d000101140a020b35cf7112581f34f52900010a020b35cf711c2102103115ff460052581f34f56d000100a400271a0c1c2c3c4c5d000c6d000c7d000c8d000c9cacbcccdd000cecfc0f0b2a0c1c2c3c4c5c6c0b3a0c1c2c3c4c5c6c7c8d000c9d000cacbd000ccd000cdced000cfc0ffc100b4a0c1c2c3c4c5c6c7c8c96000b5a0c1c2c3c4c5c6c7c8c9d000c0b6a0c1a0c1c26000b2a0c0b3a0c16000b4a090c0b5a090c0b0b7a0c1c2c36000b8a0c1c2c36000b9a090c0bad0000130a11080010001a0b080a10071a0536363636367c8d00000d089004109084848180808080029d000ca30200000000210210b001c90cda06001600260036000becfd0f000cf61000f61100f9120c0b327502330a4d000c590c680c7c0b8c980ca80c')

def test(data):
    jce = JceInputStream(data)
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jcemapdata = jce.ReadValue()[6:]
    jce_1 = JceInputStream(jcemapdata)
    print jce_1.ReadValue()
    print jce_1.ReadValue()


        # maplistdata1 =  jce_3.ReadValue()
        # jce_4 = JceInputStream(maplistdata1)
        # jce_4.ReadValue()#0A
        # jce_4.ReadValue()
        # jce_4.ReadValue()
        # jce_4.ReadValue()
        # jce_4.ReadValue()
        # jce_4.ReadValue()
        # print 'PB',jce_4.ReadValue()
        # jce_2.ReadValue() #0B
    # jcemapdata = jce.getHex(6)
    # jce1 = JceInputStream(jcemapdata)

def Un_ProfileServiceReqBatchProcess(data):
    pblist = []
    data = data[8:]
    jce = JceInputStream(data)
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    data = jce.ReadValue()

    jce_1 = JceInputStream(data)
    jce_1.getHex(6)
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    data1 =  jce_1.ReadValue()
    jce_2 = JceInputStream(data1)
    jce_2.ReadValue()
    count = jce_2.ReadValue()
    for item in range(count):
        jce_2.ReadValue() #0a
        jce_2.ReadValue()
        jce_2.ReadValue()
        jce_2.ReadValue()
        pblist.append(jce_2.ReadValue())
        jce_2.ReadValue() #0b
    return pblist

#print test1('0000044a10022c3c42047dfcfc560e50726f66696c6553657276696365661052657370426174636850726f636573737d00010411080001061052657370426174636850726f6365737318000106144b51512e52657370426174636850726f636573731d000103de0a0900020a00011c2c3d0001037d088d111001180022f3060af006088cdec7c60110001ae50608a689c44e10b9e1abb90518918880d80220c081840528d00f30870340b24e7a16e69dade5b79ee688b7e5a4962de69983e682a0e78cab8a01690d4672656520636174efbc81e8afb4e8b5b0e5b0b1e8b5b0efbc8ce5bfabe4b990e69983e682a0efbc81efbc81efbc81e788ace5b1b1efbc8ce4baa4e58f8befbc8ce887aae9a9beefbc8ce4bab2e5ad90e38082e8bdbbe5a5a2e688b7e5a496e69785e8a18cefbc81920129e688b7e5a49620e69785e6b8b820e8bf90e58aa820e69184e5bdb120e887aae9a9be20e4bab2e5ad90a00204a802bf01b00200c2026e0d46726565266e6273703b636174efbc81e8afb4e8b5b0e5b0b1e8b5b0efbc8ce5bfabe4b990e69983e682a0efbc81efbc81efbc81e788ace5b1b1efbc8ce4baa4e58f8befbc8ce887aae9a9beefbc8ce4bab2e5ad90e38082e8bdbbe5a5a2e688b7e5a496e69785e8a18cefbc81ca023908a689c44e108cdec7c6011a1830396431303461363537333933393639303030306562356520e9f2e4b9052800300038064206e4baa4e58f8bca023908a689c44e108cdec7c6011a1830396431303461363537333933393639303030306562356620e9f2e4b9052800300038064206e4bab2e5ad90ca023908a689c44e108cdec7c6011a1830396431303461363537333933393639303030306562363020e9f2e4b9052800300038064206e4bc91e997b2ca023908a689c44e108cdec7c6011a1830396431303461363537333933393639303030306562363120e9f2e4b9052800300038064206e688b7e5a496ca023908a689c44e108cdec7c6011a1830396431303461363537333933393639303030306562363220e9f2e4b9052800300038064206e69184e5bdb1ca023908a689c44e108cdec7c6011a1830396431303461363537333933393639303030306562363320e9f2e4b9052800300038064206e69785e6b8b8ca023908a689c44e108cdec7c6011a1830396431303461363537333933393639303030306562363420e9f2e4b9052800300038064206e788ace5b1b1ca023908a689c44e108cdec7c6011a1830396431303461363537333933393639303030306562363520e9f2e4b9052800300038064206e887aae9a9bed2023508a689c44e10c6f7e7c10518f84f208c81a2392896deb90e321be69dade5b79ee5b882e9be99e794b3e58991e6a1a5e585ace7a4beb803020b0a00011c2c3d00004708991110011800223e088cdec7c60110001802220408eba247220508c6ebb92f220508a689c44e220608b899b88101220608cbbcaba601220608abbf94b903220608bbd0ced8030b0b8c980ca8')
def Un_SummaryCardReqSummaryCard_1(data):
    jce = JceInputStream(data)
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    jce.ReadValue()
    data1 = jce.ReadValue()
    jce_1 = JceInputStream(data1)
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    jce_1.ReadValue()
    data2 = jce_1.ReadValue()
    jce_2 = JceInputStream(data2)
    jce_2.ReadValue()
    jce_2.ReadValue()
    jce_2.ReadValue()
    jce_2.ReadValue()
    nickname = jce_2.ReadValue()
    return nickname


def dd(data):
    d1 = data[:1]
    data = data[1:]
    return d1,data


def reddd(data,str=None):
    if str:
        pass
    else:
        str=''
    d,retdata = dd(data)
    if d == '3':
        d1,retdata1 = dd(retdata)
        str += d1
        return reddd(retdata1,str)
    else:
        return str


def Un_SummaryCardReqSummaryCard(data):
    data = data[8:]
    d = '687474703a2f2f6d632e7669702e71712e636f6d2f70726976696c6567656c6973742f6f746865723f667269656e643d'
    retdata =  re.findall(d+'([0-9]{0,24})',data)
    if retdata:
        qqnumber =  reddd(retdata[0])
        nickname = Un_SummaryCardReqSummaryCard_1(data)
        print qqnumber,nickname

    else:
        print 'null'








