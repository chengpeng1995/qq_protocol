import zlib
def gzipdecode(data):
    data = data[4:]
    a = data.decode('hex')
    b = zlib.decompress(a,-zlib.MAX_WBITS)
    c = b.encode('hex')
    return c
class JceInputStream:
    def __init__(self,data):
        if data[:4] == '78da':
            self.data = gzipdecode(data)
        else:
            self.data = data
    def getHex(self,i):
        value = self.data[:i]
        self.data = self.data[i:]
        return value
    def getType(self):
        if self.data[:1] == 'f':
            self.getHex(1)
            type = int(self.getHex(1),16)
            number = int(self.getHex(2),16)
            return [number,type]
        else:
            number = int(self.getHex(1),16)
            #print 'number',number
            type = int(self.getHex(1),16)
            #print 'type',type
            return [number,type]
    def _getType(self):
        if self.data[:1] == 'f':
            k = self.data[:4]
            k = k[1:]
            type = int(k[:1],16)
            k = k[1:]
            number = int(k,16)
            return [number,type]
        else:
            k = self.data[:2]
            number = int(k[:1],16)
            k = k[1:]
            #print 'number',number
            type = int(k[:1],16)
            #print 'type',type
            return [number,type]
    def ReadNumber(self):#8
        [number,type] = self.getType()
        if type == 12:
            return self.getValue(type,'')
        else:
            if type == 3:
                data = self.getHex(16)
                return self.getValue(type,data)
            elif type == 2:
                data = self.getHex(8)
                return self.getValue(type,data)


    def ReadByte(self):
        [number,type] = self.getType()
        if type == 12:
            return 0
        else:
            data = self.getHex(2)
            return self.getValue(type,data)

    def ReadShort(self):
        [number,type] = self.getType()
        if type == 12:
            return self.getValue(type,'')
        else:
            data = self.getHex(4)
            return self.getValue(type,data)

    def ReadString(self):

        [number,type] = self.getType()
        if type == 12:
            return self.getValue(type,'')
        else:
            long = self.getHexInt(self.getHex(2))
            if long == 0:
                return ''
            else:
                data = self.getHex(long*2)
                #print 'long',long
                return self.getValue(type,data)
    def ReadList(self):
        [number,type] = self.getType()
        if type == 12:
            return self.getValue(type,'')
        else:
            y = self.getHex(2)
            if y == '00':
                k = self.getHex(2)

                Count = self.getHexInt(k)
                return Count
            else:

                if y == '0c':
                    return 0
                else:
                    Count = self.getHexInt(y)
                    return Count
    def ReadSimpleList(self):
        [number,type] = self.getType()
        self.getHex(2)
        LONG = self.ReadValue()
        if LONG:
            return self.getHex(LONG*2)
        else:
            return self.getValue(type,'')
    def ReadStruct(self):
        [number,type] = self.getType()

    def getHexStr(self,data):
        return data.decode('hex')
    def getHexInt(self,num):
        return int(num,16)
    def getValue(self,type,data):
        if type == 0:

            return self.getHexInt(data)

        elif type == 2:
            return self.getHexInt(data)
        elif type == 6:
            return self.getHexStr(data)
        elif type == 1:
            return self.getHexInt(data)
        elif type == 3:
            return self.getHexInt(data)
    def ReadValue(self):
        """
        auto
        """
        [number,type] = self._getType()
        if type == 0:
            return self.ReadByte()
        elif type == 3 or type == 2:
            return self.ReadNumber()
        elif type == 1:
            return self.ReadShort()
        elif type == 6:
            return self.ReadString()
        elif type == 13:
            return self.ReadSimpleList()
        elif type == 9:
            return self.ReadList()
        elif type == 10:
            self.getType()
            return '0A'
        elif type == 11:
            self.getType()
            return '0B'
        elif type == 12:
            return self.ReadByte()
        else:
            self.getHex(2)
            return ''
#aa = '00b942a78e1c21025236022d2d4c50146c7c8c9ca014bcc600d001e6022d2dfc0ffd10000cfd11000cfc12fa1308000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bfc14fd1500000a088ecf8aca0b8819b817fc16fc17fc18fc19fc1af61b00fc1cfc1dfc1ef01f01fc20f62100f62200fc23fc240b8c9001acbcc004d004e900040a0c160ce68891e79a84e5a5bde58f8b20023c4c5c0b0a00011606e69c8be58f8b2c3c40015c0b0a00021606e5aeb6e4baba2c3c40025c0b0a00031606e5908ce5ada62c3c40035c0bfc0ffc10fc11f21257de6ef4fc13f9140cfc15fc16fa17020b35cf711c2c36004c50146c7c8c9cacbcc600dce6012dfc0ffd10000cfd11000cfc12fa1308000300011a0c1c2c3c0b00021a0c1c2c3c0b00031a0c1c2c3c0b0bfc14fd15000cfc16fc17fc18fc19fc1af61b00fc1cfc1dfc1efc1ffc20f62100f62200fc23fc240bf01801'
#de = JceInputStream(aa)
#print de.ReadLong()
#print de.ReadByte()
#print de.ReadShort()
#print de.ReadString()
#print de.ReadByte()
#print de.ReadByte()
#print de.ReadByte()
#print de.ReadByte()
#print de.ReadByte()
#print de.ReadByte()
#print de.ReadByte()
#print de.ReadByte()
#print de.ReadString()
#print de.ReadByte()
#print de.ReadString()
#print de.data
