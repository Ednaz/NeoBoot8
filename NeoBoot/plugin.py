#!/usr/bin/python
# -*- coding: utf-8 -*-  
####################### _(-_-)_ gutosie _(-_-)_ ####################### 
                                 
#neoboot modules
from __init__ import _
from Plugins.Extensions.NeoBoot.files.stbbranding import getLabelDisck, getINSTALLNeo, getNeoLocation, getNeoMount, getNeoMount2, getFSTAB, getFSTAB2, getKernelVersionString, getKernelImageVersion, getCPUtype, getCPUSoC,  getImageNeoBoot, getBoxVuModel, getBoxHostName, getTunerModel                    
from Plugins.Extensions.NeoBoot.files import Harddisk
from Components.About import about                                                                                                                                                    
from enigma import getDesktop
from enigma import eTimer
from Screens.Screen import Screen                                                                                                                                               
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.Standby import TryQuitMainloop
from Components.About import about
from Components.Sources.List import List
from Components.Button import Button
from Components.ActionMap import ActionMap, NumberActionMap
from Components.GUIComponent import *
from Components.MenuList import MenuList
from Components.Input import Input
from Components.Label import Label
from Components.ProgressBar import ProgressBar
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap, MultiPixmap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, pathExists, createDir, resolveFilename, SCOPE_PLUGINS
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen
from os.path import dirname, isdir, isdir as os_isdir
import os
import time
# Copyright (c) , gutosie  license
# 
# Redystrybucja wersji programu i dokonywania modyfikacji JEST DOZWOLONE, pod warunkiem zachowania niniejszej informacji o prawach autorskich. 
# Autor NIE ponosi JAKIEJKOLWIEK odpowiedzialności za skutki użtkowania tego programu oraz za wykorzystanie zawartych tu informacji.
# Modyfikacje przeprowadzasz na wlasne ryzyko!!!
# O wszelkich zmianach prosze poinformować na  http://all-forum.cba.pl   w temacie pod nazwa  	 -#[NEOBOOT]#-

# This text/program is free document/software. Redistribution and use in
# source and binary forms, with or without modification, ARE PERMITTED provided
# save this copyright notice. This document/program is distributed WITHOUT any
# warranty, use at YOUR own risk.

PLUGINVERSION = '8.00'
UPDATEVERSION = '8.06'

def Freespace(dev):
    statdev = os.statvfs(dev)
    space = statdev.f_bavail * statdev.f_frsize / 1024
    print '[NeoBoot] Free space on %s = %i kilobytes' % (dev, space)
    return space


#def Log(param = '')
	

class MyUpgrade(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="center,center" size="1280,570" title="Tools Neoboot">
                  <ePixmap position="594,226" zPosition="-2" size="623,313" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />
                  <widget source="list" render="Listbox" position="33,127" size="1229,82" scrollbarMode="showOnDemand">
                  <convert type="TemplatedMultiContent">\
                    {"template": [MultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                                  MultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
                                 ],
                                 "fonts": [gFont("Regular", 40)],
                                 "itemHeight": 66
                    }
                  </convert>
                  </widget>
                  <eLabel text="NeoBoot wykry\xc5\x82 nowsz\xc4\x85 wersj\xc4\x99. " font="Regular; 40" position="27,40" size="1042,70" halign="center" foregroundColor="red" backgroundColor="black" transparent="1" />
                  <eLabel text="EXIT - Zrezygnuj" font="Regular; 40" position="27,441" size="389,80" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
                </screen>"""
    else:
        skin = """<screen position="center,center" size="1127,569" title="Tools NeoBoot">
                  <ePixmap position="492,223" zPosition="-2" size="589,298" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />
                  <widget source="list" render="Listbox" position="18,122" size="1085,82" scrollbarMode="showOnDemand">
                    <convert type="TemplatedMultiContent">
                      {"template": [MultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
                                    MultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
                                   ],
                                   "fonts": [gFont("Regular", 40)],
                                   "itemHeight": 66
                      }
                    </convert>
                  </widget>
                  <eLabel text="NeoBoot wykry\xc5\x82 nowsz\xc4\x85 wersj\xc4\x99 wtyczki. " font="Regular; 40" position="27,40" size="1042,70" halign="center" foregroundColor="red" backgroundColor="black" transparent="1" />
                  <eLabel text="EXIT - Zrezygnuj" font="Regular; 40" position="27,441" size="389,80" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
                </screen>"""
    __module__ = __name__

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.wybierz()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.changever})

    def changever(self):
		
        ImageChoose = self.session.open(NeoBootImageChoose)
        if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'):
            out = open('%sImageBoot/.version' % getNeoLocation(), 'w')
            out.write(PLUGINVERSION)
            out.close()
            self.close()
        else:
            self.close(self.session.open(MessageBox, _('No file location NeoBot, do re-install the plugin.'), MessageBox.TYPE_INFO, 10))
            self.close()
        return ImageChoose

    def wybierz(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('Update neoboot in all images ?'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
		
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(MyUpgrade2):
            pass
        self.close()


class MyUpgrade2(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center,center" size="900,450" title="NeoBoot"><widget name="lab1" position="23,42" size="850,350" font="Regular;35" halign="center" valign="center" transparent="1"/></screen>'
    else:
        skin = '<screen position="center,center" size="400,200" title="NeoBoot"><widget name="lab1" position="10,10" size="380,180" font="Regular;24" halign="center" valign="center" transparent="1"/></screen>'

    def __init__(self, session):		
        Screen.__init__(self, session)
        self['lab1'] = Label(_('NeoBoot: Upgrading in progress\nPlease wait...'))
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.updateInfo)
        self.onShow.append(self.startShow)

    def startShow(self):		
        self.activityTimer.start(10)

    def updateInfo(self):		
        self.activityTimer.stop()
        f2 = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'r')
        mypath2 = f2.readline().strip()
        f2.close()
        if fileExists('/.multinfo'):
            self.myClose(_('Sorry, NeoBoot can installed or upgraded only when booted from Flash.'))
            self.close()
        elif mypath2 != 'Flash':
            self.myClose(_('Sorry, NeoBoot can installed or upgraded only when booted from Flash.'))
            self.close()
        else:
            for fn in listdir('%sImageBoot' % getNeoLocation() ):
                dirfile = '%sImageBoot/ ' % getNeoLocation() + fn
                if isdir(dirfile):
                    target = dirfile + '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
                    cmd = 'rm -r ' + target + ' > /dev/null 2>&1'
                    system(cmd)
                    cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot ' + target
                    system(cmd)
          
            out = open('%sImageBoot/.version' % getNeoLocation(), 'w')
            out.write(PLUGINVERSION)
            out.close()
            self.myClose(_('NeoBoot successfully updated. You can restart the plugin now.\nHave fun !!!'))


    def myClose(self, message):				
        ImageChoose = self.session.open(NeoBootImageChoose)
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close(ImageChoose)


class MyHelp(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="center,center" size="1920,1080" borderWidth="0" borderColor="transpBlack" flags="wfNoBorder">
                    <eLabel text="INFORMACJE NeoBoot" font="Regular; 35" position="71,20" size="1777,112" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
                    <widget name="lab1" position="69,134" size="1780,913" font="Regular;35"    />
                  </screen>"""
    else:
        skin = """<screen position="center,center" size="1280,720" title="NeoBoot - Informacje">
                    <widget name="lab1" position="18,19" size="1249,615" font="Regular;20" backgroundColor="black" transparent="1" />
                  </screen>"""
    __module__ = __name__

    def __init__(self, session):
		
        Screen.__init__(self, session)
        self['lab1'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'back': self.close,
         'ok': self.close,
         'up': self['lab1'].pageUp,
         'left': self['lab1'].pageUp,
         'down': self['lab1'].pageDown,
         'right': self['lab1'].pageDown})
        self['lab1'].hide()
        self.updatetext()

    def updatetext(self):
		
        message = _('NeoBoot Ver. ' + PLUGINVERSION + '  Enigma2\n\nDuring the entire installation process does not restart the receiver !!!\n\n')
        message += _('NeoBoot Ver. updates ' + UPDATEVERSION + '  \n\n')
        message = _('For proper operation NeoBota type device is required USB stick or HDD, formatted on your system files Linux ext3 or ext4..\n\n')
        message += _('1. If you do not have a media formatted with the ext3 or ext4 is open to the Device Manager <Initialize>, select the drive and format it.\n\n')
        message += _('2. Go to the device manager and install correctly hdd and usb ...\n\n')
        message += _('3. Install NeoBota on the selected device.\n\n')
        message += _('4. Install the needed packages...\n\n')
        message += _('5. For proper installation XenoBota receiver must be connected to the Internet.\n\n')
        message += _('6. In the event of a problem with the installation cancel and  inform the author of the plug of a problem.\n\n')
        message += _('Have fun !!!')
        self['lab1'].show()
        self['lab1'].setText(message)


class Opis(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="center,center" size="1920,1080" flags="wfNoBorder">
                  <ePixmap position="0,0" zPosition="-1" size="1920,1080" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame_base-fs8.png"  />
                  <widget source="session.VideoPicture" render="Pig" position=" 1253,134" size="556,313" zPosition="3" backgroundColor="#ff000000"/>
                  <eLabel text="INFORMACJE NeoBoot" position="340,50"  size="500,55" font="Regular;40" halign="left" foregroundColor="#58bcff" backgroundColor="black" transparent="1"/>
                  <widget name="key_red" position="30,950" size="430,50" zPosition="1" font="Regular; 30" halign="center" backgroundColor="red" transparent="1" foregroundColor="white" />
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/scroll.png" position="1144,160" size="26,685" zPosition="5" alphatest="blend"/>
                  <ePixmap position="1350,750" zPosition="1" size="400,241" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" />
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="100,1000" size="230,36" alphatest="blend" />
                  <widget name="lab1" position="100,160" size="1070,680" font="Regular; 30"  backgroundColor="black" transparent="1" />
                </screen>"""                  		 		   		
    else:
        skin = """<screen position="center,center" size="1280,720" title="NeoBoot - Informacje">
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1frame_base-fs8.png"  position="0,0" zPosition="-1" size="1280,720" />
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="50,680" size="230,36" alphatest="blend"  />
                  <widget name="key_red" position="35,630" zPosition="1" size="270,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
                  <widget name="lab1" position="50,100" size="730,450" font="Regular;20" backgroundColor="black"  />
                  <widget source="session.VideoPicture" render="Pig" position=" 836,89" size="370,208" zPosition="3" backgroundColor="#ff000000" />
                  <widget source="Title" render="Label"  position="200,25" size="800,30" font="Regular;28" halign="left" foregroundColor="#58bcff" backgroundColor="transpBlack" transparent="1"/>
                  <ePixmap position="920,520" zPosition="1" size="228,130" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1matrix.png" />
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/scroll.png" position="754,100" size="26,455" zPosition="5" alphatest="blend" backgroundColor="black" transparent="1" />
                </screen>"""
    __module__ = __name__

    def __init__(self, session):		
        Screen.__init__(self, session)
        self['key_red'] = Label(_('Remove NeoBoot of STB'))
        self['lab1'] = ScrollLabel('')
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'back': self.close,
         'red': self.delete,
         'ok': self.close,
         'up': self['lab1'].pageUp,
         'left': self['lab1'].pageUp,
         'down': self['lab1'].pageDown,
         'right': self['lab1'].pageDown})
        self['lab1'].hide()
        self.updatetext()

    def updatetext(self):		
        message = _('NeoBoot Ver. ' + PLUGINVERSION + '\n\n')
        message += _('NeoBoot Ver. updates ' + UPDATEVERSION + '\n\n')
        message += _('1. Requirements: For proper operation of the device NeoBota are required USB stick or HDD.\n\n')
        message += _('2. NeoBot is fully automated\n\n')
        message += _('3. To install a new image in MultiBocie should be sent by FTP software file compressed in ZIP or NIF to the folder: \n%sImagesUpload and remote control plugin NeoBoot use the green button <Installation>\n\n')
        message += _('4. For proper installation and operation of additional image multiboot, use only the image intended for your receiver. !!!\n\n')
        message += _('5. By installing the multiboot images of a different type than for your model STB DOING THIS AT YOUR OWN RISK !!!\n\n')
        message += _('6. The installed to multiboot images, it is not indicated update to a newer version.\n\n')
        message += _('The authors plug NeoBot not liable for damage a receiver, NeoBoota incorrect use or installation of unauthorized additions or images.!!!\n\n')
        message += _('Have fun !!!')
        message += _('\nCompletely uninstall NeoBota: \nIf you think NeoBot not you need it, you can uninstall it.\nTo uninstall now press the red button on the remote control.\n\n')
        self['lab1'].show()
        self['lab1'].setText(message)

    def delete(self):		
        message = _('Are you sure you want to completely remove NeoBoota of your image?\n\nIf you choose so all directories NeoBoota will be removed.\nA restore the original image settings Flash.')
        ybox = self.session.openWithCallback(self.mbdelete, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle(_('Removed successfully.'))

    def mbdelete(self, answer):		
        if answer is True:
            cmd = "echo -e '\n\n%s '" % _('Recovering setting....\n')
            cmd1 = 'rm -R /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot; rm -R %sImageBoot/.Flash; rm -R %sImageBoot/.neonextboot; rm -R %sImageBoot/.version'
            cmd2 = 'rm -R /sbin/neoinit*'
            cmd3 = 'ln -sfn /sbin/init.sysvinit /sbin/init'     
            cmd4 = 'opkg install volatile-media; sleep 2; killall -9 enigma2'  
            self.session.open(Console, _('NeoBot was removed !!! \nThe changes will be visible only after complete restart of the receiver.'), [cmd,
             cmd1,
             cmd2,
             cmd3,
             cmd4,])
            self.close()

          
class NeoBootInstallation(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="410,138" size="1200,850" title="NeoBoot">
                    <widget name="label3" position="10,632" size="1178,114" zPosition="1" halign="center" font="Regular;35" backgroundColor="black" transparent="1" foregroundColor="blue" />
                    <ePixmap position="643,282" zPosition="-2" size="531,331" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />
                    <eLabel position="15,76" size="1177,2" backgroundColor="blue" foregroundColor="blue" name="linia" /><eLabel position="10,622" size="1168,3" backgroundColor="blue" foregroundColor="blue" name="linia" />
                    <eLabel position="14,752" size="1168,3" backgroundColor="blue" foregroundColor="blue" name="linia" /><eLabel position="15,276" size="1183,2" backgroundColor="blue" foregroundColor="blue" name="linia" />
                    <widget name="label1" position="14,4" size="1180,62" zPosition="1" halign="center" font="Regular;35" backgroundColor="black" transparent="1" foregroundColor="red" />
                    <widget name="label2" position="15,82" size="1178,190" zPosition="1" halign="center" font="Regular;35" backgroundColor="black" transparent="1" foregroundColor="blue" />
                    <widget name="config" position="15,285" size="641,329" font="Regular; 32" itemHeight="42" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" scrollbarMode="showOnDemand" />
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" position="48,812" size="140,28" alphatest="on" />
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" position="311,816" size="185,28" alphatest="on" />
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellowcor.png" position="614,815" size="150,28" alphatest="on" />
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/bluecor.png" position="958,817" size="140,26" alphatest="on" />
                    <widget name="key_red" position="19,760" zPosition="1" size="221,47" font="Regular; 35" halign="center" valign="center" backgroundColor="red" transparent="1" foregroundColor="red" />
                    <widget name="key_green" position="289,761" zPosition="1" size="227,47" font="Regular; 35" halign="center" valign="center" backgroundColor="green" transparent="1" foregroundColor="green" />
                    <widget name="key_yellow" position="583,760" zPosition="1" size="224,51" font="Regular; 35" halign="center" valign="center" backgroundColor="yellow" transparent="1" foregroundColor="yellow" />
                    <widget name="key_blue" position="856,761" zPosition="1" size="326,52" font="Regular; 35" halign="center" valign="center" backgroundColor="blue" transparent="1" foregroundColor="blue" />
                </screen>"""
    else:
        skin = """<screen position="center, center" size="835, 500" title="NeoBoot">
        <ePixmap position="0,0" zPosition="-1" size="835,500" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame835x500.png"  />
        <widget name="label1" position="10,15" size="840,30" zPosition="1" halign="center" font="Regular;25" foregroundColor="red" backgroundColor="black" transparent="1" />
        \n  <widget name="label2" position="7,100" size="840,296" zPosition="1" halign="center" font="Regular;20" backgroundColor="black" foregroundColor="#58ccff" transparent="1"/>
        <widget name="config" position="220,200" size="440,207" backgroundColor="black" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor1.png" scrollbarMode="showOnDemand"  />
        <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" position="48,406" size="140,40" alphatest="on"    />
        \n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" position="246,406" size="140,40" alphatest="on" />
        \n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellowcor.png" position="474,406" size="150,40" alphatest="on" />
        \n  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/bluecor.png" position="675,406" size="140,40" alphatest="on" />
        \n  <widget name="key_red" position="48,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />
        \n  <widget name="key_green" position="248,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />
        \n  <widget name="key_yellow" position="474,406" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="yellow" transparent="1" />
        \n  <widget name="key_blue" position="672,415" zPosition="1" size="145,45" font="Regular;20" halign="center" valign="center" backgroundColor="blue" transparent="1" />
        \n  <widget name="label3" position="20,339" size="816,61" zPosition="1" halign="center" font="Regular;24" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Instruction'))
        self['key_green'] = Label(_('Installation'))
        self['key_yellow'] = Label(_('Info disc'))
        self['key_blue'] = Label(_('Device Manager'))
        self['label1'] = Label(_('Welcome to NeoBoot %s Plugin installation.') % PLUGINVERSION)
        self['label3'] = Label(_('WARNING !!! First, mount the device.'))
        self['label2'] = Label(_('Here is the list of mounted devices in Your STB\nPlease choose a device where You would like to install NeoBoot'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'DirectionActions'], {'red': self.Instrukcja,                  
         'green': self.install,
         'yellow': self.datadrive,
         'blue': self.devices, 
         'back': self.close})             
        self.updateList()
                
    def Instrukcja(self):
        self.session.open(MyHelp)

    def datadrive(self):
        try:
            message = "echo -e '\n"
            message += _('NeoBot checks the connected media.\nWAIT ...\n\nDISCS:')
            message += "'"
            os.system(" 'mount | sed '/sd/!d' | cut -d" " -f1,2,3,4,5' ")
            cmd = '/sbin/blkid '
            system(cmd)
            print '[MULTI-BOOT]: ', cmd
            self.session.open(Console, _('    NeoBot - Available media:'), [message, cmd])
            if fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom'):
                if not fileExists('%sImageBoot/.version' % getNeoLocation()):
                    os.system('mkdir -p %s; sync; chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom' % getNeoLocation())
            else:
                pass
        except:
            pass

    def updateList(self):
        if fileExists('/proc/mounts'):
            with open('/proc/mounts', 'r') as f:
                for line in f.readlines():
                    if line.startswith('/dev/sd') and line.find('/media/neoboot') == -1 and (line.find('ext4') != -1 or line.find('ext3') != -1):
                        try: self.list.append(line.split(' ')[1] + '/')
                        except Exception: pass # nie powinno sie zdarzyc, ale w razie czego
        if len(self.list) == 0:
            self['label2'].setText(_('Sorry it seems that there are not Linux formatted devices mounted on your STB. To install NeoBoot you need a Linux formatted part1 device. Click on the blue button to open Devices Panel'))
        self['config'].setList(self.list)
 
    def checkReadWriteDir(self, configele):
        from Plugins.Extensions.NeoBoot.files import Harddisk
        import os.path
        import Plugins.Extensions.NeoBoot.files.Harddisk
        supported_filesystems = frozenset(('ext4', 'ext3', 'ext2', 'ntfs', 'nfs', ))
        candidates = []
        mounts = Harddisk.getProcMounts()
        for partition in Harddisk.harddiskmanager.getMountedPartitions(False, mounts):
            if partition.filesystem(mounts) in supported_filesystems:
                candidates.append((partition.description, partition.mountpoint))

        if candidates:
            locations = []
            for validdevice in candidates:
                locations.append(validdevice[1])

            if Harddisk.findMountPoint(os.path.realpath(configele)) + '/' in locations or Harddisk.findMountPoint(os.path.realpath(configele)) in locations:
                if fileExists(configele, 'w'):
                    return True
                else:
                    check = False
                    if check == False:
                        message = _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.')
                        message += _('Do you want install NeoBoot ?\n')
                        ybox = self.session.openWithCallback(self.install, MessageBox, message, MessageBox.TYPE_YESNO)
                        ybox.setTitle(_('Install Manager'))
                    else:
                        dir = configele
                        self.session.open(MessageBox, _('The directory %s is not writable.\nMake sure you select a writable directory instead.') % dir, type=MessageBox.TYPE_ERROR)
                        return False
            else:
                check = False
                if check == False:
                    message = _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.')
                    message += _('Do you want install NeoBoot ?\n')
                    ybox = self.session.openWithCallback(self.install, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Install Manager'))
                else:
                    dir = configele
                    self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
                    return False
        else:

            check = False
            if check == False:
                message = _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.')
                message += _('Do you want install NeoBoot ?\n')
                ybox = self.session.openWithCallback(self.install, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Manager'))
            else:
                dir = configele
                self.session.open(MessageBox, _('The directory %s is not a EXT2, EXT3, EXT4 or NFS partition.\nMake sure you select a valid partition type.') % dir, type=MessageBox.TYPE_ERROR)
                return False


    def devices(self):
        check = False
        if check == False:
            message = _('After selecting OK start Mounting Manager, option Mount - green\n')
            message += _('Do you want to run the manager to mount the drives correctly ?\n')
            ybox = self.session.openWithCallback(self.device2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Device Manager'))

    def device2(self, yesno):
        if yesno:
            if fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager*/devicemanager.cfg'):
                system('rm -f /usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager*/devicemanager.cfg; touch /usr/lib/enigma2/python/Plugins/SystemPlugins/DeviceManager*/devicemanager.cfg')
            if fileExists('/etc/devicemanager.cfg'):
                system(' rm -f /etc/devicemanager.cfg; touch /etc/devicemanager.cfg ')
            from Plugins.Extensions.NeoBoot.files.devices import ManagerDevice
            self.session.open(ManagerDevice)
        else:
            self.close()

    def install(self):
        #if getFSTAB2() != 'OKinstall':
            #self.session.open(MessageBox, _('NeoBot - First use the Device Manager and mount the drives correctly !!!'), MessageBox.TYPE_INFO, 7)
            #self.close()
        #else:
            self.first_installation()

    def first_installation(self):
        check = False
        if fileExists('/proc/mounts'):
            with open('/proc/mounts', 'r') as f:
                for line in f.readlines():
                    if line.startswith('/dev/sd') and line.find('/media/neoboot') == -1 and (line.find('ext4') != -1 or line.find('ext3') != -1):
                        check = True
                        break

        if check == False:
            self.session.open(MessageBox, _('Sorry, there is not any connected devices in your STB.\nPlease connect HDD or USB to install NeoBoot!'), MessageBox.TYPE_INFO)
        else:
            #if getFSTAB2() != 'OKinstall':
                #self.session.open(MessageBox, _('Device Manager encountered an error, disk drives not installed correctly !!!'), MessageBox.TYPE_INFO)
                #self.close()
            self.mysel = self['config'].getCurrent()
            if self.checkReadWriteDir(self.mysel):
                message = _('Do You really want to install NeoBoot in:\n ') + self.mysel + '?'
                ybox = self.session.openWithCallback(self.install2, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Install Confirmation'))
            else:
                self.close()
################# Next Install #################

    def install2(self, yesno):		
        print 'yesno:', yesno
        if yesno:                 
            self.first_installationNeoBoot()
        else:
            self.myclose2(_('NeoBoot has not been installed ! :(' ))

    def first_installationNeoBoot(self):
    	    self.mysel = self['config'].getCurrent()	    
            system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; chmod 0755 ./bin/neoini*; chmod 0755 ./ex_init.py; chmod 0755 ./target/*.sh; chmod 0755 ./files/NeoBoot.sh; chmod 0755 ./files/S50fat.sh; cp -rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoini* /sbin cd;')                                    
            cmd1 = 'mkdir ' + self.mysel + 'ImageBoot;mkdir ' + self.mysel + 'ImagesUpload' 
            system(cmd1)
            cmd2 = 'mkdir ' + self.mysel + 'ImageBoot;mkdir ' + self.mysel + 'ImagesUpload/.kernel' 
            system(cmd2)
                                               
            if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'): 
                    os.system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location' )  
                    
            if fileExists('/proc/mounts'):
                fileExists('/proc/mounts')
                f = open('/proc/mounts', 'r')
                for line in f.readlines():
                    if line.find(self.mysel):
                        mntdev = line.split(' ')[0]
                f.close()                
                mntid = os.system('blkid -s UUID -o value ' + mntdev + '>/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install')
                os.system('blkid -s UUID -o value ' + mntdev + '>/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install')                

                if getFSTAB() != 'OKinstall':                                  
                    os.system('blkid -c /dev/null ' + mntdev + ' > /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install')                    
                if getFSTAB() != 'OKinstall':                                  
                    os.system('blkid -c /dev/null /dev/sd* > /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install')
                if getFSTAB() != 'OKinstall':                                  
                    os.system('blkid -c /dev/null /dev/sd* > /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install')                                                                    
                    f2 = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install', 'r')
                    for line2 in f2.readlines():
                        if line2.find(self.mysel):
                            mntdev2 = line2.split(' ')[0][0:-1]                              
                    f2.close()                                  
                    os.system(' echo ' + mntdev2 + '   > /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install')
                                        
            out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'w')
            out.write(self.mysel)
            out.close()

            os.system('sleep 2')                                          

            if os.path.isfile('%sImageBoot/.neonextboot' % getNeoLocation()): 
                    os.system('rm -f /etc/neoimage; rm -f /etc/imageboot; rm -f %sImageBoot/.neonextboot; rm -f %sImageBoot/.version; rm -f %sImageBoot/.Flash; ' % (getNeoLocation(), getNeoLocation(), getNeoLocation()) )
            if os.path.isfile('%sImagesUpload/.kernel/zImage*.ipk or %sImagesUpload/.kernel/zImage*.bin' % ( getNeoLocation(),getNeoLocation()) ): 
                        os.system('rm -f %sImagesUpload/.kernel/zImage*.ipk; rm -f %sImagesUpload/.kernel/zImage*.bin' % ( getNeoLocation(),getNeoLocation()) )
                    
            if fileExists('/etc/issue.net'):
                try:
                    lines = open('/etc/hostname', 'r').readlines()
                    imagename = lines[0][:-1]
                    image = imagename
                    open('%sImageBoot/.Flash' % getNeoLocation(), 'w').write(image)
                except:
                    False
                                
            out1 = open('%sImageBoot/.version' % getNeoLocation(), 'w')
            out1.write(PLUGINVERSION)
            out1.close()
                        
            out2 = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'w')
            out2.write('Flash ')
            out2.close()

            out3 = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.neo_info', 'w')
            out3.write('Kernel\n')
            out3.write('Kernel-Version: ' + about.getKernelVersionString() + '\n')
            out3.write('NeoBoot\n')
            out3.write('NeoBoot-Version: ' + PLUGINVERSION + '\n')
            out3.close() 
                                                                                 
            os.system('echo "mount -a" >> /etc/init.d/mdev')


            system('opkg update; chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/install; blkid -c /dev/null /dev/sd* > /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/installblkid; chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/installblkid ')                                         
                                           
            if os.system('opkg list-installed | grep python-subprocess') != 0:
                            os.system('opkg install python-subprocess')
            if os.system('opkg list-installed | grep python-argparse') != 0:
                            os.system('opkg install python-argparse')
            if os.system('opkg list-installed | grep curl') != 0:
                            os.system('opkg install curl')    
            if os.system('opkg list-installed | grep packagegroup-base-nfs') != 0:                            
                            os.system('opkg install packagegroup-base-nfs')                       
            if os.system('opkg list-installed | grep ofgwrite') != 0:                                                                                                                                                                                                                                                                                                                                                
                            os.system('opkg install ofgwrite')
            if os.system('opkg list-installed | grep bzip2') != 0:                                                                                                                                                                                                                                                                                                                                                
                            os.system('opkg install bzip2')
            if os.system('opkg list-installed | grep mtd-utils') != 0:
                            os.system('opkg install mtd-utils')
            if os.system('opkg list-installed | grep mtd-utils-ubifs') != 0:                                                                                                                                                                                                                                                                                                                                                
                            os.system('opkg install mtd-utils-ubifs')
            if os.system('opkg list-installed | grep mtd-utils-jffs2') != 0:
                            os.system('opkg install mtd-utils-jffs2')
            if os.system('opkg list-installed | grep kernel-module-nandsim') != 0:
                            os.system('opkg install kernel-module-nandsim')                          
            if os.system('opkg list-installed | grep lzo') != 0:                            
                            os.system('opkg install lzo') 
            if os.system('opkg list-installed | grep python-setuptools') != 0:                            
                            os.system('opkg install python-setuptools')                             
            if os.system('opkg list-installed | grep util-linux-sfdisk') != 0: 
                            os.system('opkg install util-linux-sfdisk') 
            

            # ARM - OctagonSF4008 - DM900 - Zgemma h7S - Octagon sf 8008 - AX HD60 4K  #gbquad4k  arm , #osmio4k  arm, #Zgemma h9  arm, #Zgemma h7S  arm , #Octagon SF4008         
            if getBoxHostName() == 'et1x000' or getBoxHostName() == 'ustym4kpro' or getTunerModel() ==  'ustym4kpro' or getCPUSoC() == 'bcm7251' or getBoxHostName() == 'sf4008' or getCPUSoC() == 'bcm7251s' or getBoxHostName() == 'h7' or getCPUSoC() == 'bcm7252s' or getBoxHostName() == 'gbquad4k' or getBoxHostName == 'osmio4k' or getBoxHostName() == 'zgemmah9s' or getBoxHostName() == 'ax60' or getBoxHostName() == 'sf8008' or getCPUSoC() == 'bcm7251'  or getCPUSoC() == 'BCM97252SSFF' or getBoxHostName() == 'dm900':
                        os.system('cp -f /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarm /sbin/neoinitarm; chmod 0755 /sbin/neoinitarm; ln -sfn /sbin/neoinitarm /sbin/init; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/arm_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')                         
                                                 

            #VUPLUS ARM 
            elif getCPUtype() == 'ARMv7' and getBoxHostName() !=  'ustym4kpro':
                if getCPUSoC() == '7278' or getBoxHostName() == 'vuduo4k':
                        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/' )
#                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarm /sbin/neoinitarm; cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarmvu /sbin/neoinitarmvu; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/duo4k_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')  
                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarm /sbin/neoinitarm; cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarmvuDuo4k /sbin/neoinitarmvu; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/duo4k_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')  
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu')                  
                        os.system('dd if=/dev/mmcblk0p6 of=%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()))
                        os.system('mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vuDuo4Kmmcblk0p6.sh /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh; cd')                         

                elif getCPUSoC() == '72604' or getBoxHostName() == 'vuzero4k':
                        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/' )
                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarm /sbin/neoinitarm; cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarmvu /sbin/neoinitarmvu; cd')  
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu')                  
                        os.system('dd if=/dev/mmcblk0p4 of=%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()))      
                        os.system('mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vuUno4Kmmcblk0p6.sh /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/zero4k_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')                         
                                                                                                                                                                                                                                                                                                                                                                                            
                #Zgemma h7S  arm  
                elif getCPUSoC() == 'bcm7251s' or getBoxHostName() == 'h7':
                        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/' )
                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarm /sbin/neoinitarm; cd') 
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarm')                 
                        os.system('python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/findkerneldevice.py; dd if=/dev/kernel of=%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()) )
                        os.system('mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_kernel.sh /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh;mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')                         
                        
                elif getCPUSoC() or getBoxHostName() == ['7444s', 
                 '7252s',
                 '7376',
                 'vuultimo4k',
                 'vuuno4k',
                 'vusolo4k',
                 'vuuno4kse'] : 
                        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/' )
                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarm /sbin/neoinitarm; cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitarmvu /sbin/neoinitarmvu; cd')  
                        os.system('chmod 755 /sbin/neoinitarm; chmod 755 /sbin/neoinitarmvu')                  
                        os.system('dd if=/dev/mmcblk0p1 of=%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()) )
                        os.system('mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mmcblk0p1.sh /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh;mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu4k_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')                         
                        
            # MIPS                                                                                                                                                                                                                 
            elif getCPUtype() == 'MIPS':
                if getCPUSoC() or getBoxHostName() or getTunerModel() == ['7335', 
                 '7413',
                 '7325',
                 '7356',
                 'bcm7356',
                 '7429',
                 '7424', 
                 '7241',
                 '7405',
                 '7405(with 3D)',
                 '7362',
                 'bcm7362',
                 'BCM7362', 
                 'bcm7358', 
                 'bcm7424', 
                 'bm750',
                 'vuduo',
                 'vusolo',
                 'vuuno',
                 'vuultimo',
                 'vusolo2',
                 'vuduo2',
                 'vusolose',
                 'vuzero',
                 'mbmini',
                 'mbultra', 
                 'osmini',
                 'h3',
                 'ini-1000sv',
                 'ini-8000sv']:                    
                        #vuplus stb mtd1
                        if getBoxHostName() == 'bm750' or getBoxHostName() == 'vuduo' or getBoxHostName() == 'vusolo' or getBoxHostName() == 'vuuno' or getBoxHostName() == 'vuultimo':
                            if fileExists ('/usr/sbin/nanddump'):
                                os.system('cd ' + getNeoLocation() + 'ImagesUpload/.kernel/; /usr/sbin/nanddump /dev/mtd1  > vmlinux.gz; mv ./vmlinux.gz ./' + getBoxHostName() + '.vmlinux.gz' )
                            elif not fileExists ('/usr/sbin/nanddump'):
                                os.system('cd ' + getNeoLocation() + 'ImagesUpload/.kernel/; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nanddump_mips /dev/mtd1  > vmlinux.gz; mv ./vmlinux.gz ./' + getBoxHostName() + '.vmlinux.gz' )
                            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; rm ./bin/neobm; rm ./bin/fontforneoboot.ttf; rm ./bin/libpngneo; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd1.sh /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh;mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mtd1_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')                         


                        #vuplus stb mtd2  
                        elif getBoxHostName() == 'vusolo2' or getBoxHostName() == 'vuduo2' or getBoxHostName() == 'vusolose' or getBoxHostName() == 'vuzero':
                            if fileExists ('/usr/sbin/nanddump'):
                                os.system('cd ' + getNeoLocation() + 'ImagesUpload/.kernel/; /usr/sbin/nanddump /dev/mtd2  > vmlinux.gz; mv ./vmlinux.gz ./' + getBoxHostName() + '.vmlinux.gz' )
                            elif not fileExists ('/usr/sbin/nanddump'):
                                os.system('cd ' + getNeoLocation() + 'ImagesUpload/.kernel/; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nanddump_mips /dev/mtd2  > vmlinux.gz; mv ./vmlinux.gz ./' + getBoxHostName() + '.vmlinux.gz' )
                            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; rm ./bin/neobm; rm ./bin/fontforneoboot.ttf; rm ./bin/libpngneo; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd2.sh /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh;mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mtd2_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')                         

                        # mbultra
                        elif  getCPUSoC() == 'bcm7424' or getBoxHostName == 'mbultra' or getTunerModel() == 'ini-8000sv':
                            os.system('cd; cd /media/neoboot/ImagesUpload/.kernel; /usr/sbin/nanddump /dev/mtd2 -o > vmlinux.gz; mv /home/root/vmlinux.gz /media/neoboot/ImagesUpload/.kernel/')
                            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; rm ./bin/neobm; rm ./bin/fontforneoboot.ttf; rm ./bin/libpngneo; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_dev_mtd2.sh /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/vu_mtd2_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')                         

                        #inne stb                                                                                                                                                                                                                                
                        elif getCPUSoC() == 'bcm7358' or getCPUSoC() == 'bcm7362' or getCPUSoC() == 'BCM7362' or getCPUSoC() == 'bcm7356' or getCPUSoC() == 'bcm7241' or getCPUSoC() == 'bcm7362' or getBoxHostName() == 'mbmini' or getBoxHostName() == 'osmini' or getTunerModel() == 'ini-1000sv' or getTunerModel() == 'h3':
                            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; mv ./bin/fontforneoboot.ttf /usr/share/fonts; mv ./bin/libpngneo /usr/lib; cp -f ./bin/neoinitmips /sbin/neoinitmips; cp -f ./bin/neoinitmipsvu /sbin/neoinitmipsvu; chmod 0755 /sbin/neoinit*; chmod 0755 ./bin/neobm; chmod 0755 /usr/lib/libpngneo; cd; chmod 0755 /sbin/neoinitmips; ln -sf /media/neoboot/ImageBoot/.neonextboot /etc/neoimage; mv /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/mips_run.py /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/run.py; cd')                         
                                                           
 
                        os.system('cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitmips /sbin/neoinitmips; cp -Rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitmipsvu /sbin/neoinitmipsvu') 
                        os.system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nfidump; chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nanddump_mips; rm -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/neoinitar*; cd')
                        os.system('chmod 755 /sbin/neoinitmips; chmod 0755 /sbin/neoinitmipsvu; cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/;mv ./bin/fontforneoboot.ttf /usr/share/fonts;mv ./bin/libpngneo /usr/lib; cp -f ./bin/neoinitmips /sbin/neoinitmips; chmod 0755 ./bin/neobm;chmod 0755 /usr/lib/libpngneo; cd; chmod 0755 /sbin/neoinitmips ')
                                                                                                                                                                                                                                                                                                            
            if fileExists('/home/root/vmlinux.gz'):
                            os.system('mv -f /home/root/vmlinux.gz %sImagesUpload/.kernel/%s.vmlinux.gz' % (getNeoLocation(), getBoxHostName()) )
                   
            if getCPUtype() == 'ARMv7':                                                                                                                                     
                        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; mv ./bin/fbcleararm ./bin/fbclear; rm -f ./bin/fbclearmips; mv ./ubi_reader_arm ./ubi_reader; rm -r ./ubi_reader_mips; rm ./bin/neoinitmips; rm ./bin/neoinitmipsvu; rm -r ./bin/nanddump_mips; rm ./bin/nfidump; rm ./bin/neobm; rm ./bin/fontforneoboot.ttf; rm ./bin/libpngneo; cd')   
            elif getCPUtype() == 'MIPS':       
                        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; mv ./bin/fbclearmips ./bin/fbclear; rm -f ./bin/fbcleararm; mv ./ubi_reader_mips ./ubi_reader; rm -r ./ubi_reader_arm; rm -f /bin/neoinitarm; rm -f /bin/neoinitarmvu; rm -r ./bin/nanddump_arm')
                                                          
            os.system(' ln -sfn ' + getNeoLocation() + 'ImageBoot/.neonextboot /etc/neoimage; chmod 644 ' + getNeoLocation() + 'ImagesUpload/.kernel/*; ln -sfn ' + getNeoLocation() + 'ImageBoot /etc/imageboot; rm -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target; chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/kernel.sh ')

            os.system('chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo_location; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo_location; sleep 2; chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom')                                    
                                              
            if os.path.isfile('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'): 	
                if getLabelDisck() != 'LABEL=':	
                    cmd = "echo -e '\n\n%s '" % _('NeoBoot has been installed succesfully !') 							                                      
                    cmd1 = "echo -e '\n\n%s '" % _('NeoBoot wykrył że dyski nie mają nadanej nazwy Label.\n') 
                elif getLabelDisck() == 'LABEL=':	
                    cmd = "echo -e '\n\n%s '" % _('NeoBoot has been installed succesfully !') 							                                      
                    cmd1 = "echo -e '\n\n%s '" % _('NeoBoot wykrył że dyski mają nadane nazwy Label.\n')                      
            else:       
                self.myclose2(_('NeoBoot has not been installed ! :(' ))
                

            self.session.open(Console, _('NeoBoot Install....'), [cmd, cmd1])
            self.close()                 
                                 	
            if fileExists('/media/usb/ImageBoot/') and fileExists('/media/hdd/ImageBoot/'): 
                    self.messagebox = self.session.open(MessageBox, _('[NeoBoot] \nError, you have neoboot installed on usb and hdd, \nUninstall one directories from one drive !!!\n'), MessageBox.TYPE_INFO, 8)
                    self.close()
            else:                                                      
                    self.close()


    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

class NeoBootImageChoose(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:

        skin = """
        <screen name="NeoBootImageChoose" position="center,center" size="1920,1080" title=" " flags="wfNoBorder" backgroundColor="transparent">  
        <widget name="progreso" position="590,600" size="530,15" borderWidth="1" zPosition="3" />
        <ePixmap position="-75,0" zPosition="-7" size="1996,1078" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/skin.png" />
        <ePixmap position="54,981" zPosition="-7" size="1809,55" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek.png" />  
        <ePixmap position="71,903" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />  
        <ePixmap position="71,820" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />    
        <ePixmap position="71,736" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />  
        <ePixmap position="70,655" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />             
        <ePixmap position="64,417" zPosition="-7" size="509,54" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/pasek2.png" />  
        <ePixmap position="1170,186" size="45,64" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/updown.png" alphatest="on" />  
        <ePixmap position="587,631" zPosition="-2" size="545,340" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrix.png" />  

        <eLabel position="70,149" size="1080,2" backgroundColor="blue" foregroundColor="blue" name="linia" />  
        <eLabel position="70,392" size="1080,2" backgroundColor="blue" foregroundColor="blue" name="linia2" />   

        <widget name="device_icon" position="123,490" size="146,136" alphatest="on" zPosition="2" />   
        <widget name="key_red" position="149,982" zPosition="1" size="280,48" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />                  
        <widget name="key_green" position="571,984" zPosition="1" size="276,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
        <widget name="key_yellow" position="1010,984" zPosition="1" size="275,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />          
        <widget name="key_blue" position="1470,983" zPosition="1" size="276,46" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />    
        <widget name="config" position="1183,256" size="659,690" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" font="Regular;32" itemHeight="42" scrollbarMode="showOnDemand" backgroundColor="black" transparent="1" />     
        <widget name="key_menu" position="254,419" zPosition="1" size="249,45" font="Regular;33" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#99FFFF" />  

        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="red" position="67,54" size="443,55" text=" NeoBoot  Multi-image " transparent="1" />          
        <eLabel backgroundColor="black" font="Regular; 30" foregroundColor="yellow" position="140,424" size="155,41" text="MENU &gt;" transparent="1" />  
        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="#C0C0C0" position="90,659" size="80,46" text="1 &gt;" transparent="1" />  
        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="#C0C0C0" position="90,742" size="80,43" text="2 &gt;" transparent="1" />  
        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="#C0C0C0" position="90,826" size="80,42" text="3 &gt;" transparent="1" />          
        <eLabel backgroundColor="black" font="Regular; 35" foregroundColor="#C0C0C0" position="90,909" size="80,39" text="4 &gt;" transparent="1" />  

        <widget name="key_1" position="150,660" zPosition="1" size="363,46" font="Regular;32" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />          
        <widget name="key_2" position="149,742" zPosition="1" size="431,42" font="Regular;32" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
        <widget name="key_3" position="149,826" zPosition="1" size="367,43" font="Regular;32" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />  

        <widget name="label1" position="1179,147" size="661,99" zPosition="1" halign="center" font="Regular;35" foregroundColor="red" backgroundColor="black" transparent="1" />                  
        <widget name="label2" position="69,164" zPosition="1" size="652,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />  
        <widget name="label3" position="315,460" zPosition="1" size="799,124" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />
        <widget name="label4" position="68,244" zPosition="1" size="606,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />  
        <widget name="label5" position="802,163" zPosition="1" size="340,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="blue" />         
        <widget name="label6" position="628,235" zPosition="1" size="516,82" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="yellow" />          
        <widget name="label7" position="836,323" zPosition="1" size="308,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
        <widget name="label8" position="67,324" zPosition="1" size="666,66" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
        <widget name="label9" position="883,49" zPosition="1" size="970,56" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" /> 
        <widget name="label10" position="985,410" zPosition="1" size="125,55" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" />       
        <widget name="label13" position="610,410" zPosition="1" size="415,55" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />  
        <widget name="label14" position="534,51" zPosition="1" size="350,56" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" /> 
        <widget name="label15" position="322,584" zPosition="1" size="265,42" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="green" />
        <widget name="label19" position="69,878" zPosition="1" size="513,99" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00FF00" />         
        </screen>"""
    else:
	    skin = """<screen name="NeoBootImageChoose" position="center,center" size="1280, 720" backgroundColor="transpBlack">
	    \n\t\t\t\t\t\t\t <ePixmap position="0,0" zPosition="-1" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1frame_base-fs8.png"  />
	    \n\t\t\t\t\t\t\t <widget source="session.VideoPicture" render="Pig" position=" 836,89" size="370,208" zPosition="3" backgroundColor="#ff000000"/>
	    \n\t\t\t\t\t\t\t        <ePixmap position="870,304" zPosition="-1" size="300,14"  pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1chan_p1_bar.png" alphatest="on" />
	    \n\t\t\t\t\t\t\t     <widget source="Title" render="Label"  position="0,5" size="800,30" font="Regular;28" halign="left" foregroundColor="#58bcff" backgroundColor="transpBlack" transparent="1"/>
	    \n\t\t\t\t\t\t\t  <widget name="label9" position="100,45" zPosition="10" size="800,30" font="Regular;24"  foregroundColor="#58bcff" backgroundColor="black" halign="left"  transparent="1" />
	    <widget name="config"  enableWrapAround="1" position="30,150" size="270,370" itemHeight="25" font="Regular;18" zPosition="2"  selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1channel_sel.png" foregroundColor="#00cc99" scrollbarMode="showNever" transparent="1" />
	    <widget name="device_icon" position="530,80" size="146,136" alphatest="on" zPosition="2" />
	    <widget name="progreso" position="400,200" size="300,10" borderWidth="1" zPosition="3" foregroundColor="white" />
	    <widget name="label3" position="380,230" zPosition="1" size="450,60" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
	    <ePixmap position="300,310" zPosition="4" size="500,4" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/separator.png" alphatest="blend" transparent="1"  />
	    <widget name="label2" position="310,340" zPosition="1" size="400,22" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
	    <widget name="label5" position="630,340" zPosition="1" size="340,22" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
	    <widget name="label4" position="310,370" zPosition="1" size="606,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
	    <widget name="label6" position="630,370" zPosition="1" size="516,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
	    <widget name="label8" position="310,400" zPosition="1" size="466,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
	    <widget name="label7" position="660,400" zPosition="1" size="308,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58ccff" />
	    <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="310,450" size="60,25" text="1 &gt;" transparent="1" />
	    <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="310,480" size="60,25" text="2 &gt;" transparent="1" />
	    <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="310,510" size="60,25" text="3 &gt;" transparent="1" />
	    <eLabel backgroundColor="black" font="Regular; 20" foregroundColor="#58ccff" position="310,540" size="60,25" text="4 &gt;" transparent="1" /> 
	    <widget name="key_1" position="360,450" zPosition="1" size="300,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
	    <widget name="key_2" position="360,480" zPosition="1" size="350,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
	    <widget name="key_3" position="360,510" zPosition="1" size="300,25" font="Regular;20" halign="left" 
valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
<widget name="label19" position="360,540" zPosition="1" size="450,25" font="Regular;20" halign="left" valign="center" backgroundColor="black" transparent="1" foregroundColor="white" />
<ePixmap position="920,480" zPosition="1" size="228,130" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1matrix.png" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="0,650" size="250,40" alphatest="blend" />
<widget name="key_red" position="0,670" zPosition="2" size="250,40"  font="Regular; 20" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green25.png" position="200,650" size="230,36" alphatest="blend" />
<widget name="key_green" position="200,670" size="230,38" zPosition="1" font="Regular; 20"  halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow25.png" position="400,650" size="230,36" alphatest="blend" />
<widget name="key_yellow" position="400,670" size="230,38" zPosition="1" font="Regular; 20"  halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue25.png" position="600,650" size="230,36" alphatest="blend" />
<widget name="key_blue" position="600,670" size="230,38" zPosition="1" font="Regular; 20" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
<widget name="key_menu" position="950,640" zPosition="1" size="249,45" font="Regular;22" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#58bcff" />
<eLabel backgroundColor="black" font="Regular; 24" foregroundColor="white" position="900,650" size="155,41" text="MENU &gt;" transparent="1" />
<ePixmap position="20,135" zPosition="1" size="280,400" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/border_menu1.png"  />
<widget source="global.CurrentTime" render="Label" position="780,30" size="450,55" font="RegularAA;24" valign="center" halign="center" backgroundColor="transpBlack" foregroundColor="#58bcff"  zPosition="10" transparent="1">
<convert type="ClockToText">Format:%A  %e  %B  %Y </convert>
</widget>
\t\t\t</screen>""" 


    def __init__(self, session):
		
        Screen.__init__(self, session)
                       
        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh'):
            os.system('touch /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh; echo "#!/bin/sh\n#DESCRIPTION=This script by gutosie\n"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh; chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh') 
            if getNeoMount() == 'hdd_install_/dev/sda1': 
                    os.system('echo "umount /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sda1 /media/hdd"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh') 
            elif getNeoMount() == 'hdd_install_/dev/sdb1': 
                    os.system('echo "umount /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sdb1 /media/hdd"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh') 
            elif getNeoMount() == 'hdd_install_/dev/sda2': 
                    os.system('echo "umount /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sda2 /media/hdd"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh') 
            elif getNeoMount() == 'hdd_install_/dev/sdb2': 
                    os.system('echo "umount /media/hdd\nmkdir -p /media/hdd\n/bin/mount /dev/sdb2 /media/hdd"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh') 

            if getNeoMount2() == 'usb_install_/dev/sdb1': 
                    os.system('echo "umount /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdb1 /media/usb"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh')      
            elif getNeoMount2() == 'usb_install_/dev/sda1': 
                    os.system('echo "umount /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sda1 /media/usb"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sdb2': 
                    os.system('echo "umount /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdb2 /media/usb"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sdc1': 
                    os.system('echo "umount /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdc1 /media/usb"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sdd1': 
                    os.system('echo "umount /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdd1 /media/usb"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sde1': 
                    os.system('echo "umount /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sde1 /media/usb"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh')  
            elif getNeoMount2() == 'usb_install_/dev/sdf1': 
                    os.system('echo "umount /media/usb\nmkdir -p /media/usb\n/bin/mount /dev/sdf1 /media/usb"  >> /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/mountpoint.sh')  

        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh'):
            if getINSTALLNeo() == '/dev/sda1':
                    out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\n/bin/mount /dev/sda1 ' + getNeoLocation() + '  \n')
                    out.close()
            elif getINSTALLNeo() == '/dev/sdb1':
                    out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\n/bin/mount /dev/sdb1 ' + getNeoLocation() + '  \n')
                    out.close()
            elif getINSTALLNeo() == '/dev/sda2':
                    out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\n/bin/mount /dev/sda2 ' + getNeoLocation() + '  \n')
                    out.close()
            elif getINSTALLNeo() == '/dev/sdb2':
                    out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\n/bin/mount /dev/sdb2 ' + getNeoLocation() + '  \n')
                    out.close()
            elif getINSTALLNeo() == '/dev/sdc1':
                    out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\n/bin/mount /dev/sdc1 ' + getNeoLocation() + '  \n')
                    out.close()                    
            elif getINSTALLNeo() == '/dev/sdd1':
                    out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\n/bin/mount /dev/sdd1 ' + getNeoLocation() + '  \n')
                    out.close()
            elif getINSTALLNeo() == '/dev/sde1':
                    out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\n/bin/mount /dev/sde1 ' + getNeoLocation() + '  \n')
                    out.close()
            elif getINSTALLNeo() == '/dev/sdf1':
                    out = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh', 'w')
                    out.write('#!/bin/sh\n#DESCRIPTION=This script by gutosie\n\n/bin/mount /dev/sdf1 ' + getNeoLocation() + '  \n')
                    out.close()
            system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo.sh')   

        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom'):
            os.system('chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo_location; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neo_location; chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom')                                    


        if fileExists('/tmp/.init_reboot'):
            system('rm /tmp/.init_reboot')

        if fileExists('/.multinfo'):
            if not fileExists('/.control_ok'):
                if fileExists('/.control_boot_new_image'):  
                    os.system('rm -f /.control_boot_new_image; echo "Image uruchomione OK\nNie kasuj tego pliku. \n\nImage started OK\nDo not delete this file."  > /.control_ok ')          
                if not fileExists('/.control_boot_new_image'):  
                    os.system('echo "Image uruchomione OK\nNie kasuj tego pliku. \n\nImage started OK\nDo not delete this file."  > /.control_ok')
                    #os.system('touch /.control_ok ') 

        if fileExists('/.multinfo') and getCPUtype() == 'ARMv7':
            if os.path.exists('/proc/stb/info/boxtype'):
                if getBoxHostName == 'sf4008':  #getCPUSoC() == 'bcm7251'  
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p4 /media/mmc')  

        if fileExists('/.multinfo') and getCPUtype() == 'ARMv7':
            if os.path.exists('/proc/stb/info/boxtype'):
                if getBoxHostName == 'et1x000': #getCPUSoC() == 'bcm7251' or   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p4 /media/mmc')  

        if fileExists('/.multinfo') and getCPUtype() == 'ARMv7':
            if os.path.exists('/proc/stb/info/boxtype'):
                if getCPUSoC() == 'bcm7251s' or getBoxHostName() == 'h7':   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p3 /media/mmc')

            if os.path.exists('/proc/stb/info/boxtype'):
                if getBoxHostName() == 'zgemmah9s':   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p7 /media/mmc')

            if getBoxHostName == 'sf8008':   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p13 /media/mmc')  

            if getBoxHostName == 'ax60':   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p21 /media/mmc')

            if getBoxHostName() == 'ustym4kpro' or getTunerModel() ==  'ustym4kpro':   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p13 /media/mmc')

            if os.path.exists('/proc/stb/info/model'):
                if getTunerModel() == 'dm900' or getCPUSoC() == 'BCM97252SSFF':   
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p2 /media/mmc')
                    
            if  getBoxVuModel() == 'uno4kse' or getBoxVuModel() == 'uno4k'  or  getBoxVuModel() == 'ultimo4k' or  getBoxVuModel() == 'solo4k':
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p4 /media/mmc')

            if  getBoxVuModel() == 'zero4k':
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p7 /media/mmc')

            if  getBoxVuModel() == 'duo4k':               
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p9 /media/mmc')

            if getCPUSoC() == 'bcm7252s' or getBoxHostName() == 'gbquad4k':
                    os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p5 /media/mmc')

            #if getBoxHostName == 'osmio4k':
                    #os.system('mkdir -p /media/mmc; mount /dev/mmcblk0p5 /media/mmc')


        self.list = []
        self.setTitle('         NeoBoot  %s  - Menu' % PLUGINVERSION + '          ' + 'Ver. update:  %s' % UPDATEVERSION)
        self['device_icon'] = Pixmap()
        self['progreso'] = ProgressBar()
        self['linea'] = ProgressBar()
        self['config'] = MenuList(self.list)
        self['key_red'] = Label(_('Boot Image'))
        self['key_green'] = Label(_('Installation'))
        self['key_yellow'] = Label(_('Remove Image '))
        self['key_blue'] = Label(_('Info'))
        self['key_menu'] = Label(_('More options'))
        self['key_1'] = Label(_('Update NeoBot'))
        self['key_2'] = Label(_('Reinstall NeoBoot'))
        self['key_3'] = Label(_('Install Kernel'))
        self['label1'] = Label(_('Please choose an image to boot'))
        self['label2'] = Label(_('NeoBoot is running from:'))
        self['label3'] = Label('')
        self['label4'] = Label(_('NeoBoot is running image:'))
        self['label5'] = Label('')
        self['label6'] = Label('')
        self['label7'] = Label('')
        self['label8'] = Label(_('Number of images installed:'))
        self['label19'] = Label('')         
        self['label9'] = Label('')
        self['label10'] = Label('')
        self['label11'] = Label('')
        self['label12'] = Label('')
        self['label13'] = Label(_('Version update: '))
        self['label14'] = Label(_('NeoBoot version: '))
        self['label15'] = Label(_('Memory disc:'))
        self['actions'] = ActionMap(['WizardActions',
         'ColorActions',
         'MenuActions',
         'NumberActionMap',
         'SetupActions',
         'number'], {'ok': self.boot,
         'red': self.boot,
         'green': self.ImageInstall,
         'yellow': self.remove,
         'blue': self.pomoc,
         'ok': self.boot,
         'menu': self.mytools,
         '1': self.neoboot_update,
         '2': self.ReinstallNeoBoot,
         '3': self.ReinstallKernel,
         'back': self.close_exit})
        if not fileExists('/etc/name'):
            os.system('touch /etc/name')
        self.onShow.append(self.updateList)

    def chackkernel(self):
		
                            message = _('NeoBoot wykryl niezgodnos kernela w flash, \nZainstalowac kernel dla flash image ? ?')
                            ybox = self.session.openWithCallback(self.updatekernel, MessageBox, message, MessageBox.TYPE_YESNO)
                            ybox.setTitle(_('Updating ... '))
    def pomoc(self):
		
        if fileExists('/.multinfo'):
            mess = _('Information available only when running Flash.')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
        else:
            self.session.open(Opis)

    def ReinstallNeoBoot(self):
		
        INSTALLbox = self.session.openWithCallback(self.reinstallboot, MessageBox, _('Wybierz Tak, by przeinstalować neoboota.\n     NEOBOOT.'), MessageBox.TYPE_YESNO)
        INSTALLbox.setTitle(_('Zainstalować ponownie neoboota ?'))
                
    def reinstallboot(self, answer):
		        
        if answer is True:
            try:
                cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Please reinstall NeoBoot....\nPlease wait, done...\nrestart systemu...')
                cmd1 = 'cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; rm ./.location; rm ./files/mountpoint.sh; rm ./files/neom; rm ./files/neo.sh; sleep 5; killall -9 enigma2 '                                                                                       
            except:                                 
                False
            self.session.open(Console, _('NeoBoot ARM....'), [cmd, cmd1])
            self.close()
        else:
            try:
                self.session.open(MessageBox, _('Rezygnacja.'), MessageBox.TYPE_INFO, 4)
                self.close()
            except:
                False
         
    def close_exit(self):
		
        system('touch /tmp/.init_reboot')
        if not fileExists('/.multinfo'):            
            out = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'w' )
            out.write('Flash')
            out.close()
        self.close()
                        
        if fileExists('/.multinfo'):            
            with open('%sImageBoot/.neonextboot' % getNeoLocation(), 'r'  ) as f:
                imagefile = f.readline().strip()
                f.close()
                out = open('%sImageBoot/.neonextboot'% getNeoLocation(), 'w' )
                out.write(imagefile)
                out.close()

        else:
            system('touch /tmp/.init_reboot')
            out = open('%sImageBoot/.neonextboot' % getNeoLocation() , 'w')
            out.write('Flash')
            out.close()
        self.close()
                        
    def ReinstallKernel(self):
		
        from Plugins.Extensions.NeoBoot.files.tools import ReinstallKernel
        self.session.open(ReinstallKernel)

##/////NA CZAS TESTU UPDATE ZATRZYMANE\\\\\####################################
#    def neoboot_update(self):
#                self.messagebox = self.session.open(MessageBox, _('Updated unnecessary, you have the latest version. Please try again later.'), MessageBox.TYPE_INFO, 8)
#                self.close()
    
    def neoboot_update(self):
		
        if fileExists('/.multinfo'):
            mess = _('Downloading available only from the image Flash.')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
        else:
            out = open('%sImageBoot/.neonextboot' % getNeoLocation() , 'w')
            out.write('Flash')
            out.close()
	
            message = _('\n\n\n')
            message += _('WARNING !: The update brings with it the risk of errors.\n')
            message += _('Before upgrading it is recommended that you make a backup NeoBoot.\n')
            message += _('Do you want to run the update now ?\n')
            message += _('\n')
            ybox = self.session.openWithCallback(self.chackupdate2, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('The download neoboot update.'))

    def chackupdate2(self, yesno):
		
        if yesno:
            self.chackupdate3()
        else:
            self.session.open(MessageBox, _('Canceled update.'), MessageBox.TYPE_INFO, 7)
                                           
    def chackupdate3(self):
		
        os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot;curl -O --ftp-ssl https://raw.githubusercontent.com/gutosie/NeoBoot8/master/ver.txt;sleep 3;cd /')            
        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt'):
            os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot;fullwget --no-check-certificate https://raw.githubusercontent.com/gutosie/NeoBoot8/master/ver.txt; sleep 3;cd /')
            if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt'):
                self.session.open(MessageBox, _('Unfortunately, at the moment not found an update, try again later.'), MessageBox.TYPE_INFO, 8)
        else:
            mypath = ''
            version = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt', 'r')
            mypath = float(version.read().strip())
            version.close()
            if float(UPDATEVERSION) != mypath:
                message = _('NeoBoot has detected update.\nDo you want to update NeoBoota now ?')
                ybox = self.session.openWithCallback(self.aktualizacjamboot, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Updating ... '))
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt'):
                os.system('rm /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt')
                self.session.open(MessageBox, _('Updated unnecessary, you have the latest version. Please try again later.'), MessageBox.TYPE_INFO)

    def aktualizacjamboot(self, yesno):
		
        if yesno:
            if fileExists('/tmp/*.zip'):
                os.system('rm /tmp/*.zip')
            os.system('cd /tmp; curl -O --ftp-ssl https://codeload.github.com/gutosie/NeoBoot8/zip/master; mv /tmp/master /tmp/neoboot.zip; cd /')
            if not fileExists('/tmp/neoboot.zip'):
                    os.system('cd /tmp;fullwget --no-check-certificate https://codeload.github.com/gutosie/NeoBoot8/zip/master; mv /tmp/master /tmp/neoboot.zip; sleep 3;cd ')
                    if not fileExists('/tmp/neoboot.zip'):
                        self.session.open(MessageBox, _('Unfortunately, at the moment not found an update, try again later.'), MessageBox.TYPE_INFO, 8)
            else:                                                                                                                                                                                                                                                                                                                                                   
                os.system('cd /tmp/; unzip -qn ./neoboot.zip; rm -f ./neoboot.zip; cp -rf ./NeoBoot8-master/NeoBoot /usr/lib/enigma2/python/Plugins/Extensions; rm -rf /tmp/NeoBoot8-master;  rm /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt; cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; chmod 0755 ./bin/neoini*;  chmod 0755 ./ex_init.py; chmod 0755 ./target/*; chmod 0755 ./files/NeoBoot.sh; chmod 0755 ./files/S50fat.sh; cd')                    
                if getCPUtype() == 'MIPS':
                    os.system('cd /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/; cp -rf ./bin/neoinitmipsvu /sbin; chmod 755 /sbin/neoinitmipsvu; cp -rf ./bin/neoinitmips /sbin; chmod 755 /sbin/neoinitmips; cd')                    
                #elif getCPUtype() == 'ARMv7':
                    #os.system('')                                                                

                restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('Completed update NeoBoot. You need to restart the E2 !!!\nRestart now ?'), MessageBox.TYPE_YESNO)
                restartbox.setTitle(_('Restart GUI now ?'))

        else:
            os.system('rm -f /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ver.txt')
            self.session.open(MessageBox, _('The update has been canceled.'), MessageBox.TYPE_INFO, 8)

    def restartGUI(self, answer):		
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def installMedia(self):				
        images = False
        myimages = os.listdir('%sImagesUpload' % getNeoLocation() )
        print myimages
        for fil in myimages:
            if fil.endswith('.zip'):
                images = True
                break
            if fil.endswith('.tar.xz'):
                images = True
                break
            if fil.endswith('.nfi'):
                images = True
                break                
            else:
                images = False
                
        if images == True:
            self.ImageInstall()
        else:
            mess = _('[NeoBoot] The %sImagesUpload directory is EMPTY !!!\nPlease upload the image files in .ZIP or .NFI formats to install. ' % getNeoLocation() )
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)

    def MBBackup(self):
		
        from Plugins.Extensions.NeoBoot.files.tools import MBBackup
        self.session.open(MBBackup)

    def MBRestore(self):
		
        from Plugins.Extensions.NeoBoot.files.tools import MBRestore
        self.session.open(MBRestore)

    def updateList(self):        
        if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'):                    
                self.session.open(NeoBootInstallation)
        else:
            self.updateListOK()

    def updateListOK(self):
		
        self.list = []
        pluginpath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        f = open(pluginpath + '/.location', 'r')
        mypath = f.readline().strip()
        f.close()
        icon = 'dev_usb.png'
        if 'card' in mypath or 'sd' in mypath:
            icon = 'dev_sd.png'
        elif 'ntfs' in mypath:
            icon = 'dev_sd.png'
        elif 'hdd' in mypath:
            icon = 'dev_hdd.png'
        elif 'cf' in mypath:
            icon = 'dev_cf.png'
        icon = pluginpath + '/images/' + icon
        png = LoadPixmap(icon)
        self['device_icon'].instance.setPixmap(png)                               
        linesdevice = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'r').readlines()
        deviceneo = linesdevice[0][0:-1]
        device = deviceneo
        ustot = usfree = usperc = ''
        rc = system('df > /tmp/memoryinfo.tmp')
        if fileExists('/tmp/memoryinfo.tmp'):
            f = open('/tmp/memoryinfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == device:               
                    if totsp == 5:
                        ustot = parts[1]
                        usfree = parts[3]
                        usperc = parts[4]
                    else:
                        ustot = 'N/A   '
                        usfree = parts[2]
                        usperc = parts[3]
                    break

            f.close()
            os.remove('/tmp/memoryinfo.tmp')

        perc = int(usperc[0:-1])
        self['progreso'].setValue(perc)
        green = '#00389416'
        red = '#00ff2525'
        yellow = '#00ffe875'
        orange = '#00ff7f50'
        if perc < 30:
                color = green
        elif perc < 60:
                color = yellow
        elif perc < 80:
                color = orange
        else:
                color = red
        try:
            from skin import parseColor
            self['label13'].instance.setForegroundColor(parseColor(color))
            self['label14'].instance.setForegroundColor(parseColor(color))
            self['label15'].instance.setForegroundColor(parseColor(color))
            self['progreso'].instance.setForegroundColor(parseColor(color))
        except:
            pass

        self.availablespace = usfree[0:-3]
        strview = _('Used: ') + usperc + _('   \n   Available: ') + usfree[0:-3] + ' MB'
        self['label3'].setText(strview)
        try:
            f2 = open('%sImageBoot/.neonextboot', 'r' % getNeoLocation())
            mypath2 = f2.readline().strip()
            f2.close()
        except:
            mypath2 = 'Flash'

        if mypath2 == 'Flash':
            image = getImageNeoBoot()
            if not fileExists('/.multinfo'):
                if fileExists('/etc/issue.net'):
                    try:
                        obraz = open('/etc/issue.net', 'r').readlines()
                        imagetype = obraz[0][:-3]
                        image = imagetype
                        open('%sImageBoot/.Flash', 'w' % getNeoLocation()).write(image)
                    except:
                        False
            if fileExists('/.multinfo'):
                if fileExists('/media/mmc/etc/issue.net'):
                    try:
                        obraz = open('/media/mmc/etc/issue.net', 'r').readlines()
                        imagetype = obraz[0][:-3]
                        image = imagetype
                        open('%sImageBoot/.Flash', 'w' % getNeoLocation()).write(image)
                    except:
                        False
                elif fileExists('/etc/issue.net'):
                    try:
                        obraz = open('/etc/issue.net', 'r').readlines()
                        imagetype = obraz[0][:-1]
                        lines = open('/etc/hostname', 'r').readlines()
                        boxtype = lines[0][:-1]
                        image = imagetype[0:-2] + ' ' + boxtype
                        open('%sImageBoot/.Flash', 'w' % getNeoLocation()).write(image)
                    except:
                        False

        elif fileExists('%sImageBoot/.Flash' % getNeoLocation()):
            f = open('%sImageBoot/.Flash', 'r' % getNeoLocation())
            image = f.readline().strip()
            f.close()
        image = ' [' + image + ']'
        self.list.append('Flash' + image)
        self['label5'].setText(mypath)
        if fileExists('/.multinfo'):
            f2 = open('/.multinfo', 'r')
            mypath3 = f2.readline().strip()
            f2.close()
            self['label6'].setText(mypath3)
        else:
            f2 = open('%sImageBoot/.neonextboot' % getNeoLocation() , 'r' )
            mypath3 = f2.readline().strip()
            f2.close()
            self['label6'].setText(mypath3)
        mypath = ('%sImageBoot' % getNeoLocation())
        myimages = listdir(mypath)
        for fil in myimages:
            if os.path.isdir(os.path.join(mypath, fil)):
                self.list.append(fil)

        self['label7'].setText(str(len(self.list) - 1))
        self['config'].setList(self.list)
        KERNELVERSION = getKernelImageVersion()      
        strview = PLUGINVERSION + '             ' + 'Kernel %s' % KERNELVERSION
        self['label9'].setText(strview)
        self['label19'].setText(readline('%sImagesUpload/.kernel/used_flash_kernel' % getNeoLocation() ))
        strview = UPDATEVERSION
        self['label10'].setText(strview)

    def mytools(self):		
        from Plugins.Extensions.NeoBoot.files.tools import MBTools
        self.session.open(MBTools)

    def remove(self):
		
        self.mysel = self['config'].getCurrent()
        if 'Flash' in self.mysel:
            self.mysel = 'Flash'
        if self.mysel:
            f = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'r')
            mypath = f.readline().strip()
            f.close()
            try:
                if fileExists('/.multinfo'):
                     self.session.open(MessageBox, _('Sorry you can delete only from the image Flash.'), MessageBox.TYPE_INFO, 5)
                elif self.mysel == 'Flash':
                    self.session.open(MessageBox, _('Sorry you cannot delete Flash image'), MessageBox.TYPE_INFO, 5)
                elif mypath == self.mysel:
                    self.session.open(MessageBox, _('Sorry you cannot delete the image currently booted from.'), MessageBox.TYPE_INFO, 5)
                else:
                    out = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'w' )
                    out.write('Flash')
                    out.close()
                    message = _('Delete the selected image - ') + self.mysel + _('\nDelete ?')
                    ybox = self.session.openWithCallback(self.remove2, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Delete Confirmation'))
            except:
                print 'no image to remove'

        else:
            self.mysel

    def up(self):		
        self.list = []
        self['config'].setList(self.list)
        self.updateList()

    def up2(self):		
        try:
            self.list = []
            self['config'].setList(self.list)
            self.updateList()
        except:
            print ' '

    def remove2(self, yesno):		
        if yesno:
            cmd = _("echo -e 'Deleting in progress...\n'")
            cmd1 = 'rm -r %sImageBoot/' % getNeoLocation() + self.mysel
            self.session.openWithCallback(self.up, Console, _('NeoBoot: Deleting Image'), [cmd, cmd1])
        else:
            self.session.open(MessageBox, _('Removing canceled!'), MessageBox.TYPE_INFO)

    def ImageInstall(self):		
        if fileExists('/.multinfo'):
                    message = _('Instalacja nowego oprogramowania do neoboot, zalecane tylko z poziomu Flash!!!\n---Kontynuowac ?---')
                    ybox = self.session.openWithCallback(self.installation_image, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Installation with risk '))
        else:
                    message = _('Instalacja z poziomu Flash!!!\n---Kontynuowac ?---')
                    ybox = self.session.openWithCallback(self.installation_image, MessageBox, message, MessageBox.TYPE_YESNO)
                    ybox.setTitle(_('Installation new image. '))
#            self.installation_image()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             

    def installation_image(self, yesno):		
        if yesno:
            if getCPUSoC() or getBoxHostName() or getTunerModel() == ['zgemmah9s',
             'osmio4k',
             'bcm7252s',
             'gbquad4k', 
             'ax60',
             'sf8008',
             'bcm7251', 
             'sf4008', 
             'et1x000',
             'bcm7251s', 
             '7241', 
             'h7',
             'dm900',
             'BCM97252SSFF', 
             '7444s',
             '7252s',
             '7376',
             '72604',
             '7278',
             '7335',
             '7413',
             '7325',
             '7356',
             'bcm7356', 
             '7429',
             '7424',
             '7362', 
             'bcm7362',
             'BCM7362',
             'bcm7358', 
             '7405', 
             '7405(with 3D)',
             'bcm7424',
             'vuultimo', 
             'mbmini',
             'osmini',
             'mbultra',
             'ustym4kpro'             
             'h3']:                   
                self.extractImage()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
            else:
                self.messagebox = self.session.open(MessageBox, _('Tuner nie jest wspierany przez NeoBoota.\nSkontaktuj sie z autorem.\nNie wykryto odpowiedniego STB do instalacji !!!!'), MessageBox.TYPE_INFO, 8)
                self.close()
        else:
                self.messagebox = self.session.open(MessageBox, _('Zaleca sie instalacje nowego oprogramowania tylko z poziomu systemu flash.\n---NEOBOOT EXIT---'), MessageBox.TYPE_INFO, 10)
                self.close()
            
    def extractImage(self):		
        images = False
        if fileExists('%sImageBoot/.without_copying' % getNeoLocation() ):
            system('rm %sImageBoot/.without_copying' % getNeoLocation() )
            
        if not os.path.exists('%sImagesUpload' % getNeoLocation()):
            system('mkdir %sImagesUpload' % getNeoLocation())                                                                      
        myimages = listdir('%sImagesUpload' % getNeoLocation())
        print myimages
        for fil in myimages:
            if fil.endswith('.zip'):
                images = True
                break
            if fil.endswith('.tar.xz'):
                images = True
                break
            if fil.endswith('.nfi'):
                images = True
                break                
            else:
                images = False

        if images == True:
                from Plugins.Extensions.NeoBoot.unpack import InstallImage
                self.session.open(InstallImage)
        else:
            self.ImageSystem()

    def ImageSystem(self):		
        if fileExists('%sImageBoot/.neonextboot' % getNeoLocation()):
                self.messagebox = self.session.open(MessageBox, _('[NeoBoot] The %sImagesUpload directory is EMPTY !!!\nPlease upload the image files in .ZIP or .NFI formats to install.\n' % getNeoLocation() ), MessageBox.TYPE_INFO, 8)
                self.close()   
        else:
            self.close()

    def boot(self):		
        self.mysel = self['config'].getCurrent()
        if 'Flash' in self.mysel:
            self.mysel = 'Flash'
        if self.mysel:
            out = open('' + getNeoLocation() + 'ImageBoot/.neonextboot', 'w' )
            out.write(self.mysel)
            out.close()

            from Plugins.Extensions.NeoBoot.run import StartImage
            self.session.open(StartImage)

    def myClose(self, message):		
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()
                
                                                               
def readline(filename, iferror = ''):
    if iferror[:3] == 'or:':
      data = iferror[3:]
    else:
      data = iferror
    try:
        if os.path.exists(filename):
            with open(filename) as f:
                data = f.readline().strip()
                f.close()
    except Exception:
        PrintException()
    return data

def checkimage():
    mycheck = False
    if fileExists('/proc/stb/info'): #vumodel'): ogranicza tylko dla vu+
        mycheck = True
    else:
        mycheck = False
    return mycheck


def main(session, **kwargs):
	
    if not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom'):
        pass
    else:
        if not fileExists('%sImageBoot/.version' % getNeoLocation()):
            os.system('mkdir -p %s; sync; chmod 0755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom' % getNeoLocation())

    version = 0           
    if fileExists('%sImageBoot/.version' % getNeoLocation()):
        f = open('%sImageBoot/.version' % getNeoLocation())
        version = float(f.read())
        f.close()
    if fileExists('%sImageBoot/.neonextboot' % getNeoLocation()):
        f2 = open('%sImageBoot/.neonextboot' % getNeoLocation(), 'r' )
        mypath2 = f2.readline().strip()
        f2.close()
        if mypath2 != 'Flash' or mypath2 == 'Flash' and checkimage():
            if float(PLUGINVERSION) != version:
                session.open(MyUpgrade)
            else:
                session.open(NeoBootImageChoose)
        else:
            session.open(MessageBox, _('Sorry: Wrong image in flash found. You have to install in flash Vu+ or Octagon-sf4008 Image !!!'), MessageBox.TYPE_INFO, 10)
    else:  
        session.open(NeoBootInstallation)

def menu(menuid, **kwargs):
    if menuid == 'mainmenu':
        return [(_('NeoBOOT'),
          main,
          'neo_boot',
          1)]
    return []

from Plugins.Plugin import PluginDescriptor

def Plugins(**kwargs):
    return [PluginDescriptor(name='NeoBootUstym ', description='NeoBoot', where=PluginDescriptor.WHERE_MENU, fnc=menu), PluginDescriptor(name='NeoBoot', description=_('Installing multiple images'), icon='neo.png', where=PluginDescriptor.WHERE_PLUGINMENU, fnc=main)]

####################### _(-_-)_ gutosie _(-_-)_ #######################
