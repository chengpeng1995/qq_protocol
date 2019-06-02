import random
import time


def getVarints(data):
    b2 = ''
    p = bin(data).replace('0b', '')
    p = '0'*(35-len(p)) + p
    b2 = '0'+p[:7] +b2
    p = p[7:]
    b2 = '1'+p[:7] +b2
    p = p[7:]
    b2 = '1'+p[:7] +b2
    p = p[7:]
    b2 = '1'+p[:7] +b2
    p = p[7:]
    b2 = '1'+p[:7] +b2
    p = p[7:]
    return hex(int(b2,2)).replace('0x', '').replace('L', '')
def encode_Varints(number):
    if number>127:
        bin2data =  bin(number).replace('0b', '')
        bin2data =  (7-len(bin2data)%7)*'0'+bin2data
        number = len(bin2data)/7
        retdata = ''
        while bin2data:
            number = number-1
            if number != 0:
                retdata =  retdata + '1'+bin2data[-7:]
                bin2data = bin2data[:-7]
            else:
                retdata =  retdata + '0'+bin2data[-7:]
                bin2data = bin2data[:-7]
        rrr =  hex(int(retdata,2)).replace('0x', '').replace('L', '')
        if (len(rrr) % 2) == 0:
            return rrr
        else:
            return '0'+rrr
    else:
        ret = hex(number).replace('0x', '')
        return '0'*(2-len(ret))+ret
def abc(n):
    value = ''
    for item in range(n):
        value += random.choice('0123456789')
    return value
def getmsg():

    value = '0000003608001224'+msg()+'180020142803300138'

    return value

def msg():
    datatime = getVarints(int(time.time()))
    msg = ''
    msg += '08'
    msg += datatime
    msg += '10'
    msg += datatime
    msg += '28'
    msg += getVarints(int(abc(10)))
    msg += '48'
    msg += getVarints(int(abc(10)))
    msg += '58'
    msg += getVarints(int(abc(10)))
    msg += '68'
    msg += datatime
    return msg

