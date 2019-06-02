# -*- coding: utf-8 -*-

class protobuf:
    def __init__(self,data):
        self.data = data
    def decode(self,path):
        cache = self.data
        list = path.split('->')
        if not list[0]:
            list.remove('')
        for item in list:
            [type,value,retdata] = self.getWireTypeValue(item,cache)
            if type == 2:
                cache = value
            else:
                return value
        return cache
    def bin2(self,data):
        b2 = bin(int(data,16)).replace('0b', '')
        value = '0'*(8-len(b2)) + b2
        return value

    def getVarint(self,data,b = ''):
        hex = data[:2]
        data = data[2:]
        bin8 = self.bin2(hex)

        if bin8[:1] == '0':
            value = bin8[1:]+ b
            return [value,data]
        else:
            value = bin8[1:]+ b
            return self.getVarint(data,value)
    def getValue(self,type,data):
        if type == 0:
            if data[:2]:
                [value,retdata] = self.getVarint(data)
                return [int(value,2),retdata]
            else:
                data = data[:2]
                return [127,data]
        elif type == 2:
            [long,retdata] = self.getVarint(data)
            long = int(long,2)
            if long:
                value = retdata[:long*2]
                retdata = retdata[long*2:]
                return [value,retdata]
            else:
                return [0,retdata]
    def WireType(self,data):
        [value,data] = self.getVarint(data)
        if value>7:
            number = int(value,2) >> 3
            type = int(value[-3:],2)
        else:
            number = int(value[:4], 2)
            type = int(value[-3:], 2)
        return [number,type,data]


    def getWireTypeValue(self,numberhex2,data):

        while data:
            type = data[:2]
            if type == numberhex2:

                [number,type,retdata] = self.WireType(data)
                [value,retdata] = self.getValue(type,retdata)
                return [type,value,retdata]


            else:

                [number,type,retdata] = self.WireType(data)
                [value,retdata] = self.getValue(type,retdata)
                data = retdata
        print '找不到'
    def getWireTypeValueList(self,numberhex2,data):
        list = []

        while data:
            type = data[:2]
            if type == numberhex2:

                [number,type,retdata] = self.WireType(data)
                [value,retdata] = self.getValue(type,retdata)
                data = retdata
                list.append(value)
            else:

                [number,type,retdata] = self.WireType(data)
                [value,retdata] = self.getValue(type,retdata)
                data = retdata
        return list



#aaa = protobuf('0a0e1a0c08e0b290f40110a18692e007120a0801100018f78dfeff0f1aab010aa80112a50122a2010a2439333645453036424430333530393543393931433541323537323631344145342e6a706710b9d2031a252f39666337326266342d393833332d343835642d623437382d34646464626539636133623028eb073a10936ee06bd035095c991c5a2572614ae440c00748d00552252f39666337326266342d393833332d343835642d623437382d3464646462653963613362306800800103c001a18e01c80186890220f78d022893adc0f906322408a98d94c20510a98d94c205288aae82a80548a2a2fdec07588c978ab90968a98d94c2054000')
#print aaa.decode('->1a->0a->12->22->1a')
#print aaa.decode('->1a->0a->12->22->52')




#print pbmsgdecode('->2a->22->1a->0a->0a->4a')

#print pbmsgdecode('->2a->22->1a->0a->12->0a->0a').decode('hex')

#aa = protobuf('080012001a2308cb93aebf0510cb93aebf05288a968e784890aca1f90b58b996988e0768cb93aebf0520022a8801088793aebf0510889fb78d01180122760a2808889fb78d0110f19ed75918a601200b28a9800130cb93aebf0538c598fbac8e80808001b801dd12120808011000180020001a400a3e0a27080010ca93aebf0518c598fbac0e2000280a300038860140314a0ce5beaee8bdafe99b85e9bb9112130a110a0fe4bda0e5a5bde5958ae5958ae5958a30012a0f08a5caa3bf0510f19ed759180130013800420048')
#print aa.decode('->2a->22->1a->0a->0a->4a').decode('hex')
#print aa.decode('->2a->22->1a->0a->12->0a->0a').decode('hex')


#606722b22da294d333bd7653aa1fec0f

#print '2f39666337326266342d393833332d343835642d623437382d346464646265396361336230'.decode('hex')


#0a2439333645453036424430333530393543393931433541323537323631344145342e6a706710b9d2031a252f39666337326266342d393833332d343835642d623437382d34646464626539636133623028eb073a10936ee06bd035095c991c5a2572614ae440c00748d00552252f39666337326266342d393833332d343835642d623437382d3464646462653963613362306800800103c001a18e01c80186890220f78d022893adc0f906322408a98d94c20510a98d94c205288aae82a80548a2a2fdec07588c978ab90968a98d94c2054000
#0a2439333645453036424430333530393543393931433541323537323631344145342e6a706710b9d2031a252f39666337326266342d393833332d343835642d623437382d34646464626539636133623028eb073a10936ee06bd035095c991c5a2572614ae440c00748d00552252f39666337326266342d393833332d343835642d623437382d3464646462653963613362306800800103c00118209868902