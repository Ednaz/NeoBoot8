#!/usr/bin/python
# -*- coding: utf-8 -*-  
                               
from __init__ import _                                                                                                                                                    
from Plugins.Extensions.NeoBoot.files.stbbranding import getNeoLocation, getKernelVersionString, getKernelImageVersion, getCPUtype, getCPUSoC,  getImageNeoBoot, getBoxVuModel, getBoxHostName, getTunerModel
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

class InstallImage(Screen, ConfigListScreen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="82,105" size="1650,875" title="NeoBoot - Installation">
                  <eLabel position="41,107" size="1541,2" backgroundColor="blue" foregroundColor="blue" name="linia" />
                  <eLabel position="40,744" size="1545,2" backgroundColor="blue" foregroundColor="blue" name="linia" />
                  <eLabel text="NeoBoot opcje dla instalowanego obrazu" font="Regular; 38" position="40,24" size="1538,74" halign="center" foregroundColor="red" backgroundColor="black" transparent="1" />
                  <widget name="config" position="38,134" size="1547,593" font="Regular; 32" itemHeight="42" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/selektor.png" scrollbarMode="showOnDemand" transparent="1" backgroundColor="transpBlack" />
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/redcor.png" position="84,820" size="178,28" alphatest="on" />
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/greencor.png" position="457,820" size="178,29" alphatest="on" />
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellowcor.png" position="884,823" size="169,28" alphatest="on" />
                  <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/bluecor.png" position="1288,821" size="167,29" alphatest="on" />
                  <widget name="HelpWindow" position="330,310" zPosition="5" size="1,1" transparent="1" alphatest="on" />
                  <widget name="key_red" position="36,762" zPosition="1" size="284,53" font="Regular; 35" halign="center" valign="center" backgroundColor="#FF0000" transparent="1" foregroundColor="red" />
                  <widget name="key_green" position="403,760" zPosition="1" size="293,55" font="Regular; 35" halign="center" valign="center" backgroundColor="#00FF00" transparent="1" foregroundColor="green" />
                  <widget name="key_yellow" position="816,761" zPosition="1" size="295,54" font="Regular; 35" halign="center" valign="center" backgroundColor="#FFFF00" transparent="1" foregroundColor="yellow" />
                  <widget name="key_blue" position="1233,760" zPosition="1" size="272,56" font="Regular; 35" halign="center" valign="center" backgroundColor="#0000FF" transparent="1" foregroundColor="blue" />\
               </screen>"""
    else:
          skin = """<screen position="0,0" size="1280,720" title="NeoBoot - Installation">
                    <ePixmap position="0,0" zPosition="-1" size="1280,720" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1frame_base-fs8.png"  />
                    <eLabel text="NeoBoot opcje dla instalowanego obrazu" font="Regular; 28" position="10,30" size="700,30" halign="center" foregroundColor="#58ccff" backgroundColor="black" transparent="1" />
                    <widget name="config" position="0,150" size="780,450" font="Regular; 22" itemHeight="32" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/listselection700x32-fs8.png" scrollbarMode="showOnDemand" transparent="1" backgroundColor="transpBlack" />
                    <widget name="HelpWindow" position="100,500" zPosition="5" size="1,1" transparent="1" alphatest="on" />
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/red25.png" position="0,650" size="250,40" alphatest="blend" />
                    <widget name="key_red" position="0,670" zPosition="2" size="250,40"  font="Regular; 20" halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/green25.png" position="200,650" size="230,36" alphatest="blend" />
                    <widget name="key_green" position="200,670" size="230,38" zPosition="1" font="Regular; 20"  halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/yellow25.png" position="400,650" size="230,36" alphatest="blend" />
                    <widget name="key_yellow" position="400,670" size="230,38" zPosition="1" font="Regular; 20"  halign="center" backgroundColor="transpBlack" transparent="1" foregroundColor="white" />
                    <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/blue25.png" position="600,650" size="230,36" alphatest="blend" />
                    <widget source="session.VideoPicture" render="Pig" position=" 836,89" size="370,208" zPosition="3" backgroundColor="#ff000000"/>
                    <ePixmap position="920,500" zPosition="1" size="228,130" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/1matrix.png" />
                  </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        fn = 'NewImage'
        sourcelist = []                        
        for fn in os.listdir('%sImagesUpload' % getNeoLocation() ):
            if fn.find('.zip') != -1:
                fn = fn.replace('.zip', '')
                sourcelist.append((fn, fn))
                continue
            if fn.find('.tar.xz') != -1:
                fn = fn.replace('.tar.xz', '')
                sourcelist.append((fn, fn))
                continue
            if fn.find('.nfi') != -1:
                fn = fn.replace('.nfi', '')
                sourcelist.append((fn, fn))
                continue
        if len(sourcelist) == 0:
            sourcelist = [('None', 'None')]
        self.source = ConfigSelection(choices=sourcelist)
        self.target = ConfigText(fixed_size=False)
        self.stopenigma = ConfigYesNo(default=False)     
        self.CopyFiles = ConfigYesNo(default=True)
        if getCPUtype() == 'ARMv7' and getCPUSoC() or getBoxHostName() == ['7444s', 
             '7376',                           
             '7252s',
             '7278', 
             '72604',
             'vuultimo4k'             
             'vusolo4k',                         
             'vuuno4k',                          
             'vuuno4kse',
             'vuduo4k',
             'vuzero4k']: 
            self.CopyKernel = ConfigYesNo(default=True)
        else:
            self.CopyKernel = ConfigYesNo(default=False)        
        self.TvList = ConfigYesNo(default=False) 
        self.Montowanie = ConfigYesNo(default=False)         
        self.LanWlan = ConfigYesNo(default=False)
        if getCPUtype() == 'ARMv7' and getCPUSoC() or getBoxHostName() == ['osmio4k', 
             'ax60',
             'sf8008', 
             'bcm7251',
             'sf4008',
             'et1x000',
             'dm920',
             'bcm7251s',
             'h7',
             'hi3798mv200'
             'zgemmah9s',
             'bcm7252s',
             'gbquad4k',              
             'ustym4kpro',
             '3798mv200'                                       
             'dm900'] :
            self.Sterowniki = ConfigYesNo(default=True)
        else:
            self.Sterowniki = ConfigYesNo(default=False)                                                
        self.InstallSettings = ConfigYesNo(default=False)        
        self.ZipDelete = ConfigYesNo(default=False)                 
        self.RepairFTP = ConfigYesNo(default=False)
        self.SoftCam = ConfigYesNo(default=False)
        self.MediaPortal = ConfigYesNo(default=False)                                                                             
        self.BlackHole = ConfigYesNo(default=False)
        self.target.value = ''
        self.curselimage = ''

        try:
            if self.curselimage != self.source.value:
                self.target.value = self.source.value[:-13]
                self.curselimage = self.source.value
        except:
            pass

        self.createSetup()
        ConfigListScreen.__init__(self, self.list, session=session)
        self.source.addNotifier(self.typeChange)
        self['actions'] = ActionMap(['OkCancelActions',
         'ColorActions',
         'CiSelectionActions',
         'VirtualKeyboardActions'], {'cancel': self.cancel,
         'red': self.cancel,
         'green': self.imageInstall,
         'yellow': self.HelpInstall,
         'blue': self.openKeyboard}, -2)        
        self['key_green'] = Label(_('Install'))
        self['key_red'] = Label(_('Cancel'))
        self['key_yellow'] = Label(_('Help'))
        self['key_blue'] = Label(_('Keyboard'))        
        self['HelpWindow'] = Pixmap()
        self['HelpWindow'].hide()

    def createSetup(self):
        self.list = []
        self.list.append(getConfigListEntry(_('Source Image file'), self.source))
        self.list.append(getConfigListEntry(_('Image Name'), self.target)) 
        self.list.append(getConfigListEntry(_('Zatrzymać procesy E2 na czas instalacji ?'), self.stopenigma))          
        self.list.append(getConfigListEntry(_('Copy files from Flash to the installed image ?'), self.CopyFiles ))         
        self.list.append(getConfigListEntry(_('Copy the kernel of the installed system (recommended ?'), self.CopyKernel ))         
        self.list.append(getConfigListEntry(_('Copy the channel list ?'), self.TvList))          
        self.list.append(getConfigListEntry(_('Copy mounting disks ? (Recommended)'), self.Montowanie))         
        self.list.append(getConfigListEntry(_('Copy network settings LAN-WLAN ?'), self.LanWlan))
        self.list.append(getConfigListEntry(_('Copy the drivers ? (Recommended only other image.)'), self.Sterowniki))                                                                
        self.list.append(getConfigListEntry(_('Copy Settings to the new Image'), self.InstallSettings))                                                                                
        self.list.append(getConfigListEntry(_('Delete Image zip after Install ?'), self.ZipDelete)) 
        self.list.append(getConfigListEntry(_('Repair FTP ? (Recommended only other image if it does not work.)'), self.RepairFTP))
        self.list.append(getConfigListEntry(_('Copy config SoftCam ?'), self.SoftCam)) 
        self.list.append(getConfigListEntry(_('Copy MediaPortal ?'), self.MediaPortal))                 
        self.list.append(getConfigListEntry(_('Path BlackHole ? (Not recommended for VuPlus)'), self.BlackHole))
     
    def HelpInstall(self):
        if fileExists('/.multinfo'):
            mess = _('Information available only when running Flash.')
            self.session.open(MessageBox, mess, MessageBox.TYPE_INFO)
        else:
            self.session.open(HelpInstall)
               
        

    def typeChange(self, value):
        self.createSetup()
        self['config'].l.setList(self.list)
        if self.curselimage != self.source.value:
            self.target.value = self.source.value[:-13]
            self.curselimage = self.source.value

    def openKeyboard(self):
        sel = self['config'].getCurrent()
        if sel:
            if sel == self.target:
                if self['config'].getCurrent()[1].help_window.instance is not None:
                    self['config'].getCurrent()[1].help_window.hide()
            self.vkvar = sel[0]
            if self.vkvar == _('Image Name'):
                self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)
        return

    def VirtualKeyBoardCallback(self, callback = None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].setValue(callback)
            self['config'].invalidate(self['config'].getCurrent())
        return

    def imageInstall(self):
        if self.check_free_space():
            pluginpath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
            myerror = ''
            source = self.source.value.replace(' ', '')
            target = self.target.value.replace(' ', '')
            for fn in os.listdir('%sImageBoot' % getNeoLocation()):
                if fn == target:
                    myerror = _('Sorry, an Image with the name ') + target + _(' is already installed.\n Please try another name.')
                    continue

            if source == 'None':
                myerror = _('You have to select one Image to install.\nPlease, upload your zip file in the folder: %sImagesUpload and select the image to install.')
            if target == '':
                myerror = _('You have to provide a name for the new Image.')
            if target == 'Flash':
                myerror = _('Sorry this name is reserved. Choose another name for the new Image.')
            if len(target) > 35:
                myerror = _('Sorry the name of the new Image is too long.')
            if myerror:
                myerror
                self.session.open(MessageBox, myerror, MessageBox.TYPE_INFO)
            else:
                myerror
                message = "echo -e '"
                message += _('NeoBot started installing new image.\n')
                message += _('The installation process may take a few minutes.\n')
                message += _('Please: DO NOT reboot your STB and turn off the power.\n')
                message += _('Please, wait...\n')                
                message += "'"
                cmd1 = 'python ' + pluginpath + '/ex_init.py'
                cmd = '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s' % (cmd1,
                 source,
                 target.replace(' ', '.'),
                 str(self.stopenigma.value),                  
                 str(self.CopyFiles.value),                 
                 str(self.CopyKernel.value),                 
                 str(self.TvList.value),                
                 str(self.Montowanie.value),                 
                 str(self.LanWlan.value),
                 str(self.Sterowniki.value),                                                                                                                        
                 str(self.InstallSettings.value), 
                 str(self.ZipDelete.value),                                                                    
                 str(self.RepairFTP.value),                                  
                 str(self.SoftCam.value), 
                 str(self.MediaPortal.value),                 
                 str(self.BlackHole.value))  
                print '[NEO-BOOT]: ', cmd
                self.session.open(Console, _('NEOBoot: Install new image'), [message, cmd])


    def check_free_space(self):
        if Freespace('%sImagesUpload' % getNeoLocation()) < 500000:
            self.session.open(MessageBox, _('Not enough free space on %s !!\nYou need at least 500Mb free space.\n\nExit plugin.' % getNeoLocation() ), type=MessageBox.TYPE_ERROR)
            return False
        return True

    def cancel(self):
        self.close()

class HelpInstall(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="center,center" size="1920,1080" borderWidth="0" borderColor="transpBlack" flags="wfNoBorder">
                    <eLabel text="Informacje instalacji image w NeoBoot" font="Regular; 35" position="71,20" size="1777,112" halign="center" foregroundColor="yellow" backgroundColor="black" transparent="1" />
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
        
        message = _('Source Image file')
        message += _(' -Wybierz kursorem pilota oprogramowanie do zainstalowania (w lewo lub prawo).\n\n')  
              
        message += _('Image Name')
        message += _(' -Zmień nazwę image - aby zmienić naciśnij na pilocie niebieski.\n\n')   
             
        message += _('Do not copy files from Flash to the installed image ?')
        message += _(' - po zaznaczeniu tej opcji nie zostanie nic skopiowane z image flash do instalowanego image w neoboot. \n\n')  
              
        message += _('Copy the kernel of the installed system (recommended ) ?')
        message += _(' - po zaznaczeniu tej opcji zostanie skopiowany plik jądra (kernel) instalowanego image do neoboota, zalecane tylko dla STB vuplus \n\n')
                
        message += _('Copy the channel list ?')
        message += _(' - opcja kopiuje listę kanałów z flasha do instalowanego image w neoboocie.\n\n')
                
        message += _('Copy mounting disks ? (Recommended)')
        message += _(' - opcja przenosi do instalowanego image w neoboot ustawienia montowania podłaczonych urządzeń do tunera.\n\n')
                
        message += _('Copy network settings LAN-WLAN ?')
        message += _(' - opcja przenosi pliki z zawartymi ustawieniami dla sieci lan i wlan. \n\n ')
                
        message += _('Copy the drivers ? (Recommended only other image.)')  
        message += _(' - opcja przenosi z flasza sterowniki do instalowanego image w neoboocie, zalecane tylko w przypadku jeśli instalujemy image od innego model niż posiadamy.\n\n') 
                      
        message += _('Copy Settings to the new Image')
        message += _(' - opcja kopiuje ustawienia oprogramowania z flasza do instalowanego systemu w neoboocie.\n\n')
                
        message += _('Delete Image zip after Install ?')
        message += _(' - po instalacji, opcja kasuje plik zip image z katalogu ImagesUpload. \n\n')
                
        message += _('Repair FTP ? (Recommended only other image if it does not work.)')
        message += _(' - opcja w niektórych przypadkach naprawia w instalowanym image polączenie FTP (ang. File Transfer Protocol) \n\n')
                
        message += _('Copy config SoftCam ?')
        message += _(' - opcja kopiuje configi oscama i cccam (openpli -domyślnie)\n\n')
                
        message += _('Path BlackHole ? (Not recommended for VuPlus)')  
        message += _(' - opcja przeznaczona dla image blackhole, pomaga uruchomić BH w neoboot \n\n')
                     
        self['lab1'].show()
        self['lab1'].setText(message)
                
def Freespace(dev):
    statdev = os.statvfs(dev)
    space = statdev.f_bavail * statdev.f_frsize / 1024
    print '[NeoBoot] Free space on %s = %i kilobytes' % (dev, space)
    return space