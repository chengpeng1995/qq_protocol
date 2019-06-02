# -*- coding: utf-8 -*-


#-----------------设备信息--------------

DEVICE_NAME = 'Lenovo A820t'
DEVICE_IMEI = '866819027236128'
DEVICE_VERSION = '4.4.4'

#----------------基本设置---------------
msgCookies = 'B6CC78FC' #16进制
ImgServerUrl = ''
AutoAgreeAddFriend = True
AutoAgreeGroup = False

#-------------------常量-----------------
login_state_logining = 0
login_state_veriy = 1
login_state_success = 2
TYPE_BYTE = 0
TYPE_SHORT = 1
TYPE_INT = 2
TYPE_LONG = 3
TYPE_FLOAT = 4
TYPE_DOUBLE = 5
TYPE_STRING1 = 6
TYPE_STRING4 = 7
TYPE_MAP = 8
TYPE_LIST = 9
TYPE_STRUCT_BEGIN = 10
TYPE_STRUCT_END = 11
TYPE_ZERO_TAG = 12
TYPE_SIMPLE_LIST = 13


class JceMap(object):
    key_type = 0
    key = ''
    value_type = 0
    value = ''

