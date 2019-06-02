# -*- coding: utf-8 -*-


def SetInt(int):
    data = hex(long(int)).replace('0x', '').replace('L', '')
    return '0'*(8-len(data)) + data
def SetShort(int):
    data = hex(long(int)).replace('0x', '').replace('L', '')
    return '0'*(4-len(data)) + data

def SetByte(int):
    data = hex(long(int)).replace('0x', '').replace('L', '')
    return '0'*(2-len(data)) + data

def SetLong(int):
    data = hex(long(int)).replace('0x', '').replace('L', '')
    return '0'*(16-len(data)) + data
def SetBin(value):
    return value.encode('hex')

def qSetBin(value):
    if len(value) %2 == 0:
        return _SetBin(value)

    else:

        print '不是16进制',value
        return value.encode('hex')

def _SetBin(value):
    for item in value:
        try:
            if int(item,16) < 15:
                pass
        except:
            print '不是16进制'
            return value.encode('hex')
    print '是16进制',value
    return value
