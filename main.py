# -*- coding: utf-8 -*-
import base64
import thread
import traceback

import wx,time,config
from wx.lib.embeddedimage import PyEmbeddedImage

from AndroidQQ import AndroidQQ
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class MyDialog(wx.Dialog):
   def __init__(self, parent, ImageBase):
      super(MyDialog, self).__init__(parent, title = u'验证码', size = (300,200))

      bitmap = PyEmbeddedImage(ImageBase).GetBitmap()
      labelqq = wx.StaticText(self, label=u'请输入验证码：',pos=(110,70))
      self.m_bitmap1 = wx.StaticBitmap(self, wx.ID_ANY, bitmap,pos=(80,10))
      self.text = wx.TextCtrl(self, size=(120,30),pos=(90,100))
      self.btn = wx.Button(self, wx.ID_OK, label = "ok", size = (80,30), pos = (110,138))
class Example(wx.Panel):
    def __init__(self,parent,QQClass):
        self.QQClass = QQClass

        self.STATUS = 0

        wx.Panel.__init__(self,parent=parent)


        mainsizer = wx.BoxSizer(wx.VERTICAL)
        headsizer = wx.BoxSizer(wx.HORIZONTAL)
        bodysizer = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, label=u'qq:')
        self.qqnumber = wx.TextCtrl(self, size=(120,25),value=u'188075889')
        label1 = wx.StaticText(self, label=u'mm:')
        self.qqmm = wx.TextCtrl(self, size=(120,25),value=u'qw6012827')
        self.login = wx.Button(self, label=u'登录', size=(80,32))
        self.Bind(wx.EVT_BUTTON,self.start,self.login)
        self.loginOut = wx.Button(self, label=u'退出', size=(80,32))
        labelX = wx.StaticText(self)





        headsizer.Add(label,flag=wx.EXPAND|wx.LEFT|wx.RIGHT| wx.TOP,border=10)
        headsizer.Add(self.qqnumber,flag=wx.EXPAND|wx.TOP,border=6)
        headsizer.Add(label1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT| wx.TOP,border=10)
        headsizer.Add(self.qqmm,flag=wx.EXPAND|wx.TOP,border=6)
        headsizer.Add(labelX,proportion=1)

        headsizer.Add(self.login,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=20)
        headsizer.Add(self.loginOut,flag=wx.EXPAND|wx.RIGHT,border=20)

        self.textview = wx.TextCtrl(self,-1,style=wx.TE_RICH|wx.TE_MULTILINE)
        bodysizer.Add(self.textview,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=10)
        mainsizer.Add(headsizer,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM,border=10)
        mainsizer.Add(bodysizer,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM,border=20)
        self.SetSizer(mainsizer)
    def start(self,event):
        if self.STATUS == 0:

            thread.start_new_thread(self._start,())
        else:
            self.STATUS = 0
            self.login.Enable()
            self.loginOut.Disable()
    def _start(self):
        self.login.Disable()
        self.STATUS = 1

        self.QQClass.login(self.qqnumber.GetValue(),self.qqmm.GetValue(),self)



    def log(self,data):

        self.textview.AppendText(time.strftime("%H:%M:%S")+':  '+data+'\n')

    def SetVerification(self,ImageHex):
        message = ''
        data = ImageHex.decode('hex')
        imagebase = base64.encodestring(data)
        dlg = MyDialog(self,imagebase)
        if dlg.ShowModal() == wx.ID_OK:
            print 'yes'
            message = dlg.text.GetValue()#获取文本框中输入的值
            return message
        dlg.Destroy()

class QQFriend(wx.Panel):
    def __init__(self,parent,QQClass):
        self.QQClass = QQClass
        wx.Panel.__init__(self,parent=parent)

        labelqq = wx.StaticText(self, label=u'目标qq：',pos=(10,20))
        self.qqnumber = wx.TextCtrl(self, size=(120,25),pos=(80,20),value=u'296603528')
        labelmsg = wx.StaticText(self, label=u'消息内容：',pos=(10,50))

        self.msgtextview = wx.TextCtrl(self, size=(120,25),pos=(80,50),value=u'你好啊')

        self.sendmsg = wx.Button(self, label=u'发送消息', pos=(40,80),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.SendMessage,self.sendmsg)

        labelqq1 = wx.StaticText(self, label=u'添加qq好友：',pos=(350,20))
        self.addqqnumber = wx.TextCtrl(self, size=(120,25),pos=(430,20),value=u'296603528')
        labelmsg1 = wx.StaticText(self, label=u'验证消息：',pos=(350,50))
        self.addmsgtextview = wx.TextCtrl(self, size=(120,25),pos=(430,50),value=u'你好啊')

        self.addfriend = wx.Button(self, label=u'添加好友', pos=(410,80),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.SendAddFriend,self.addfriend)

        name1 = wx.StaticText(self, label=u'分组名：',pos=(10,140))
        self.groupname = wx.TextCtrl(self, size=(120,25),pos=(70,140),value=u'test1')
        self.addgroupname = wx.Button(self, label=u'添加分组', pos=(40,180),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.Addgroupname,self.addgroupname)




        self.qqnumber_1 = wx.TextCtrl(self, size=(120,25),pos=(40,280),value=u'296603528')
        self.group_2 = wx.TextCtrl(self, size=(120,25),pos=(180,280),value=u'574240651')
        self.imgname_1 = wx.TextCtrl(self, size=(120,25),pos=(40,340),value=u'936ee06bd035095c991c5a2572614ae4')
        self.path_1 = wx.TextCtrl(self, size=(120,25),pos=(180,340),value=u'/7b9da5a3-8b5b-462f-a03c-eb9c6f37ebb8A')
        self.test = wx.Button(self, label=u'发送群成员图片消息', pos=(40,400),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.SendGroupMemberImageMsg,self.test)

        self.test1 = wx.Button(self, label=u'发送好友图片消息', pos=(150,400),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.SendGroupMemberImageMsg,self.test1)

    def SendImageMsg(self,event):
        self.QQClass.QQ.SendFriendImageMsg(self.qqnumber_1.GetValue(),self.imgname_1.GetValue(),self.path_1.GetValue())

    def SendGroupMemberImageMsg(self,event):
        self.QQClass.QQ.SendGroupMemberImageMsg(self.group_2.GetValue(),self.qqnumber_1.GetValue(),self.imgname_1.GetValue(),self.path_1.GetValue())

    def Addgroupname(self,event):
        self.QQClass.QQ.AddfriendGroup(self.groupname.GetValue())
    def SendMessage(self,event):
        self.QQClass.QQ.sendMsg(self.qqnumber.GetValue(),self.msgtextview.GetValue())
    def SendAddFriend(self,event):
        self.QQClass.QQ.Addfriend(self.addqqnumber.GetValue(),self.addmsgtextview.GetValue())


class QQGroup(wx.Panel):
    def __init__(self,parent,QQClass):
        self.QQClass = QQClass
        wx.Panel.__init__(self,parent=parent)

        labelqq = wx.StaticText(self, label=u'目标qq群：',pos=(10,20))
        self.qqgroup_number = wx.TextCtrl(self, size=(120,25),pos=(80,20),value=u'296603528')
        labelmsg = wx.StaticText(self, label=u'消息内容：',pos=(10,50))

        self.msgtextview = wx.TextCtrl(self, size=(120,25),pos=(80,50),value=u'你好啊')

        self.sendmsg = wx.Button(self, label=u'发送群消息', pos=(40,80),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.SendGroupMessage,self.sendmsg)

        labelqq1 = wx.StaticText(self, label=u'添加qq群：',pos=(350,20))
        self.addqqgroup_number = wx.TextCtrl(self, size=(120,25),pos=(420,20),value=u'475499084')
        labelmsg1 = wx.StaticText(self, label=u'验证消息：',pos=(350,50))
        self.addmsgtextview = wx.TextCtrl(self, size=(120,25),pos=(420,50),value=u'你好啊')

        self.addfriend = wx.Button(self, label=u'添加群', pos=(400,80),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.SendAddGroup,self.addfriend)

        labelqq2 = wx.StaticText(self, label=u'qq群号：',pos=(10,180))
        self.groupnumber = wx.TextCtrl(self, size=(120,25),pos=(70,175),value=u'296603528')
        self.but = wx.Button(self, label=u'获取群成员', pos=(50,210),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.GetGroupInfo,self.but)

        labelqq3 = wx.StaticText(self, label=u'目标qq群号：',pos=(10,280))
        self.groupnumber1 = wx.TextCtrl(self, size=(120,25),pos=(90,275),value=u'467949438')
        labelqq4 = wx.StaticText(self, label=u'成员qq号：',pos=(230,280))
        self.groupmembernumber = wx.TextCtrl(self, size=(120,25),pos=(310,275),value=u'296603528')
        self.Removes = wx.Button(self, label=u'踢出该成员', pos=(50,310),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.GroupRemovesMember,self.Removes)



        labelqq5 = wx.StaticText(self, label=u'目标qq群号：',pos=(10,360))
        self.groupnumber2 = wx.TextCtrl(self, size=(120,25),pos=(90,355),value=u'467949438')
        labelqq6 = wx.StaticText(self, label=u'群名片：',pos=(230,360))
        self.groupcardname= wx.TextCtrl(self, size=(120,25),pos=(310,355),value=u'test1123')
        self.setcardname = wx.Button(self, label=u'修改群名片', pos=(50,400),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.SetGroupCardName,self.setcardname)

        labelqq6 = wx.StaticText(self, label=u'目标qq群号：',pos=(10,460))
        self.groupnumber3 = wx.TextCtrl(self, size=(120,25),pos=(90,455),value=u'467949438')
        self.getgroupmanager = wx.Button(self, label=u'获取群主', pos=(50,500),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.GetGroupManager,self.getgroupmanager)


    def GetGroupManager(self,event):
        self.QQClass.QQ.GetGroupManager(self.groupnumber3.GetValue())
    def SetGroupCardName(self,event):
        self.QQClass.QQ.SetGroupCardName(self.groupcardname.GetValue(),self.groupnumber2.GetValue())
    def SendGroupMessage(self,event):
        self.QQClass.QQ.SendGroupMsg(self.qqgroup_number.GetValue(),self.msgtextview.GetValue())
    def SendAddGroup(self,event):
        self.QQClass.QQ.AddGroup(self.addqqgroup_number.GetValue(),self.addmsgtextview.GetValue())
    def GetGroupInfo(self,event):
        self.QQClass.QQ.GetGroupInfo(self.groupnumber.GetValue())
    def GroupRemovesMember(self,event):
        self.QQClass.QQ.GroupRemovesMember(self.groupnumber1.GetValue(),self.groupmembernumber.GetValue())
class Qzone(wx.Panel):
    def __init__(self,parent,QQClass):
        self.QQClass = QQClass
        wx.Panel.__init__(self,parent=parent)
        self.getfriendwidget = wx.Button(self, label=u'获取好友动态', pos=(40,80),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.SendGetfriendWidget,self.getfriendwidget)


        self.long = wx.TextCtrl(self, size=(120,25),pos=(40,180),value=u'120.01408900')
        self.lat =  wx.TextCtrl(self, size=(120,25),pos=(40,230),value=u'30.296275000')

        self.test = wx.Button(self,label=u'test', pos=(40,280),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.GetNearPeople,self.test)

        self.phone = wx.TextCtrl(self, size=(120,25),pos=(40,380),value=u'')

        self.but = wx.Button(self,label=u'test', pos=(40,480),size=(100,30))
        self.Bind(wx.EVT_BUTTON,self.GetQQnumber,self.but)
    def GetQQnumber(self,event):
        self.QQClass.QQ.GetQQnumber(self.phone.GetValue())

    def SendGetfriendWidget(self,event):
        self.QQClass.QQ.GetfriendWidget()
    def GetNearPeople(self,event):
        long = float(self.long.GetValue())
        lat = float(self.lat.GetValue())
        self.QQClass.QQ.GetNearPeople(long,lat)
    def GetNearPeople2(self,event):
        self.QQClass.QQ.GetNearPeople2()
class Search(wx.Panel):
    def __init__(self,parent,QQClass):
        self.QQClass = QQClass
        wx.Panel.__init__(self,parent=parent)
        label = wx.StaticText(self, label=u'关键词：',pos=(240,23))
        self.textview = wx.TextCtrl(self, size=(120,25),pos=(310,20),value=u'--')
        self.Searchkey = wx.Button(self, label=u'搜索', pos=(440,18),size=(80,30))
        self.Bind(wx.EVT_BUTTON,self.SendSearchkey,self.Searchkey)
    def SendSearchkey(self,event):
        self.QQClass.QQ.GetSearchkey(self.textview.GetValue())
class Setting(wx.Panel):
    def __init__(self,parent,QQClass):
        self.QQClass = QQClass
        wx.Panel.__init__(self,parent=parent)
        self.check = wx.CheckBox(self,label=u'自动通过好友添加请求',pos=(30,30),size=(150,20))
        self.check.SetValue(True)
        self.check1 = wx.CheckBox(self,label=u'自动通过申请加入群请求',pos=(30,60),size=(150,20))
        self.check1.SetValue(False)
        self.check.Bind(wx.EVT_CHECKBOX,self.Autofriend)
        self.check1.Bind(wx.EVT_CHECKBOX,self.AutoGroup)
    def Autofriend(self,event):
        config.AutoAgreeAddFriend = self.check.GetValue()
    def AutoGroup(self,event):
        config.AutoAgreeAddFriend = self.check1.GetValue()

class QQ:
    def __int__(self):
        pass
    def login(self,qqnum,qqmm,window):
        self.QQ = AndroidQQ(qqnum,qqmm,window)
        self.QQ.login()
if __name__ == "__main__":
    QQClass = QQ()
    app = wx.App()
    frame = wx.Frame(None,title=u'qq',size=(800,600))
    nb = wx.Notebook(frame)
    nb.AddPage(Example(nb,QQClass),u'登录')
    nb.AddPage(QQFriend(nb,QQClass),u'好友功能')
    nb.AddPage(QQGroup(nb,QQClass),u'群功能')
    nb.AddPage(Qzone(nb,QQClass),u'空间功能')
    nb.AddPage(Search(nb,QQClass),u'搜索好友')
    nb.AddPage(Setting(nb,QQClass),u'设置')
    frame.Show()
    app.MainLoop()