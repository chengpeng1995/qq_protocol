# -*- coding: utf-8 -*-
from Tools import Coder
import config
from mode import Pack
def WriteInt(value,tag):
    if value >= -32768 and value <= 32768:
        return WriteShort(value,tag)
    else:
        return WriteHead(config.TYPE_INT,tag) + Pack.SetInt (value)
def WriteShort(value, tag):
    if value>= -128 and value <= 127:
        return WriteByte(value,tag)
    else:
        return WriteHead(config.TYPE_SHORT,tag) + Pack.SetShort (value)
def WriteHead(value, tag):
    if tag >= 15:
        _value = value | 240
        return Pack.SetByte (_value) + Pack.SetByte (tag)
    else:
        _value = value | (tag << 4)
        return Pack.SetByte (_value)

def WriteByte(value, tag):
    if value == 0:
        return WriteHead(config.TYPE_ZERO_TAG,tag)
    else:

        return WriteHead(config.TYPE_BYTE,tag) + Pack.SetByte(value)
def WriteStringByte(value,tag):
    t_value = str(value)

    if len(t_value) > 255:
        return WriteHead(config.TYPE_STRING4,tag) + Pack.SetInt(len(t_value)) + Pack.SetBin(t_value)
    else:
        return WriteHead(config.TYPE_STRING1,tag) + Pack.SetByte(len(t_value)) + Pack.SetBin(t_value)
def WriteSimpleList(value,tag):
    data = ''
    data += WriteHead(config.TYPE_SIMPLE_LIST,tag)
    data += WriteHead(0, 0)
    data += WriteInt(len(str(value)), 0)
    data += Pack.SetBin(value)
    return data
def WriteLong(value,tag):
    if value >= -2147483648 and value <= 2147483648:
        return WriteInt(int(value),tag)
    else:
        return WriteHead(config.TYPE_LONG,tag)+Pack.SetLong(value)
def WriteObj(type,value,tag):
    if type == config.TYPE_BYTE:
        return WriteByte(int(value),tag)
    elif type == config.TYPE_SHORT:
        return WriteShort(int(value),tag)
    elif type == config.TYPE_INT:
        return WriteInt(int(value),tag)
    elif type == config.TYPE_LONG:
        return WriteLong(int(value),tag)
    elif type == config.TYPE_SIMPLE_LIST:
        return WriteSimpleList(value,tag)
    elif type == config.TYPE_MAP:
        print '没有map'
    elif type == config.TYPE_STRING1:
        return WriteStringByte(value,tag)
    elif type == config.TYPE_LIST:
        return WriteList(str(value),tag)
    elif type == config.TYPE_STRING4:
        return WriteStringByte(str(value),tag)
def WriteList(value,tag):
    data = ''
    data += WriteHead(config.TYPE_LIST,tag)
    data += WriteInt(len(value),0)
    for item in value:
        print item
        data += '00'+item.encode('hex')
    return data
def WriteJceStruct(value,tag):
    data = ''

    data += WriteHead(config.TYPE_STRUCT_BEGIN,tag)
    data += Pack.SetBin(value)
    data += WriteHead(config.TYPE_STRUCT_END,0)
    return data
def WriteMap(data,tag):
    key_type = data.key_type
    key = data.key
    value_type = data.value_type
    value = data.value
    data = ''
    data += WriteHead(config.TYPE_MAP,tag)
    data += WriteShort(1,0)
    data += WriteObj(key_type,key,0)
    data += WriteObj(value_type,value,1)
    return data

def _WriteMap(key,key_type,value,value_type,tag):
    data = ''
    data += WriteHead(config.TYPE_MAP,tag)
    data += WriteShort(1,0)
    data += WriteStringByte(key,0)
    data += WriteSimpleList(value,1)
    print data

