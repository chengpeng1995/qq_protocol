import config
import JceOutput as out
from Tools import Coder
def Write_SvcReqRegister(Uin,Bid,Status,timeStamp):
    msg = ''
    msg += out.WriteLong(Uin, 0)
    msg += out.WriteLong(Bid, 1)
    msg += out.WriteByte(0, 2)
    msg += out.WriteStringByte('', 3)
    msg += out.WriteInt(Status, 4)
    msg += out.WriteByte(0, 5)
    msg += out.WriteByte(0, 6)
    msg += out.WriteByte(0, 7)
    msg += out.WriteByte(0, 8)
    msg += out.WriteByte(0, 9)
    msg += out.WriteLong(timeStamp, 10)

    msg += out.WriteByte(15, 11)
    msg += out.WriteByte(1, 12)
    msg += out.WriteStringByte('', 13)
    msg += out.WriteByte(0, 14)
    msg += out.WriteSimpleList(config.DEVICE_IMEI, 16)
    msg += out.WriteShort(2052, 17)
    msg += out.WriteByte(0, 18)
    msg += out.WriteStringByte(config.DEVICE_NAME, 19)
    msg += out.WriteStringByte(config.DEVICE_NAME, 20)
    msg += out.WriteStringByte(config.DEVICE_VERSION, 21)
    return msg
def Write_RequestPacket(Version,RequestId,ServantName,FuncName,Bin):
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

    return data
def Write_FL(ReqType,Reflush,Uin,StartIndex,GetFriendCount,FriendCount):
    msg = ''
    msg += out.WriteShort(ReqType,0)
    msg += out.WriteShort(Reflush,1)
    msg += out.WriteLong(Uin,2)
    msg += out.WriteShort(StartIndex,3)
    msg += out.WriteShort(GetFriendCount,4)
    msg += out.WriteShort(0,5)
    msg += out.WriteShort(FriendCount,6)
    msg += out.WriteShort(0,7)
    return msg

