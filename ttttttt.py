# -*- coding: utf-8 -*-
import time,re
import threading
import random
from mode import JceFactory
from mode import JceOutput as out
from Tools import Coder
from Tools import MD5
from Tools import TEA
from Tools import HexPacket
from Tools import Img
import Keys
from Tlv import Tlv
from RawSocket import RawSocket
import config
def decodeTlv( cmd, data):
    if cmd == Coder.trim('01 6A'):
        pass
    elif cmd == Coder.trim('01 06'):
        pass
    elif cmd == Coder.trim('01 0C'):
        pass
    elif cmd == Coder.trim('01 0A'):
        token004c = data
    elif cmd == Coder.trim('01 0D'):
        pass
    elif cmd == Coder.trim('01 14'):
        pack = HexPacket(data)
        pack.shr(6)
        token0058 = pack.shr(Coder.hexstr2num(pack.shr(2)))
    elif cmd == Coder.trim('01 0E'):
        mst1Key = data
    elif cmd == Coder.trim('01 03'):
        stweb = data
    elif cmd == Coder.trim('01 1F'):
        pass
    elif cmd == Coder.trim('01 38'):
        pass
    elif cmd == Coder.trim('01 1A'):
        pack = HexPacket(data)
        pack.shr(2 + 1 + 1)
        nickname = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(1))))
    elif cmd == Coder.trim('01 20'):
        skey = data
    elif cmd == Coder.trim('01 36'):
        vkey = data
    elif cmd == Coder.trim('01 1A'):
        pass
    elif cmd == Coder.trim('01 20'):
        pass
    elif cmd == Coder.trim('01 36'):
        pass
    elif cmd == Coder.trim('03 05'):
        sessionKey = data
        qqkey = sessionKey
        print 'qqkey',qqkey
    elif cmd == Coder.trim('01 43'):
        token002c = data
    elif cmd == Coder.trim('01 64'):
        sid = data
    elif cmd == Coder.trim('01 18'):
        pass
    elif cmd == Coder.trim('01 63'):
        pass
    elif cmd == Coder.trim('01 30'):
        pack = HexPacket(data)
        pack.shr(2)
        server_time = pack.shr(4)
        ip = Coder.hexstr2ip(pack.shr(4))
    elif cmd == Coder.trim('01 05'):
        pack = HexPacket(data)
        verifyToken1 = pack.shr(Coder.hexstr2num(pack.shr(2)))
        verifyPicHexstr = pack.shr(Coder.hexstr2num(pack.shr(2)))
    elif cmd == Coder.trim('01 04'):
        verifyToken2 = data
    elif cmd == Coder.trim('01 65'):
        pack = HexPacket(data)
        pack.shr(4)
        title = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(1))))
        msg = Coder.hexstr2str(pack.shr(Coder.hexstr2num(pack.shr(4))))
        verifyReason = title + ": " + msg
    elif cmd == Coder.trim('01 08'):
        ksid = data
    elif cmd == Coder.trim('01 6D'):
        superKey = data
    elif cmd == Coder.trim('01 6C'):
        psKey = data
    else:
        print 'unknown tlv: '
        print cmd, ': ', data

def unpackRecvLoginSucceedMessage(data):
    data = TEA.detea_hexstr(data,'9A1BDA11D3BEA2DEDC58C487B3D174BA') #shareKey
    pack = HexPacket(data)
    pack.shr(2 + 1 + 4)
    data = pack.shr(Coder.hexstr2num(pack.shr(2)))
    #TLV解包
    data = TEA.detea_hexstr(data,'9d2a2efab0653d0aecdb8a3e97c4dd22')#tgtKey
    pack = HexPacket(data)
    tlv_num = Coder.hexstr2num(pack.shr(2))
    for i in xrange(tlv_num):
        tlv_cmd = pack.shr(2)
        tlv_data = pack.shr(Coder.hexstr2num(pack.shr(2)))
        decodeTlv(tlv_cmd, tlv_data)


def unpackRecvLoginMessage(data):
    data = TEA.detea_hexstr(data, '00'*16)
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
        unpackRecvLoginSucceedMessage(pack.remain())

#print Coder.str2hexstr('188075889')


#print 'd855a395498ac6850826a74b0800450004afdc2840003406b132b73d2e92ac1b23031f90a74eb484671a15d5dd4850180052b7ec0000000004870000000802000000000d31383830373538383965c4fa3be3953615850b34d869149bad2d9902b54b35d427b3d5a72db32731a05967a1bef5dbf382212a52a89a8039641e1749393ea42f88d9cb13e4d6fbc62cc984eb616dcb8fe73a9cb2f05a4667bad559581ad41a0388dee7797f47aa8d770b43794356e2d739239fa20c8a13f6a2035e68568613a784bbf3b9d5b2dfcda900addf529a8cd744d51c87a0435407b36ba9765b8db2edd9daae1da0452f47747ae8c4a3b77f6013b84698d1d52fde84776986c28be180527890e6fcfa3d46f7c7734bb37efbfae245d74d57c7c63a94cfb60945f055364cebe8aa1c9d1e3630b2f78a1feb6c1067ed735b488af80a6f3653b07b1d11ad3a6e9f51b7095d2e8857500079e55897c8e8557199a005cb86e054eea7901b1e8bbb7ac1a3992be779a034b729b96117cf1976320a4dde57e7151d63079564428b63a0b0e65d5a42cd27665e485b65329de08d895117e9dd15942adbb686688038c5ad8ceaa2ea13410a3809d9d0084667dbde7e2ce733380eb702ed2dfd716f0688f48a061faec4542edf5ee11ed73ec2eb267856b2dc5ce2f72349065404a58c1f208b63676c96ad7028fc8693af3725f9a7d5e026425fb83607b2487fafebf6e7995a121987cf442a9b27c7d8a98842a83de89a3b423006d5f8125c6fb56d379dded9bc115e27edbb9142f88ca2f8174f9accae3e3f98e4a796fe9264331f857b519398db82e889f152dfac60abb0845ad198e8021aac64ae48dd6a4aab4104810e21e1c5365a3ab71c9ae4e183c9325c6421ed8d9c19479a9f176b452b7c78ea85209910cb77854691ce22c77fb7a6153482194e772a5bf3e3fafaec4cedef8844c7011714b9f7b8d9cdc0e105fc7a5efaaadbffa1bf0234f7f3b4cabe73dd696f9ef5c92c5e859657056f091a8ab47316eabecc41461ae867986ef263d338576c9d1e27c0c9fd886f5ddb4b056fcc0c6f42fd57ee02a584bf12c5bd148e912b261d545e2428e932a643a11c0ebbd3e272747b8a8118ed072493c7a5318f76dd86c3cb6f1947f2ecea8f289500e25fe33679618a2ba20cdb1441abf48d883d58904796eeade924f30db4027a2a3dcae68ddcf596ad9318ce744662ec812b6c3ae55d5d3280d6ea491ba9048da3c429d4c5a684cde0c27a5071eb1824e609aedb900b58255340d8ca2f54198a233d48adbde621fafeda81a7623be39f7ff0590dddba0bbf6bf40b4b4ad12b9841c06decd622ab2709bd102bd262374bf817dc4ac810d50a6ffd3f4c3e83d812984631b33973c6d8a90b8f1ec71c87de64724700b885e4c541a7c60d819e05f4c5226222138c5ef9bd41472eb4399e56a9d11b6a19644b609641abe3b851308ee41dfb3e37a0939d197beea791c487c504c01708f6f538c37f768a84ce2125348f1c2c409292be7359c879419324afe9947cb1b95329d9686712def98d46e4c3ad0ac66cda19486d9d63d53c6ec6231068a7bb2944649500599133d875d19a1c326f5f8e88458a604fe006bedba3195f69fc1a38e16536b68544392409d10b57459486af50ffd09ae8565c78160f3564532bec843efd1fecf74b6d71e433596a729ce0c03be18d1ed3bfe1'
ret = 'd855a395498ac6850826a74b0800450000cf06fe40003206641d7040edb5ac14d3031f90bb533ad334a05bc628b550180048c4fb0000000000a70000000802000000000d313838303735383839d156bab3103f29d24b7b6b22a2c0250a9dcb2e8854782b11520596e711475a8cbe5bb70c4ba3b8d02198cd7ab29aa719f9cc257c5e390412c761fdf9433448b526a7f286317ebcd9ec83e2e2719097532578f872fa88ca2c77a04d0ed3562e66dff62b349dbb555d5ee608bc7ceb5f17254e1784dea4b64ce70fcf159b64edcdee825f54a35287306d517cfab34202be'


#返回包体
unpackRecvLoginMessage(ret)
# value = '03000000wqeqweasd'
# def getre(pram,data):
#     value = re.findall(pram,data)
#     if value:
#         return value[0]
#     else:
#         return data
#
# print getre('03000000(.*)',value)
#
#
# data = '00000036080012240880c883bf051080c883bf0528c5c5b2c60648bdfae0f81058c2cfa1931b6880c883bf05180020142803300138'
#
# body = TEA.entea_hexstr(data,'3c40512a6e507d76605d6d2c6b5d3e32')
# print body
# da = 'c30a59c20817913680b0787dc4af5c16a93a80c46b6a9ebff2db69a3fd65f8938c0f46e438e273507b4ce1592652a4f1e16b4c23302863d890c300d1e5c2bff4'
# print TEA.detea_hexstr(da,'3c40512a6e507d76605d6d2c6b5d3e32')

