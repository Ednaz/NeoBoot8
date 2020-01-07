#!/usr/bin/python
# -*- coding: utf-8 -*-
from __init__ import _
import codecs
from enigma import getDesktop
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.ScrollLabel import ScrollLabel
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.ConfigList import ConfigListScreen
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.config import getConfigListEntry, config, ConfigYesNo, ConfigText, ConfigSelection, NoSave
from Plugins.Extensions.NeoBoot.plugin import Plugins
from Plugins.Plugin import PluginDescriptor
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.Console import Console
from Screens.Screen import Screen
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, fileExists, pathExists, createDir
from os import system, listdir, mkdir, chdir, getcwd, rename as os_rename, remove as os_remove, popen
from os.path import dirname, isdir, isdir as os_isdir
from enigma import eTimer
from Plugins.Extensions.NeoBoot.files.stbbranding import getNeoLocation, getImageNeoBoot, getKernelVersionString
import os
import time
import sys
import struct, shutil

PLUGINVERSION = '5.00'

neoboot = getNeoLocation()
 
def getKernelVersion():
    try:
        return open('/proc/version', 'r').read().split(' ', 4)[2].split('-', 2)[0]
    except:
        return _('unknown')
            
def getCPUtype():
    cpu='UNKNOWN'
    if os.path.exists('/proc/cpuinfo'):
        with open('/proc/cpuinfo', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('ARMv7') != -1:
            cpu='ARMv7'
        elif lines.find('mips') != -1:
            cpu='MIPS'
    return cpu

if os.path.exists('/etc/hostname'):
    with open('/etc/hostname', 'r') as f:
        myboxname = f.readline().strip()
        f.close()            
           
if os.path.exists('/proc/stb/info/vumodel'):
    with open('/proc/stb/info/vumodel', 'r') as f:
        vumodel = f.readline().strip()
        f.close() 

if os.path.exists('/proc/stb/info/boxtype'):
    with open('/proc/stb/info/boxtype', 'r') as f:
        boxtype = f.readline().strip()
        f.close() 

class BoundFunction:
    __module__ = __name__

    def __init__(self, fnc, *args):
        self.fnc = fnc
        self.args = args

    def __call__(self):
        self.fnc(*self.args)


class MBTools(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '\n <screen name="NeoBoot" position="center,center" size="1159,750" title="Narzedzia NeoBoota">\n\t\t<widget source="list" render="Listbox" position="15,27" size="1131,720" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                    \t\t\tMultiContentEntryText(pos = (50, 1), size = (820, 46), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (66, 66), png = 1),\n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 35)],\n                    \t\t\t"itemHeight": 50\n                \t\t}\n            \t\t</convert>\n\t\t</widget>\n        </screen>'
    else:
        skin = '\n <screen position="center,center" size="590,330" title="Narzedzia NeoBoota">\n\t\t<widget source="list" render="Listbox" position="10,16" size="570,300" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                    \t\t\tMultiContentEntryText(pos = (50, 1), size = (520, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),\n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 22)],\n                    \t\t\t"itemHeight": 36\n                \t\t}\n            \t\t</convert>\n\t\t</widget>\n        </screen>'
    __module__ = __name__

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.updateList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def updateList(self):                       
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)

        res = (_('Wykonaj kopi\xc4\x99 obrazu z NeoBoota'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

        res = (_('Przywr\xc3\xb3\xc4\x87 kopi\xc4\x99 obrazu do NeoBoota'), png, 1)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Menad\xc5\xbcer urz\xc4\x85dze\xc5\x84'), png, 2)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Usu\xc5\x84 image ZIP z katalogu ImagesUpload  '), png, 3)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Odinstalowanie  NeoBoota'), png, 4)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Reinstalacja  NeoBoota'), png, 5)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Zaktualizuj NeoBoota na wszystkich obrazach.'), png, 6)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Kopia Zapasowa NeoBoota'), png, 7)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Aktualizacja listy TV na zainstalowanych image.'), png, 8)
        self.list.append(res)
        self['list'].list = self.list

        res = (_('Aktualizacja IPTVPlayer na zainstalowanych image.'), png, 9)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Usuniecie hasla do root.'), png, 10)
        self.list.append(res)
        self['list'].list = self.list        

        res = (_('Sprawdz poprawnosc instalacji neoboota'), png, 11)
        self.list.append(res)
        self['list'].list = self.list
        
        res = (_('Informacje NeoBoota'), png, 12)
        self.list.append(res)
        self['list'].list = self.list        

        res = (_('Wspierane tunery sat'), png, 13)
        self.list.append(res)
        self['list'].list = self.list  

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0 and self.session.open(MBBackup):
            pass
        if self.sel == 1 and self.session.open(MBRestore):
            pass
        if self.sel == 2 and self.session.open(MenagerDevices):
            pass
        if self.sel == 3 and self.session.open(MBDeleUpload):
            pass
        if self.sel == 4 and self.session.open(UnistallMultiboot):
            pass
        if self.sel == 5 and self.session.open(ReinstllNeoBoot):
            pass
        if self.sel == 6 and self.session.open(UpdateNeoBoot):
            pass
        if self.sel == 7 and self.session.open(BackupMultiboot):
            pass
        if self.sel == 8 and self.session.open(ListTv):
            pass
        if self.sel == 9 and self.session.open(IPTVPlayer):
            pass
        if self.sel == 10 and self.session.open(SetPasswd): 
            pass
        if self.sel == 11 and self.session.open(CheckInstall): 
            pass                        
        if self.sel == 12 and self.session.open(MultiBootMyHelp):
            pass
        if self.sel == 13 and self.session.open(TunerInfo):
            pass


class MBBackup(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = ' <screen position="center,center" size="850,750" title="Wykonaj kopie zapasowa obrazu z NeoBoota">\n\t\t\n            <widget name="lab1" position="24, 5" size="819, 62" font="Regular;35" halign="center" valign="center" transparent="1" foregroundColor="blue" />\n\n            <widget name="lab2" position="22, 82" size="819, 61" font="Regular;35" halign="center" valign="center" transparent="1" foregroundColor="blue" />\n\n            <widget name="lab3" position="21, 150" size="819, 62" font="Regular;35" halign="center" valign="center" transparent="1" foregroundColor="blue" />\n \n            <widget source="list" render="Listbox" itemHeight="40" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" font="Regular;25" position="20, 218" zPosition="1" size="820, 376" scrollbarMode="showOnDemand" transparent="1">\n\t\t\t\n            <convert type="StringList" font="Regular;35" />\n\n            </widget>\n\n            <ePixmap position="336, 596" size="181, 29" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" />\n\n           <widget name="key_red" position="307, 629" zPosition="2" size="251, 77" font="Regular;35" halign="center" valign="center" backgroundColor="red" transparent="1" foregroundColor="red" />\n\n           </screen>'
    else:
        skin = ' <screen position="center,center" size="700,550" title="Wykonaj kopie zapasowa obrazu z NeoBoota">\n\t\t\n             <widget name="lab1" position="20,20" size="660,30" font="Regular;24" halign="center" valign="center" transparent="1"/>\n\n             <widget name="lab2" position="20,50" size="660,30" font="Regular;24" halign="center" valign="center" transparent="1"/>\n\n             <widget name="lab3" position="20,100" size="660,30" font="Regular;22" halign="center" valign="center" transparent="1"/>\n \n             <widget source="list" render="Listbox" position="40,130" zPosition="1" size="620,360" scrollbarMode="showOnDemand" transparent="1" >\n\t\t\t\n             <convert type="StringList" />\n</widget>\n<ePixmap position="280,500" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" />\n\n               <widget name="key_red" position="280,500" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />\n\n            </screen>'   

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('')
        self['lab2'] = Label('')
        self['lab3'] = Label(_('Wybierz obraz z kt\xc3\xb3rego chcesz zrobi\xc4\x87 kopie'))
        self['key_red'] = Label(_('Kopia Zapasowa'))
        self['list'] = List([])
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'ok': self.backupImage,
         'red': self.backupImage})
        if pathExists('/media/usb/ImageBoot'):
            neoboot = 'usb'
        elif pathExists('/media/hdd/ImageBoot'):
            neoboot = 'hdd' 
        self.backupdir = '/media/' + neoboot + '/NeoBootImageBackup' 
        self.availablespace = '0'
        self.onShow.append(self.updateInfo)

    def updateInfo(self):
        if pathExists('/media/usb/ImageBoot'):
            neoboot = 'usb'
        elif pathExists('/media/hdd/ImageBoot'):
            neoboot = 'hdd' 
        device = '/media/' + neoboot + '' 
        usfree = '0'
        devicelist = ['cf',
         'hdd',
         'card',
         'usb',
         'usb2']
        for d in devicelist:
            test = '/media/' + d + '/ImageBoot/.neonextboot'
            if fileExists(test):
                device = '/media/' + d

        rc = system('df > /tmp/ninfo.tmp')
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find('/hdd') != -1:
                self.backupdir = '/media/' + neoboot + '/NeoBootImageBackup'
                device = '/media/' + neoboot + '' 

        f.close()
        if pathExists(self.backupdir) == 0 and createDir(self.backupdir):
            pass
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == device:
                    if totsp == 5:
                        usfree = parts[3]
                    else:
                        usfree = parts[2]
                    break

            f.close()
            os_remove('/tmp/ninfo.tmp')
        self.availablespace = usfree[0:-3]
        strview = _('Masz zainstalowane nas\xc5\xa7\xc4\x99puj\xc4\x85ce obrazy')
        self['lab1'].setText(strview)
        strview = _('Masz jeszcze wolne: ') + self.availablespace + ' MB'
        self['lab2'].setText(strview)
        imageslist = ['Flash']
        for fn in listdir('/media/' + neoboot + '/ImageBoot'):
            dirfile = '/media/' + neoboot + '/ImageBoot/' + fn
            if os_isdir(dirfile) and imageslist.append(fn):
                pass

        self['list'].list = imageslist

    def backupImage(self):
        image = self['list'].getCurrent()
        if image:
            self.backimage = image.strip()
            myerror = ''
            if self.backimage == 'Flash':
                myerror = _('Niestety nie mo\xc5\xbcna wykona\xc4\x87 kopii zapasowej z flesza t\xc4\x85 wtyczk\xc4\x85\nZainstaluj backupsuite do kopii obrazu z pamieci flesza')
            if int(self.availablespace) < 150:
                myerror = _('Brak miejca do zrobienia kopii obrazu. Potrzebne jest 150 Mb wolnego miejsca na kopie obrazu.')
            if myerror == '':
                message = _('Wykona\xc4\x87 kopi\xc4\x99 obrazu:') + image + ' teraz ?'
                ybox = self.session.openWithCallback(self.dobackupImage, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Potwierdzenie kopii zapasowej'))
            else:
                self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)

    def dobackupImage(self, answer):
        if answer is True:
            if pathExists('/media/usb/ImageBoot'):
                neoboot = 'usb'
            elif pathExists('/media/hdd/ImageBoot'):
                neoboot = 'hdd' 
            cmd = "echo -e '\n\n%s '" % _('Prosz\xc4\x99 czeka\xc4\x87, NeoBoot dzia\xc5\x82a, wykonywanie kopii zapasowej moze zajac kilka chwil, proces w toku...')
            cmd1 = '/bin/tar -cf ' + self.backupdir + '/' + self.backimage + '.tar /media/' + neoboot + '/ImageBoot/' + self.backimage + '  > /dev/null 2>&1'
            cmd2 = 'mv -f ' + self.backupdir + '/' + self.backimage + '.tar ' + self.backupdir + '/' + self.backimage + '.mb'
            cmd3 = "echo -e '\n\n%s '" % _('NeoBoot: Kopia Zapasowa KOMPLETNA !')
            self.session.open(Console, _('NeoBoot: Kopia Zapasowa Obrazu'), [cmd,
             cmd1,
             cmd2,
             cmd3])
            self.close()


class MBRestore(Screen):
    __module__ = __name__
    skin = '  \n\t<screen position="center,center" size="700,550" title="NeoBoot Przywracanie Obrazu">\n    <widget name="lab1" position="20,20" size="660,30" font="Regular;24" halign="center" valign="center" transparent="1"/>\n                <widget name="lab2" position="20,50" size="660,30" font="Regular;24" halign="center" valign="center" transparent="1"/>\n                <widget name="lab3" position="20,100" size="660,30" font="Regular;22" halign="center" valign="center" transparent="1"/>\n                <widget source="list" render="Listbox" position="40,130" zPosition="1" size="620,380" scrollbarMode="showOnDemand" transparent="1" >\n\t\t\t<convert type="StringList" />\n                </widget>\n                <ePixmap position="140,500" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" />\n                <ePixmap position="420,500" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" alphatest="on" zPosition="1" />\n                <widget name="key_red" position="140,500" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" />\n                <widget name="key_green" position="420,500" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="green" transparent="1" />\n        </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('')
        self['lab2'] = Label('')
        self['lab3'] = Label(_('Wybierz kopi\xc4\x99 kt\xc3\xb3r\xc4\x85 chcesz przywr\xc3\xb3ci\xc4\x87'))
        self['key_red'] = Label(_('Restore'))
        self['key_green'] = Label(_('Delete'))
        self['list'] = List([])
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'ok': self.restoreImage,
         'red': self.restoreImage,
         'green': self.deleteback})
        self.backupdir = '' + getNeoLocation() + 'NeoBootImageBackup'
        self.availablespace = '0'
        self.onShow.append(self.updateInfo)

    def updateInfo(self):
        linesdevice = open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'r').readlines()
        deviceneo = linesdevice[0][0:-1]
        device = deviceneo
        usfree = '0'
        devicelist = ['cf',
         'CF',
         'hdd',
         'card',
         'sd',
         'SD',
         'usb',
         'USB',
         'usb2']
        for d in devicelist:
            test = '/media/' + d + '/ImageBoot/.neonextboot'
            if fileExists(test):
                device = device + d

        rc = system('df > /tmp/ninfo.tmp')
        f = open('/proc/mounts', 'r')
        for line in f.readlines():
            if line.find('/hdd') != -1:
                self.backupdir = '' + getNeoLocation() + 'NeoBootImageBackup'
            elif line.find('/usb') != -1:
                self.backupdir = '' + getNeoLocation() + 'NeoBootImageBackup'
        f.close()
        if pathExists(self.backupdir) == 0 and createDir(self.backupdir):
            pass
        if fileExists('/tmp/ninfo.tmp'):
            f = open('/tmp/ninfo.tmp', 'r')
            for line in f.readlines():
                line = line.replace('part1', ' ')
                parts = line.strip().split()
                totsp = len(parts) - 1
                if parts[totsp] == device:
                    if totsp == 5:
                        usfree = parts[3]
                    else:
                        usfree = parts[2]
                    break

            f.close()
            os_remove('/tmp/ninfo.tmp')
        self.availablespace = usfree[0:-3]
        strview = _('Kopie Zapasowe znajduj\xc4\x85 si\xc4\x99 w katalogu /' + getNeoLocation() + 'NeoBootImageBackup')
        self['lab1'].setText(strview)
        strview = _('Ilo\xc5\x9b\xc4\x87 wolnego miejsca w Superbocie: ') + self.availablespace + ' MB'
        self['lab2'].setText(strview)
        imageslist = []
        for fn in listdir(self.backupdir):
            imageslist.append(fn)

        self['list'].list = imageslist

    def deleteback(self):
        image = self['list'].getCurrent()
        if image:
            self.delimage = image.strip()
            message = _('Wybierz obraz do przywr\xc3\xb3cenia lub usuni\xc4\x99cia:\n ') + image + '?'
            ybox = self.session.openWithCallback(self.dodeleteback, MessageBox, message, MessageBox.TYPE_YESNO)
            ybox.setTitle(_('Potwierdzenie Usuni\xc4\x99cia'))

    def dodeleteback(self, answer):
        if answer is True:
            cmd = "echo -e '\n\n%s '" % _('SuperBoot usuwanie plik\xc3\xb3w kopi zapasowej.....')
            cmd1 = 'rm ' + self.backupdir + '/' + self.delimage
            self.session.open(Console, _('SuperBoot: Pliki kopii zapasowej usuni\xc4\x99te'), [cmd, cmd1])
            self.updateInfo()

    def restoreImage(self):
        image = self['list'].getCurrent()
        if image:
            curimage = 'Flash'
            if fileExists('/.neonextboot'):
                f = open('/.neonextboot', 'r')
                curimage = f.readline().strip()
                f.close()
            self.backimage = image.strip()
            imagename = self.backimage[0:-3]
            myerror = ''
            if curimage == imagename:
                myerror = _('Sorry you cannot overwrite the image currently booted from. Please, boot from Flash to restore this backup.')
            if myerror == '':
                message = _('Przed przywracaniem sprawdz czy masz wolne miejsce na swoim urz\xc4\x85dzeniu - 300Mb \nCzy chcesz przywr\xc3\xb3ci\xc4\x87 ten obraz:\n ') + image + '?'
                ybox = self.session.openWithCallback(self.dorestoreImage, MessageBox, message, MessageBox.TYPE_YESNO)
                ybox.setTitle(_('Potwierdzenie Przywracania'))
            else:
                self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)

    def dorestoreImage(self, answer):
        if answer is True:
            imagename = self.backimage[0:-3]
            cmd = "echo -e '\n\n%s '" % _('Wait please, NeoBoot is working: ....Restore in progress....')
            cmd1 = 'mv -f ' + self.backupdir + '/' + self.backimage + ' ' + self.backupdir + '/' + imagename + '.tar'
            cmd2 = '/bin/tar -xf ' + self.backupdir + '/' + imagename + '.tar -C /'
            cmd3 = 'mv -f ' + self.backupdir + '/' + imagename + '.tar ' + self.backupdir + '/' + imagename + '.mb'
            cmd4 = 'sync'
            cmd5 = "echo -e '\n\n%s '" % _('Superboot: Restore COMPLETE !')
            self.session.open(Console, _('NeoBoot: Restore Image'), [cmd,
             cmd1,
             cmd2,
             cmd3,
             cmd4,
             cmd5])
            self.close()

    def myclose(self):
        self.close()

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()


class MenagerDevices(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="Menad\xc5\xbcer urz\xc4\x85dze\xc5\x84">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Uruchomic Menad\xc5\xbcer urz\xc4\x85dze\xc5\x84 ?')
        self['key_red'] = Label(_('Uruchom'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.MD})

    def MD(self):
        try:
                from Plugins.Extensions.NeoBoot.files.devices import ManagerDevice
                self.session.open(ManagerDevice)
        except:
            False


class UnistallMultiboot(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="Odinstaluj NeoBoota">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Czy odinstalowa\xc4\x87 NeoBoota ?')
        self['key_red'] = Label(_('Odinstaluj'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.usun})

    def usun(self):
        message = _('Je\xc5\x9bli wybierzesz Tak, zostan\xc4\x85 przywr\xc3\xb3cone ustawienia obrazu pli \nMultibot zostanie tylko odinstalowany. \nBedziesz m\xc3\xb3g\xc5\x82 go zainstalowa\xc4\x87 ponownie')
        ybox = self.session.openWithCallback(self.reinstallneoboot, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle(_('Delete Confirmation'))

    def reinstallneoboot(self, answer):
        if answer is True:
            cmd0 = "echo -e '\n\nPrzywracanie ustawie\xc5\x84.....'"
            cmd = "echo -e '\n%s '" % _('Czekaj usuwam...')
            cmd1 = 'rm /sbin/multinit; sleep 2'
            cmd1a = "echo -e '\nNeoBoot usuwanie mened\xc5\xbcera rozruchu....'"
            cmd2 = 'rm /sbin/init; sleep 2'
            cmd3 = 'ln -sfn /sbin/init.sysvinit /sbin/init'
            cmd4 = 'chmod 777 /sbin/init; sleep 2'
            cmd4a = "echo -e '\nNeoBoot restoring media mounts....'"
            cmd6 = 'rm ' + getNeoLocation() + 'ImageBoot/.neonextboot;rm /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location; sleep 2'
            cmd7 = 'rm ' + getNeoLocation() + 'ImageBoot/.Flash; rm ' + getNeoLocation() + 'ImageBoot/.version'
            cmd7a = "echo -e '\n\nOdinstalowywanie neoboota...'"
            cmd8 = "echo -e '\n\nPrzywracanie montowania.'"
            cmd9 = "echo -e '\n\nNeoBoot odinstalowany, mozesz zrobic reinstalacje.'"
            self.session.openWithCallback(self.close, Console, _('NeoBoot is reinstall...'), [cmd0,
             cmd,
             cmd1,
             cmd1a,
             cmd2,
             cmd3,
             cmd4,
             cmd4a,
             cmd6,
             cmd7,
             cmd7a,
             cmd8,
             cmd9])
            self.close()


class ReinstllNeoBoot(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="Update NeoBoot">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Przywrocic kopie NeoBoota z lokalizacji /media/neoboot  ?')
        self['key_red'] = Label(_('Backup'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.reinstallMB})

    def reinstallMB(self):
        system('/bin/tar -xzvf ' + getNeoLocation() + 'NeoBoot_Backup.tar.gz -C /')
        self.close()


class UpdateNeoBoot(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="Update NeoBoot">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Aktualizowac neoboota na wszystkich obrazach ?')
        self['key_red'] = Label(_('Zainstaluj'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.mbupload})

    def mbupload(self):
        self.session.open(MyUpgrade2)


class MyUpgrade2(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center,center" size="900,450" title="NeoBoot">\n\t\t<widget name="lab1" position="23,42" size="850,350" font="Regular;35" halign="center" valign="center" transparent="1" />\n</screen>'
    else:
        skin = '<screen position="center,center" size="400,200" title="NeoBoot">\n\t\t<widget name="lab1" position="10,10" size="380,180" font="Regular;24" halign="center" valign="center" transparent="1"/>\n\t</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label(_('[NeoBoot]Prosze czeka\xc4\x87, aktualizacja w toku...'))
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
        if mypath2 != 'Flash':
            self.myClose(_('Sorry, NeoBoot can installed or upgraded only when booted from Flash STB'))
            self.close()
        else:
            for fn in listdir('%sImageBoot'  % getNeoLocation() ):
                dirfile = '%sImageBoot/'  % getNeoLocation() + fn
                if isdir(dirfile):
                    target = dirfile + '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
                    cmd = 'rm -r ' + target + ' > /dev/null 2>&1'
                    system(cmd)
                    cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot ' + target
                    system(cmd)

            out = open('%sImageBoot/.version'  % getNeoLocation(), 'w')
            out.write(PLUGINVERSION)
            out.close()
            self.myClose(_('NeoBoot successfully updated. You can restart the plugin now.\nHave fun !!'))

    def myClose(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

class MBDeleUpload(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="NeoBoot - wyczy\xc5\x9b\xc4\x87 pobrane image">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Czy na pewno chcesz usun\xc4\x85\xc4\x87 obraz z katalogu ImagesUpload ?\n\nJe\xc5\x9bli wybierzesz czerwony przycisk na pilocie to usuniesz wszystkie obrazy ZIP z katalogu ImagesUpload')
        self['key_red'] = Label(_('Wyczy\xc5\x9b\xc4\x87'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.usunup})

    def usunup(self):
        message = _('Czy napewno chcesz wyczy\xc5\x9bci\xc4\x87')
        ybox = self.session.openWithCallback(self.pedeleup, MessageBox, message, MessageBox.TYPE_YESNO)
        ybox.setTitle(_('Czyszenie z pobranych obraz\xc3\xb3w'))

    def pedeleup(self, answer):
        if answer is True:
            cmd = "echo -e '\n\n%s '" % _('Czekaj usuwam.....')
            cmd1 = 'rm -r ' + getNeoLocation() + 'ImagesUpload/*.zip' 
            self.session.open(Console, _('Usuwanie pobranych obraz\xc3\xb3w....'), [cmd, cmd1])
            self.close()


class BackupMultiboot(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="590,330" title="Backup NeoBoot">\n\t\t<widget source="list" render="Listbox" position="10,16" size="570,300" scrollbarMode="showOnDemand" >\n\t\t\t<convert type="TemplatedMultiContent">\n                \t\t{"template": [\n                    \t\t\tMultiContentEntryText(pos = (50, 1), size = (520, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),\n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),\n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 22)],\n                    \t\t\t"itemHeight": 36\n                \t\t}\n            \t\t</convert>\n\t\t</widget>\n        </screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.downList()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})

    def downList(self):
        self.list = []
        mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('Wykonac kompletna kopie NeoBoota ?'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self):
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]
        if self.sel == 0:
            cmd = 'sh /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/NeoBoot.sh -i'
            self.session.open(Console, _('Kopia zapasowa zostanie zapisana w lokalizacji /media/neoboot. Trwa wykonywanie....'), [cmd])
            self.close()


class SetPasswd(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="Zmiana Hasla">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Czy skasowac haslo ?')
        self['key_red'] = Label(_('Uruchom'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.passwd})

    def passwd(self):
        os.system('passwd -d root')
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
        restartbox.setTitle(_('Restart GUI now?'))

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

class ReinstallKernel(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="Module kernel">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Reinstalacja j\xc4\x85dra.\n\nZainstalowa\xc4\x87 ?')
        self['key_red'] = Label(_('Instalacja'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.kernel_image})

    def kernel_image(self):
            os.system('echo "Flash "  > ' + getNeoLocation() + 'ImageBoot/.neonextboot')
            out = open('' + getNeoLocation() + 'ImagesUpload/.kernel/used_flash_kernel', 'w')
            out.write('Used Kernel:  Flash')
            out.close()            
            cmd1 = 'rm -f /home/root/*.ipk; opkg download kernel-image; sleep 2; opkg install --force-maintainer --force-reinstall --force-overwrite --force-downgrade /home/root/*.ipk; opkg configure update-modules'
            self.session.open(Console, _('NeoBoot....'), [cmd1])
            self.close() 

class ListTv(Screen):
    __module__ = __name__
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center,center" size="900,450" title="NeoBoot">\n\t\t<widget name="lab1" position="23,42" size="850,350" font="Regular;35" halign="center" valign="center" transparent="1" />\n</screen>'
    else:
        skin = '<screen position="center,center" size="400,200" title="NeoBoot">\n\t\t<widget name="lab1" position="10,10" size="380,180" font="Regular;24" halign="center" valign="center" transparent="1"/>\n\t</screen>'

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
        f2 = open('' + getNeoLocation() + 'ImageBoot/.neonextboot', 'r')
        mypath2 = f2.readline().strip()
        f2.close()
        if mypath2 != 'Flash':
            self.myClose(_('Sorry, NeoBoot can installed or upgraded only when booted from Flash.'))
            self.close()
        else:
            os.system('mv /etc/enigma2 /etc/enigma2.tmp')
            os.system('mkdir -p /etc/enigma2')
            os.system('cp -f /etc/enigma2.tmp/*.tv /etc/enigma2')
            os.system('cp -f /etc/enigma2.tmp/*.radio /etc/enigma2')
            os.system('cp -f /etc/enigma2.tmp/lamedb /etc/enigma2')
            for fn in listdir('' + getNeoLocation() + 'ImageBoot'):
                dirfile = '' + getNeoLocation() + 'ImageBoot/' + fn
                if isdir(dirfile):
                    target = dirfile + '/etc/'
                    cmd = 'cp -r -f /etc/enigma2 ' + target
                    system(cmd)
                    target1 = dirfile + '/etc/tuxbox'
                    cmd = 'cp -r -f /etc/tuxbox/satellites.xml ' + target1
                    system(cmd)
                    target2 = dirfile + '/etc/tuxbox'
                    cmd = 'cp -r -f /etc/tuxbox/terrestrial.xml ' + target2
                    system(cmd)

            os.system('rm -f -R /etc/enigma2')
            os.system('mv /etc/enigma2.tmp /etc/enigma2/')
            self.myClose(_('NeoBoot successfully updated list tv.\nHave fun !!'))

    def myClose(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()


class IPTVPlayer(Screen):
    __module__ = __name__
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen position="center,center" size="900,450" title="IPTVPlayer">\n\t\t<widget name="lab1" position="23,42" size="850,350" font="Regular;35" halign="center" valign="center" transparent="1" />\n</screen>'
    else:
        skin = '<screen position="center,center" size="400,200" title="IPTVPlayer">\n\t\t<widget name="lab1" position="10,10" size="380,180" font="Regular;24" halign="center" valign="center" transparent="1"/>\n\t</screen>'

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
        f2 = open('' + getNeoLocation() + 'ImageBoot/.neonextboot', 'r')
        mypath2 = f2.readline().strip()
        f2.close()
        if mypath2 != 'Flash':
            self.myClose(_('Sorry, NeoBoot can installed or upgraded only when booted from Flash.'))
            self.close()
        elif not fileExists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer'):
            self.myClose(_('Sorry, IPTVPlayer not found.'))
            self.close()
        else:
            for fn in listdir('' + getNeoLocation() + 'ImageBoot'):
                dirfile = '' + getNeoLocation() + 'ImageBoot/' + fn
                if isdir(dirfile):
                    target = dirfile + '/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer'
                    cmd = 'rm -r ' + target + ' > /dev/null 2>&1'
                    system(cmd)
                    cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer ' + target
                    system(cmd)

            self.myClose(_('NeoBoot successfully updated IPTVPlayer.\nHave fun !!'))

    def myClose(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()

class SetPasswd(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="Zmiana Hasla">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Czy skasowac haslo ?')
        self['key_red'] = Label(_('Uruchom'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.passwd})

    def passwd(self):
        os.system('passwd -d root')
        restartbox = self.session.openWithCallback(self.restartGUI, MessageBox, _('GUI needs a restart.\nDo you want to Restart the GUI now?'), MessageBox.TYPE_YESNO)
        restartbox.setTitle(_('Restart GUI now?'))

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

class CheckInstall(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="Zmiana Hasla">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('Sprawdzanie poprawnosci zainstalwoanych modulow dla NeoBoota')
        self['key_red'] = Label(_('Uruchom'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.neocheck})
         
    def neocheck(self):
        try:
            cmd = ' /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/module_neoboot.sh -i'
            self.session.openWithCallback(self.close, Console, _('NeoBoot....'), [cmd,
             cmd]) 
            self.close()

        except:
            False

class MultiBootMyHelp(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = '<screen name=" NeoBoot" position="center,center" size="1920,1080" title="NeoBoot - Opis" flags="wfNoBorder">\n<eLabel text="INFORMACJE NeoBoot" font="Regular; 35" position="69,66" size="1777,96" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" /><widget name="lab1" position="69,162" size="1780,885" font="Regular;35" />\n</screen>'
    else:
        skin = '<screen name=" NeoBoot" position="center,center" size="1280,720" title="NeoBoot - Opis">\n<widget name="lab1" position="18,19" size="1249,615" font="Regular;20" />\n</screen>'
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
        message = ''
        message += 'NeoBoot Wersja ' + PLUGINVERSION + '  Enigma2\n\n'
        message += 'NeoBoot opiera si\xc4\x99 na EGAMIBoot < mod by gutosie >\n\n'
        message += 'Autor EGAMIBoota zezwolil na rozwijanie i edycje NeoBoot - Thanks/Dzi\xc4\x99ki\n\n'
        message += 'nfidump by gutemine - Thanks/Dzi\xc4\x99ki\n\n'
        message += 'ubi_reader by Jason Pruitt  - Thanks/Dzi\xc4\x99ki\n\n'
        message += 'T\xc5\x82umaczenie: gutosie\n\n'
        message += _('Podziekowania wszystkim tu niewspomnianym za udzielenie pomocy w ulepszaniu NeoBoota \n\n')
        message += _('Udanej zabawy :)\n\n')      
                
        self['lab1'].show()
        self['lab1'].setText(message)


class TunerInfo(Screen):
    __module__ = __name__
    skin = '\n\t<screen position="center,center" size="700,300" title="NeoBoot - Tunery Sat">\n\t\t<widget name="lab1" position="20,20" size="660,215" font="Regular;24" halign="center" valign="center" transparent="1"/><ePixmap position="280,250" size="140,40" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" alphatest="on" zPosition="1" /><widget name="key_red" position="280,250" zPosition="2" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="red" transparent="1" /></screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self['lab1'] = Label('NeoBoot: Lista wspieranych modeli STB.')
        self['key_red'] = Label(_('Uruchom - Red'))
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'back': self.close,
         'red': self.iNFO})
         
    def iNFO(self):
        try:
            cmd = ' cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/stbinfo'
            cmd1 = ''
            self.session.openWithCallback(self.close, Console, _('NeoBoot....'), [cmd,
                     cmd1]) 
            self.close()

        except:
            False



def myboot(session, **kwargs):
    session.open(MBTools)


def Plugins(path, **kwargs):
    global pluginpath
    pluginpath = path
    return PluginDescriptor(name='NeoBoot', description='MENU NeoBoot', icon=None, where=PluginDescriptor.WHERE_PLUGINMENU, fnc=myboot)
