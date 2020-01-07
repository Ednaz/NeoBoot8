#!/usr/bin/python
# -*- coding: utf-8 -*-  
#echo "Flash "  >>  '+ getImageNeoBoot() + 'ImagesUpload/.kernel/used_flash_kernel;

from __init__ import _
from Plugins.Extensions.NeoBoot.files import Harddisk                                                                                                                                                     
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


class StartImage(Screen):
    screenwidth = getDesktop(0).size().width()
    if screenwidth and screenwidth == 1920:
        skin = """<screen position="center, center" size="1241, 850" title="NeoBoot">
        \n\t\t\t<ePixmap position="491, 673" zPosition="-2" size="365, 160" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/matrixhd.png" />
        <widget source="list" render="Listbox" position="20, 171" size="1194, 290" scrollbarMode="showOnDemand">\n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (90, 1), size = (920, 66), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (8, 4), size = (66, 66), png = 1),
        \n                    \t\t\t],
        \n                    \t\t\t"fonts": [gFont("Regular", 40)],\n                    \t\t\t"itemHeight": 66\n                \t\t}
        \n            \t\t</convert>\n\t\t</widget>
        \n         <widget name="label1" position="21, 29" zPosition="1" size="1184, 116" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        <widget name="label2" position="22, 480" zPosition="-2" size="1205, 168" font="Regular;35" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="red" />
        \n\t\t        </screen>"""
    else:
        skin = """<screen position="center, center" size="835, 500" title="NeoBoot">
        \n\t\t\t           <ePixmap position="0,0" zPosition="-1" size="835,500" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/frame835x500.png"  />
        <widget source="list" render="Listbox" position="16, 150" size="800, 40"    selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/listselection800x35.png" scrollbarMode="showOnDemand">
        \n\t\t\t\t<convert type="TemplatedMultiContent">
        \n                \t\t{"template": [
        \n                    \t\t\tMultiContentEntryText(pos = (180, 0), size = (520, 36), flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0),
        \n                    \t\t\tMultiContentEntryPixmapAlphaTest(pos = (4, 2), size = (36, 36), png = 1),
        \n                    \t\t\t],\n                    \t\t\t"fonts": [gFont("Regular", 22)],
        \n                    \t\t\t"itemHeight": 35\n               \t\t}\n            \t\t</convert>
        \n\t\t</widget>\n<widget name="label1" font="Regular; 26" position="15, 70" size="803, 58" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />
        <widget name="label2" position="40, 232" zPosition="2" size="806, 294" font="Regular;25" halign="center" valign="center" backgroundColor="black" transparent="1" foregroundColor="#00cc99" />
        \n\t\t        </screen>"""

    __module__ = __name__
    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self['list'] = List(self.list)
        self.select()
        self['actions'] = ActionMap(['WizardActions', 'ColorActions'], {'ok': self.KeyOk,
         'back': self.close})
        self['label1'] = Label(_('Start the chosen system now ?'))
        self['label2'] = Label(_('Select OK to run the image.'))
        
    def select(self):
        self.list = []
        mypath = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot'
        if not fileExists(mypath + 'icons'):
            mypixmap = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/images/ok.png'
        png = LoadPixmap(mypixmap)
        res = (_('OK Start image...'), png, 0)
        self.list.append(res)
        self['list'].list = self.list

    def KeyOk(self): 
        if getImageNeoBoot() != 'Flash': 
            if not fileExists('%sImageBoot/%s/.control_ok' % ( getNeoLocation(),  getImageNeoBoot())):                                  
                cmd = _("echo -e '[NeoBoot] Uwaga!!! po poprawnym starcie wybranego oprogramowania w neoboot,\nnalezy uruchomic NEOBOOTA by potwierdzic prawidlowy start image.\n\nNacisnij OK lub exit na pilocie by kontynuowac...\n\n\n'") 
                self.session.openWithCallback(self.StartImageInNeoBoot, Console, _('NeoBoot: Start image...'), [cmd])
            else:
                self.StartImageInNeoBoot()
        else:
            self.StartImageInNeoBoot()

    def StartImageInNeoBoot(self):                              
        if getImageNeoBoot() != 'Flash':
            if fileExists('%sImageBoot/%s/.control_ok' % ( getNeoLocation(),  getImageNeoBoot())): 
                system('touch /tmp/.control_ok ') 
            else:
                system('touch %sImageBoot/%s/.control_boot_new_image ' % ( getNeoLocation(), getImageNeoBoot() ))

        system('chmod 755 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/*')               
        self.sel = self['list'].getCurrent()
        if self.sel:
            self.sel = self.sel[2]     
        if self.sel == 0:          
            if fileExists('/media/mmc/etc/init.d/neobootmount.sh'):
                os.system('rm -f /media/mmc/etc/init.d/neobootmount.sh;')


#################_____ARM____##########################  
            #Zgemma h7S ARM  ARM - h7s_mmcblk0p2.sh              
            if getBoxHostName() == 'h7' or getCPUSoC() == 'bcm7251s':                  
                        if not fileExists('%sImagesUpload/.kernel/flash-kernel-%s.bin' % (getNeoLocation(), getBoxHostName()) ):
                            self.myclose2(_('\n\n\nError - w lokalizacji %sImagesUpload/.kernel/  \nnie odnaleziono pliku kernela flash-kernel-%s.bin ' % getNeoLocation() % ( getBoxHostName()) ))
                        else:
                            if getImageNeoBoot() == 'Flash':                                                
                                if fileExists('/.multinfo'):
                                    cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')
                                    cmd1 = 'cd /media/mmc; ln -sf "init.sysvinit" "/media/mmc/sbin/init"; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_kernel.sh '                  

                                elif not fileExists('/.multinfo'): 
                                    cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')
                                    cmd1 = 'ln -sf "init.sysvinit" "/sbin/init"; reboot -f'  

                            elif  getImageNeoBoot() != 'Flash':                                                 
                                if not fileExists('/.multinfo'):  
                                    if not fileExists('%sImageBoot/%s/boot/zImage.%s' % ( getNeoLocation(), getImageNeoBoot(), getBoxHostName())):  
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')
                                        cmd1 = 'ln -sfn /sbin/neoinitarm /sbin/init; reboot -f'
                                    
                                    elif fileExists('%sImageBoot/%s/boot/zImage.%s' % ( getNeoLocation(), getImageNeoBoot(), getBoxHostName())):     
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')
                                        cmd1 = 'ln -sfn /sbin/neoinitarm /sbin/init; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_kernel.sh '                    

                                elif fileExists('/.multinfo'):    
                                    if not fileExists('%sImageBoot/%s/boot/zImage.%s' % ( getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')                                                                                                                                                                                                                                                                                                                                                                 
                                        cmd1 = 'python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/findkerneldevice.py; dd if=%sImagesUpload/.kernel/flash-kernel-%s.bin of=/dev/kernel; cd /media/mmc;ln -sf "neoinitarm" "/media/mmc/sbin/init"; reboot -f' % getNeoLocation() %  getBoxHostName()

                                    elif fileExists('%sImageBoot/%s/boot/zImage.%s' % ( getNeoLocation(), getImageNeoBoot(), getBoxHostName())):
                                        cmd = "echo -e '\n\n%s '" % _('NEOBOOT - Restart image flash....\nPlease wait, in a moment the decoder will be restarted...')
                                        cmd1 = 'cd /media/mmc; ln -sf "neoinitarm" "/media/mmc/sbin/init"; /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/target/h7s_kernel.sh '                                                                                       

                            self.session.open(Console, _('NeoBoot ARM....'), [cmd, cmd1])
                            self.close()   

            else:
                            os.system('echo "Flash "  >> ' + getNeoLocation() + 'ImageBoot/.neonextboot')
                            self.messagebox = self.session.open(MessageBox, _('Wygląda na to że multiboot nie wspiera tego modelu STB !!! '), MessageBox.TYPE_INFO, 8)
                            self.close()

    def myclose2(self, message):
        self.session.open(MessageBox, message, MessageBox.TYPE_INFO)
        self.close()
