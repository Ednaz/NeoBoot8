#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver. gutosie
import time, sys, os, struct, shutil 

def getFSTAB2():
    install='UNKNOWN'
    if os.path.exists('/etc/fstab'):
        with open('/etc/fstab', 'r') as f:
            lines = f.read()
            f.close()
        if lines.find('UUID') != -1:
            install='OKinstall'
        elif not lines.find('UUID') != -1:
            install='NOinstall'
    return install 

def getBoxHostName():
    if os.path.exists('/etc/hostname'):
        with open('/etc/hostname', 'r') as f:
            myboxname = f.readline().strip()
            f.close()   
    return myboxname 

def getCPUSoC():
    chipset='UNKNOWN'
    if os.path.exists('/proc/stb/info/chipset'):
        with open('/proc/stb/info/chipset', 'r') as f:
            chipset = f.readline().strip()
            f.close()     
        if chipset == '7405(with 3D)':
            chipset == '7405'
                                            
    return chipset
      
def getBoxVuModel():
    vumodel='UNKNOWN'
    if os.path.exists("/proc/stb/info/vumodel") and not os.path.exists("/proc/stb/info/boxtype"):
        with open('/proc/stb/info/vumodel', 'r') as f:
            vumodel = f.readline().strip()
            f.close() 
    return vumodel

def getCPUtype() :
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
    
def getKernelVersion():
    try:
        return open('/proc/version', 'r').read().split(' ', 4)[2].split('-', 2)[0]
    except:
        return _('unknown')
             
def getNeoLocation():
    locatino='UNKNOWN'
    if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location'):
        with open('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location', 'r') as f:
            locatino = f.readline().strip()
            f.close()     
    return locatino

media = getNeoLocation()
mediahome = media + '/ImageBoot/'
extensions_path = '/usr/lib/enigma2/python/Plugins/Extensions/'
dev_null = ' > /dev/null 2>&1'

def NEOBootMainEx(source, target, stopenigma, CopyFiles, CopyKernel, TvList, Montowanie, LanWlan, Sterowniki, InstallSettings, ZipDelete, RepairFTP, SoftCam, MediaPortal, BlackHole):
    media_target = mediahome + target
    list_one = ['rm -r ' + media_target + dev_null, 'mkdir ' + media_target + dev_null, 'chmod -R 0777 ' + media_target]
    for command in list_one:
        os.system(command)

    if stopenigma == 'True':
        os.system('echo "All system processes have been stopped,\n please wait, after the installation is completed, E2 will restart..."')
        os.system('touch /tmp/init4; init 4')

    rc = NEOBootExtract(source, target, ZipDelete, BlackHole)    
    if not os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions' % (media, target)):
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins' % (media, target))
        os.system('mkdir -p %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions' % (media, target))
                
    list_two = ['mkdir -p ' + media_target + '/media' + dev_null,
     'rm ' + media_target + media + dev_null,
     'rmdir ' + media_target + media + dev_null,
     'mkdir -p ' + media_target + media + dev_null,
     'cp /etc/passwd ' + media_target + '/etc/passwd' + dev_null,
     'cp /etc/hostname ' + media_target + '/etc/hostname' + dev_null,       
     #'cp -rf /etc/init.d/vuplus-platform-util ' + media_target + '/etc/init.d/vuplus-platform-util' + dev_null,       
     'cp -rf ' + extensions_path + 'NeoBoot ' + media_target + extensions_path + 'NeoBoot' + dev_null]
    for command in list_two:
        os.system(command)

    if CopyFiles == 'False':
        os.system('echo "No copying of files..."')
        os.system('touch  ' + getNeoLocation() + 'ImageBoot/.without_copying; sleep 5')              

    if CopyKernel == 'True':        
            #mips
            if getBoxHostName() == 'vuultimo' or getCPUSoC() == '7405' and os.path.exists('%s/ImageBoot/%s/etc/vtiversion.info' % (media, target)):
                if os.path.exists('%s/ImageBoot/%s/lib/modules' % (media, target)):
                    cmd = 'rm -r %s/ImageBoot/%s/lib/modules' % (media, target)
                    rc = os.system(cmd)
                cmd = 'mkdir -p %s/ImageBoot/%s/lib/modules > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -r /lib/modules  %s/ImageBoot/%s/lib  > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                if os.path.exists('%s/ImageBoot/%s/lib/firmware' % (media, target)):
                    cmd = 'rm -r %s/ImageBoot/%s/lib/firmware' % (media, target)
                    rc = os.system(cmd)
                cmd = 'mkdir -p %s/ImageBoot/%s/lib/firmware > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -r /lib/firmware %s/ImageBoot/%s/lib > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                os.system('echo "Skopiowano sterowniki systemu. Nie skopiowano kernel.bin dla Ultimo HD - NIE ZALECANE DLA TEGO MODELU."')
                          
            elif getBoxHostName() == 'vuultimo' or getCPUSoC() == '7335' or getCPUSoC() == '7325' or getCPUSoC() == '7405' or getCPUSoC() == '7356' or getCPUSoC() == '7424' or getCPUSoC() == '7241' or getCPUSoC() == '7362':
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/vuplus/' + getBoxVuModel() + '/kernel_cfe_auto.bin ' + media_target + '/boot/' + getBoxHostName() + '.vmlinux.gz' + dev_null)        
                os.system('echo "Skopiowano kernel.bin STB-MIPS"')

#Ultra
            elif getBoxHostName() == 'mbultra' or getCPUSoC() == 'bcm7424':
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra/kernel.bin ' + media_target + '/boot/' + getBoxHostName() + '.vmlinux.gz' + dev_null)        
                os.system('echo "Skopiowano kernel.bin MiracleBoxUltra. Typ stb - MIPS"')

#Edision OS MINI 
            elif getBoxHostName() == 'osmini' or getCPUSoC() == 'BCM7362':
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/osmini/kernel.bin ' + media_target + '/boot/' + getBoxHostName() + '.vmlinux.gz' + dev_null)        
                os.system('echo "Skopiowano kernel.bin Edision OS MINI. Typ stb - MIPS"')
#arm octagon
            elif getBoxHostName() == 'sf4008':  #getCPUSoC() == 'bcm7251' or
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/' + getBoxHostName() + '/kernel.bin ' + media_target + '/boot/zImage.' + getBoxHostName() + '' + dev_null)
                os.system('echo "Skopiowano kernel.bin STB-ARM Octagon."')   

#arm Galaxy Innvations ET-11000 4K et1x000
            elif getBoxHostName() == 'et1x000': #getCPUSoC() == 'bcm7251' or
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/' + getBoxHostName() + '/kernel.bin ' + media_target + '/boot/zImage.' + getBoxHostName() + '' + dev_null)
                os.system('echo "Skopiowano kernel.bin STB-ARM GI ET-11000 4K."')

#arm  Ariva 4K Combo
            elif getBoxHostName() == 'et1x000': #getCPUSoC() == 'bcm7251' or
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/e2/update/kernel.bin ' + media_target + '/boot/zImage.' + getBoxHostName() + '' + dev_null)
                os.system('echo "Skopiowano kernel.bin STB-ARM Ariva 4K Combo."')

#arm Zgemma h7
            elif getCPUSoC() == 'bcm7251s' or getBoxHostName() == 'h7':
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/zgemma/' + getBoxHostName() + '/kernel.bin ' + media_target + '/boot/zImage.' + getBoxHostName() + '' + dev_null)
                os.system('echo "Skopiowano kernel.bin STB-ARM Zgemma h7."')   
#arm gbquad4k
            elif getCPUSoC() == 'bcm7252s' or getBoxHostName() == 'gbquad4k':
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/gigablue/quad4k' + getBoxHostName() + '/kernel.bin ' + media_target + '/boot/zImage.' + getBoxHostName() + '' + dev_null)
                os.system('echo "Skopiowano kernel.bin STB-ARM gbquad4k."')                 
                         
#arm vuplus
            elif getCPUSoC() == '7444s' or getCPUSoC() == '7278' or getCPUSoC() == '7376' or getCPUSoC() == '7252s' or getCPUSoC() == '72604':
                os.system('mv ' + getNeoLocation() + 'ImagesUpload/vuplus/' + getBoxVuModel() + '/kernel_auto.bin ' + media_target + '/boot/zImage.' + getBoxHostName() + '' + dev_null)
                os.system('echo "Skopiowano kernel.bin STB-ARM"')   
                                            
    if not os.path.exists('' + getNeoLocation() + 'ImageBoot/.without_copying'):           
        if os.path.exists('/usr/sbin/nandwrite'):
            cmd = 'cp -r /usr/sbin/nandwrite %s/ImageBoot/%s/usr/sbin/nandwrite > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/bin/fullwget'):
            cmd = 'cp -r /usr/bin/fullwget %s/ImageBoot/%s/usr/bin/fullwget > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/etc/init.d/inadyn-mt'):
            cmd = 'cp -r /etc/init.d/inadyn-mt %s/ImageBoot/%s/etc/init.d/inadyn-mt > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/bin/inadyn-mt'):
            cmd = 'cp -r /usr/bin/inadyn-mt %s/ImageBoot/%s/usr/bin/inadyn-mt > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/etc/inadyn.conf'):
            cmd = 'cp -r /etc/inadyn.conf %s/ImageBoot/%s/etc/inadyn.conf > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/SystemPlugins/FanControl'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/SystemPlugins/FanControl %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/SystemPlugins > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/EmuManager'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/EmuManager %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/CamdMenager'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/CamdMenager %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /usr/lib/python*.*/htmlentitydefs.pyo %s/ImageBoot/%s/usr/lib/python*.* > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/FeedExtra'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/FeedExtra %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/MyUpdater'):
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/MyUpdater %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        if not os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/boxbranding.so' % (media, target)):
            cmd = 'cp -r /usr/lib/enigma2/python/boxbranding.so %s/ImageBoot/%s/usr/lib/enigma2/python/boxbranding.so > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
        os.system('echo "Skopiowano wtyczki."')        
        
        if TvList == 'True':
            if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                cmd = 'mkdir -p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.tv %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.radio %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/*.tv %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/lamedb %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            os.system('echo "Skopiowano list\xc4\x99 tv."')

        if Montowanie == 'True':
            if os.path.exists('%s/ImageBoot/%s/etc/fstab' % (media, target)):
                cmd = 'mv %s/ImageBoot/%s/etc/fstab %s/ImageBoot/%s/etc/fstab.org' % (media,
                 target,
                 media,
                 target)
                rc = os.system(cmd)
            if os.path.exists('%s/ImageBoot/%s/etc/init.d/volatile-media.sh' % (media, target)):
                cmd = 'mv %s/ImageBoot/%s/etc/init.d/volatile-media.sh %s/ImageBoot/%s/etc/init.d/volatile-media.sh.org' % (media,
                 target,
                 media,
                 target)
                rc = os.system(cmd)
            cmd = 'cp -r /etc/fstab %s/ImageBoot/%s/etc/fstab' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/S50fat.sh %s/ImageBoot/%s/etc/rcS.d' % (media, target)
            rc = os.system(cmd)

###########################################################

            if os.path.exists('%s/ImageBoot/%s/etc/init.d/udev' % (media, target)):
                filename = '%s/ImageBoot/%s/etc/init.d/udev' % (media, target)
                if os.path.exists(filename):
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('exit 0') != -1:
                            line = '\n'
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)

                    cmd = 'echo "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom" >> %s/ImageBoot/%s/etc/init.d/udev' % (media, target)
                    rc = os.system(cmd)
                    cmd = 'echo "exit 0" >> %s/ImageBoot/%s/etc/init.d/udev' % (media, target)
                    rc = os.system(cmd)

            if os.path.exists('%s/ImageBoot/%s/etc/init.d/mdev'% (media, target)):                    
                    cmd = 'echo " " >> %s/ImageBoot/%s/etc/init.d/mdev' % (media, target)
                    rc = os.system(cmd)
                    cmd = 'echo "/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/files/neom" >> %s/ImageBoot/%s/etc/init.d/mdev' % (media, target)
                    rc = os.system(cmd)

        if LanWlan == 'True':
            if os.path.exists('%s/ImageBoot/%s/etc/vtiversion.info' % (media, target)):
                os.system('echo "Nie skopiowano LAN-WLAN, nie zalecane dla tego image."')
            elif os.path.exists('/etc/vtiversion.info') and os.path.exists('%s/usr/lib/enigma2/python/Plugins/PLi' % (media, target)):
                os.system('echo "Nie skopiowano LAN-WLAN, nie zalecane dla tego image."')
            elif os.path.exists('/etc/bhversion') and os.path.exists('%s/usr/lib/enigma2/python/Plugins/PLi' % (media, target)):
                os.system('echo "Nie skopiowano LAN-WLAN, nie zalecane dla tego image."')
            else:                
                if os.path.exists('/etc/wpa_supplicant.wlan0.conf'):
                    cmd = 'cp -Rpf /etc/wpa_supplicant.wlan0.conf %s/ImageBoot/%s/etc/wpa_supplicant.wlan0.conf > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/network/interfaces'):
                    cmd = 'cp -r /etc/network/interfaces %s/ImageBoot/%s/etc/network/interfaces > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/wpa_supplicant.conf'):
                    cmd = 'cp -Rpf /etc/wpa_supplicant.conf %s/ImageBoot/%s/etc/wpa_supplicant.conf > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/resolv.conf'):
                    cmd = 'cp -Rpf /etc/resolv.conf %s/ImageBoot/%s/etc/resolv.conf > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)
                if os.path.exists('/etc/wl.conf.wlan3'):
                    cmd = 'cp -r /etc/wl.conf.wlan3 %s/ImageBoot/%s/etc/wl.conf.wlan3 > /dev/null 2>&1' % (media, target)
                    rc = os.system(cmd)

        if Sterowniki == 'True':
            if os.path.exists('%s/ImageBoot/%s/lib/modules' % (media, target)):
                cmd = 'rm -r %s/ImageBoot/%s/lib/modules' % (media, target)
                rc = os.system(cmd)
            cmd = 'mkdir -p %s/ImageBoot/%s/lib/modules > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp -r /lib/modules  %s/ImageBoot/%s/lib  > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            if os.path.exists('%s/ImageBoot/%s/lib/firmware' % (media, target)):
                cmd = 'rm -r %s/ImageBoot/%s/lib/firmware' % (media, target)
                rc = os.system(cmd)
            cmd = 'mkdir -p %s/ImageBoot/%s/lib/firmware > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            cmd = 'cp -r /lib/firmware %s/ImageBoot/%s/lib > /dev/null 2>&1' % (media, target)
            rc = os.system(cmd)
            os.system('echo "Skopiowano sterowniki systemu."')

        if InstallSettings == 'True':
            if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                cmd = 'mkdir -p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp /etc/enigma2/settings %s/ImageBoot/%s/etc/enigma2' % (media, target)
            rc = os.system(cmd)
            if not os.path.exists('%s/ImageBoot/%s/etc/tuxbox/config' % (media, target)):
                cmd = 'mkdir -p /etc/tuxbox/config %s/ImageBoot/%s/etc/tuxbox/config' % (media, target)
                rc = os.system(cmd)
                cmd = 'mkdir -p /etc/tuxbox/scce %s/ImageBoot/%s/etc/tuxbox/scce' % (media, target)
                rc = os.system(cmd)
            cmd = 'cp -a /etc/tuxbox/* %s/ImageBoot/%s/etc/tuxbox' % (media, target)
            rc = os.system(cmd)
            os.system('echo "Skopiowano ustawienia systemu."')

        if RepairFTP == 'True':
            if os.path.exists('%s/ImageBoot/%s/etc/vsftpd.conf' % (media, target)):
                filename = media + '/ImageBoot/' + target + '/etc/vsftpd.conf'
                if os.path.exists(filename):
                    filename2 = filename + '.tmp'
                    out = open(filename2, 'w')
                    f = open(filename, 'r')
                    for line in f.readlines():
                        if line.find('listen=NO') != -1:
                            line = 'listen=YES\n'
                        elif line.find('listen_ipv6=YES') != -1:
                            line = 'listen_ipv6=NO\n'
                        out.write(line)

                    f.close()
                    out.close()
                    os.rename(filename2, filename)
            os.system('echo "Naprawa ftp."')

        if SoftCam == 'True':
            if os.path.exists('/etc/CCcam.cfg'):
                cmd = 'cp -r -f /etc/CCcam.cfg %s/ImageBoot/%s/etc > /dev/null 2>&1' % (media, target)    
                rc = os.system(cmd)
            if os.path.exists('/etc/tuxbox/config'):
                cmd = 'cp -r -f /etc/tuxbox/config %s/ImageBoot/%s/etc/tuxbox > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)       
            if os.path.exists('/etc/init.d/softcam.oscam'):
                cmd = 'cp -r -f -p /etc/init.d/softcam.osca* %s/ImageBoot/%s/etc/init.d > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 
            if os.path.exists('/etc/init.d/softcam.None'):
                cmd = 'cp -r -f -p /etc/init.d/softcam.None %s/ImageBoot/%s/etc/init.d > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 
            if os.path.exists('/etc/init.d/softcam.CCcam'):
                cmd = 'cp -r -f -p /etc/init.d/softcam.softcam.CCcam %s/ImageBoot/%s/etc/init.d > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 
       
        if MediaPortal == 'True':
            if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal'):
                cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/MediaPortal %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)            
                cmd = 'cp -r /usr/lib/enigma2/python/Plugins/Extensions/mpgz %s/ImageBoot/%s/usr/lib/enigma2/python/Plugins/Extensions > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 
                cmd = 'cp -r /usr/lib/python2.7/argparse.pyo %s/ImageBoot/%s/usr/lib/python2.7 > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd) 
                cmd = 'cp -r /usr/lib/python2.7/robotparser.pyo %s/ImageBoot/%s/usr/lib/python2.7 > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)             
                cmd = 'cp -r /usr/lib/python2.7/site-packages/Crypto %s/ImageBoot/%s/usr/lib/python2.7/site-packages > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -r /usr/lib/python2.7/site-packages/mechanize %s/ImageBoot/%s/usr/lib/python2.7/site-packages > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -r /usr/lib/python2.7/site-packages/requests %s/ImageBoot/%s/usr/lib/python2.7/site-packages > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp -r /usr/lib/python2.7/site-packages/requests-2.11.1-py2.7.egg-info %s/ImageBoot/%s/usr/lib/python2.7/site-packages > /dev/null 2>&1' % (media, target)
                rc = os.system(cmd)                                    

                if not os.path.exists('%s/ImageBoot/%s/etc/enigma2' % (media, target)):
                    cmd = 'mkdir -p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                    rc = os.system(cmd)
                cmd = 'cp /etc/enigma2/mp_2s4p %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp /etc/enigma2/mp_config %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)
                cmd = 'cp /etc/enigma2/mp_pluginliste %s/ImageBoot/%s/etc/enigma2' % (media, target)
                rc = os.system(cmd)                                
                os.system('echo "Skopiowano MediaPortal z ustawieniami systemowymi."')
            elif not os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/MediaPortal'):                    
                os.system('echo "MediaPortal not found."')

    if not os.path.exists('' + getNeoLocation() + 'ImageBoot/.without_copying'):
    #if os.path.exists('' + getNeoLocation() + 'ImageBoot'):



#        if getFSTAB2() == 'OKinstall':
                                                  
               # os.system(' echo ' + fstablines + '   >> %s/ImageBoot/%s/etc/fstab' % (media, target))
         
        namefile = media + '/ImageBoot/' + target + '/etc/fstab'
        namefile2 = namefile + '.tmp'
        if os.path.exists(namefile2):
            out = open(namefile2, 'w')
            f = open(namefile, 'r')
            for line in f.readlines():

                if line.find('/dev/mmcblk0p1') != -1:
                    line = '#' + line
                elif line.find('/dev/mmcblk0p2') != -1:
                    line = '#' + line
                elif line.find('/dev/mmcblk0p3') != -1:
                    line = '#' + line
                elif line.find('/dev/mmcblk0p4') != -1:
                    line = '#' + line
                elif line.find('/dev/mmcblk0p5') != -1:
                    line = '#' + line                
                elif line.find('/dev/mmcblk0p6') != -1:
                    line = '#' + line 
                elif line.find('/dev/mmcblk0p7') != -1:
                    line = '#' + line 
                elif line.find('/dev/mmcblk0p8') != -1:
                    line = '#' + line 
                elif line.find('/dev/mmcblk0p9') != -1:
                    line = '#' + line 
                elif line.find('/dev/root') != -1:
                    line = '#' + line                
                elif line.find('/dev/mtdblock1') != -1:
                    line = '#' + line
                elif line.find('/dev/mtdblock2') != -1:
                    line = '#' + line
                elif line.find('/dev/mtdblock3') != -1:
                    line = '#' + line
                elif line.find('/dev/mtdblock4') != -1:
                    line = '#' + line
                elif line.find('/dev/mtdblock5') != -1:
                    line = '#' + line                
                elif line.find('/dev/mtdblock6') != -1:
                    line = '#' + line 
                elif line.find('/dev/mtdblock7') != -1:
                    line = '#' + line 
                elif line.find('/dev/mtdblock8') != -1:
                    line = '#' + line 
                elif line.find('/dev/mtdblock9') != -1:
                    line = '#' + line 
                elif line.find('/dev/root') != -1:
                    line = '#' + line
                out.write(line)

            f.close()
            out.close()
            os.rename(namefile2, namefile)

        tpmd = media + '/ImageBoot/' + target + '/etc/init.d/tpmd'
        if os.path.exists(tpmd):
                os.system('rm ' + tpmd)

        fname = media + '/ImageBoot/' + target + '/usr/lib/enigma2/python/Components/config.py'
        if os.path.exists(fname):
            fname2 = fname + '.tmp'
            out = open(fname2, 'w')
            f = open(fname, 'r')
            for line in f.readlines():
                if line.find('if file(""/proc/stb/info/vumodel")') != -1:
                    line = '#' + line
                out.write(line)

            f.close()
            out.close()
            os.rename(fname2, fname)


        targetfile = media + '/ImageBoot/' + target + '/etc/vsftpd.conf'
        if os.path.exists(targetfile):
            targetfile2 = targetfile + '.tmp'
            out = open(targetfile2, 'w')
            f = open(targetfile, 'r')
            for line in f.readlines():
                if not line.startswith('nopriv_user'):
                    out.write(line)

            f.close()
            out.close()
            os.rename(targetfile2, targetfile)


        mypath = media + '/ImageBoot/' + target + '/usr/lib/opkg/info/'
        cmd = 'mkdir -p %s/ImageBoot/%s/var/lib/opkg/info > /dev/null 2>&1' % (media, target)
        rc = os.system(cmd)
        if not os.path.exists(mypath):
            mypath = media + '/ImageBoot/' + target + '/var/lib/opkg/info/'
        for fn in os.listdir(mypath):
            if fn.find('kernel-image') != -1 and fn.find('postinst') != -1:
                filename = mypath + fn
                filename2 = filename + '.tmp'
                out = open(filename2, 'w')
                f = open(filename, 'r')
                for line in f.readlines():
                    if line.find('/boot') != -1:
                        line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                    out.write(line)

                if f.close():
                    out.close()
                    os.rename(filename2, filename)
                    cmd = 'chmod -R 0755 %s' % filename
                    rc = os.system(cmd)
            if fn.find('-bootlogo.postinst') != -1:
                filename = mypath + fn
                filename2 = filename + '.tmp'
                out = open(filename2, 'w')
                f = open(filename, 'r')
                for line in f.readlines():
                    if line.find('/boot') != -1:
                        line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                    out.write(line)

                f.close()
                out.close()
                os.rename(filename2, filename)
                cmd = 'chmod -R 0755 %s' % filename
                rc = os.system(cmd)
            if fn.find('-bootlogo.postrm') != -1:
                filename = mypath + fn
                filename2 = filename + '.tmp'
                out = open(filename2, 'w')
                f = open(filename, 'r')
                for line in f.readlines():
                    if line.find('/boot') != -1:
                        line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                    out.write(line)

                f.close()
                out.close()
                os.rename(filename2, filename)
                cmd = 'chmod -R 0755 %s' % filename
                rc = os.system(cmd)
            if fn.find('-bootlogo.preinst') != -1:
                filename = mypath + fn
                filename2 = filename + '.tmp'
                out = open(filename2, 'w')
                f = open(filename, 'r')
                for line in f.readlines():
                    if line.find('/boot') != -1:
                        line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                    out.write(line)

                f.close()
                out.close()
                os.rename(filename2, filename)
                cmd = 'chmod -R 0755 %s' % filename
                rc = os.system(cmd)
            if fn.find('-bootlogo.prerm') != -1:
                filename = mypath + fn
                filename2 = filename + '.tmp'
                out = open(filename2, 'w')
                f = open(filename, 'r')
                for line in f.readlines():
                    if line.find('/boot') != -1:
                        line = line.replace('/boot', '/boot > /dev/null 2>\\&1; exit 0')
                    out.write(line)

                f.close()
                out.close()
                os.rename(filename2, filename)
                cmd = 'chmod -R 0755 %s' % filename
                rc = os.system(cmd)

    os.system('mkdir -p ' + media_target + '/media/hdd' + dev_null)
    os.system('mkdir -p ' + media_target + '/media/usb' + dev_null)
    
    os.system('mkdir -p ' + media_target + '/var/lib/opkg/info/' + dev_null)  
    os.system('touch ' + getNeoLocation() + 'ImageBoot/.data; echo "Data instalacji image" > ' + getNeoLocation() + 'ImageBoot/.data; echo " "; date  > ' + getNeoLocation() + 'ImageBoot/.data')
    os.system('mv -f ' + getNeoLocation() + 'ImageBoot/.data ' + getNeoLocation() + 'ImageBoot/%s/.data' % target)
    cmd = 'touch /tmp/.init_reboot'
    rc = os.system(cmd)
    out = open(mediahome + '.neonextboot', 'w')
    out.write(target)
    out.close()
    os.system('cp ' + getNeoLocation() + 'ImageBoot/.neonextboot ' + getNeoLocation() + 'ImageBoot/%s/.multinfo' % target)
    out = open(mediahome + '.neonextboot', 'w')
    out.write('Flash')
    out.close()                                                                             
    if '.tar.xz' not in source and not os.path.exists('' + getNeoLocation() + '/ImageBoot/%s/etc/issue' %  target):
            os.system('echo ""; echo "Nie zainstalowano systemu ! Powodem b\xc5\x82\xc4\x99du instalacji mo\xc5\xbce by\xc4\x87 \xc5\xbale spakowany plik image w zip lub nie jest to sytem dla Twojego modelu ."')
            os.system('echo "Instalowany system może sieę nie uruchomić poprawnie! Sprawdż poprawność kataogow w instalwoanym image!!!"')
            os.system('rm -r ' + getNeoLocation() + '/ImageBoot/%s' % target )

    if os.path.exists('' + getNeoLocation() + 'ubi'):
        os.system('rm -rf ' + getNeoLocation() + 'ubi')          
    if os.path.exists('' + getNeoLocation() + 'image_cache/'):
        os.system('rm ' + getNeoLocation() + 'image_cache')
    if os.path.exists('' + getNeoLocation() + 'ImageBoot/.without_copying'):
        os.system('rm ' + getNeoLocation() + 'ImageBoot/.without_copying') 

    rc = RemoveUnpackDirs()
    if os.path.exists('/tmp/init4'):
        os.system('rm -f /tmp/init4; init 3')

    os.system('echo "End of installation:"; date +%T')

def RemoveUnpackDirs():
    os.chdir(media + '/ImagesUpload')
    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/vuplus')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf4008'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/sf4008')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmio4k'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osmio4k')        
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm900'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/dm900')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd51'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/hd51')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/gigablue')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/miraclebox')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/e4hd'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/e4hd')                
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/update')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/*.nfi'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/*.nfi')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/zgemma')                                                                                               
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/uclan') 
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler1'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/formuler1')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler3'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/formuler3')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler4turbo'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/formuler4turbo')                        
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et*'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/et*')                
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedl*'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/xpeedl*')
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmini'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/osmini')  
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/xp1000 '):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/xp1000 ') 
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dinobot '):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/dinobot ') 
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/e2/update'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/e2')                                                                                          
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et1x000'):
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/et1x000') 
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/octagon/sf8008'):          
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/usb_update.bin ' + getNeoLocation() + 'ImagesUpload/octagon; rm -r ' + getNeoLocation() + 'ImagesUpload/octagon')                                          
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd60'):          
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/hd60; mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/hd60; rm -r ' + getNeoLocation() + 'ImagesUpload/hd60')                                          
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h7'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/h7; mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/h7')                                                                                                
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/h7')  
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/bootargs.bin ' + getNeoLocation() + 'ImagesUpload/h9; mv ' + getNeoLocation() + 'ImagesUpload/fastboot.bin ' + getNeoLocation() + 'ImagesUpload/h9')                                                                                                
        rc = os.system('rm -r ' + getNeoLocation() + 'ImagesUpload/h9')                      
    elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/uclan'):
        rc = os.system('mv ' + getNeoLocation() + 'ImagesUpload/usb_update.bin ' + getNeoLocation() + 'ImagesUpload/uclan') 


def NEOBootExtract(source, target, ZipDelete, BlackHole):
    RemoveUnpackDirs()
    os.system('echo "Installation started:"; date +%T;echo "Extracting the installation file..."')

    if os.path.exists('' + getNeoLocation() + 'ImageBoot/.without_copying'):
        os.system('rm ' + getNeoLocation() + 'ImageBoot/.without_copying') 
    if os.path.exists('' + getNeoLocation() + 'image_cache'):
        os.system('rm -rf ' + getNeoLocation() + 'image_cache')

    sourcefile = media + '/ImagesUpload/%s.zip' % source
    sourcefile2 = media + '/ImagesUpload/%s.nfi' % source
    
    #Instalacja *.nfi
    if os.path.exists(sourcefile2) is True:
        if sourcefile2.endswith('.nfi'):
            os.system('echo "Instalacja systemu skapowanego w plik nfi..."')
            to = '' + getNeoLocation() + 'ImageBoot/' + target
            cmd = 'mkdir %s > /dev/null 2<&1' % to
            rc = os.system(cmd)
            to = '' + getNeoLocation() + 'ImageBoot/' + target
            cmd = 'chmod -R 0777 %s' % to
            rc = os.system(cmd)
            cmd = '/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/nfidump ' + sourcefile2 + ' ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            if ZipDelete == 'True':
                rc = os.system('rm -rf ' + sourcefile2)
            else:
                os.system('echo "NeoBoot keep the file:  %s  for reinstallation."' % sourcefile2)
    #Instalacja *.zip
    elif os.path.exists(sourcefile) is True:
        os.system('unzip ' + sourcefile)
        if ZipDelete == 'True':
            os.system('rm -rf ' + sourcefile)

    #Instalacja MIPS
    if getCPUtype() == 'MIPS':                 
        if os.path.exists('' + getNeoLocation() + 'ubi') is False:
            rc = os.system('mkdir ' + getNeoLocation() + 'ubi')
        to = '' + getNeoLocation() + 'ImageBoot/' + target
        cmd = 'mkdir %s > /dev/null 2<&1' % to
        rc = os.system(cmd)
        to = '' + getNeoLocation() + 'ImageBoot/' + target
        cmd = 'chmod -R 0777 %s' % to
        rc = os.system(cmd)
        rootfname = 'rootfs.bin'
        brand = ''
        #NANDSIM
        if os.path.exists('/lib/modules/%s/kernel/drivers/mtd/nand/nandsim.ko' % getKernelVersion()):
            for i in range(0, 20):
                    mtdfile = '/dev/mtd' + str(i)
                    if os.path.exists(mtdfile) is False:
                        break
                
            mtd = str(i)
            os.chdir(media + '/ImagesUpload')
            #zgemma
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma'):
                os.chdir('zgemma')
                brand = 'zgemma'
                rootfname = 'rootfs.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/sh1'):
                    os.chdir('sh1')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/sh2'):
                    os.chdir('sh2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h2'):
                    os.chdir('h2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h3'):
                    os.chdir('h3')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h5'):
                    os.chdir('h5')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h7'):
                    os.chdir('h7')

            #miraclebox
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox'):
                os.chdir('miraclebox')
                brand = 'miraclebox'
                rootfname = 'rootfs.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/mini'):
                    os.chdir('mini')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/miniplus'):
                    os.chdir('miniplus')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/minihybrid'):
                    os.chdir('minihybrid')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/twin'):
                    os.chdir('twin')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra'):
                    os.chdir('ultra')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/micro'):
                    os.chdir('micro')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/twinplus'):
                    os.chdir('twinplus')
            #atemio
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio'):
                    os.chdir('atemio')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/5x00'):
                        os.chdir('5x00')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6000'):
                        os.chdir('6000')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6100'):
                        os.chdir('6100')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6200'):
                        os.chdir('6200')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/8x00'):
                        os.chdir('8x00')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/8x00'):
                        os.chdir('8x00')
            #Xtrend
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et10000'):
                os.chdir('et10000')
                brand = 'et10000'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et9x00'):
                os.chdir('et9x00')
                brand = 'et9x00'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et8500'):
                os.chdir('et8500')
                brand = 'et8500'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et8000'):
                os.chdir('et8000')
                brand = 'et8000'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et7x00'):
                os.chdir('et7x00')
                brand = 'et7x00'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et6x00'):
                os.chdir('et6x00')
                brand = 'et6x00'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et5x00'):
                os.chdir('et5x00')
                brand = 'et5x00'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et4x00'):
                os.chdir('et4x00')
                brand = 'et4x00'
            #formuler
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler1'):
                os.chdir('formuler1')
                brand = 'formuler1'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler2'):
                os.chdir('formuler2')
                brand = 'formuler2'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler3'):
                os.chdir('formuler3')
                brand = 'formuler3'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/formuler4turbo'):
                os.chdir('formuler4turbo')
                brand = 'formuler4turbo'
            #inne
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf3038'):
                os.chdir('sf3038')
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx'):
                os.chdir('xpeedlx')
                brand = 'xpeedlx'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx3'):
                os.chdir('xpeedlx3')
                brand = 'xpeedlx3'
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xp1000'):
                os.chdir('xp1000')
                brand = 'xp1000'
            #VuPlus
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus'):
                os.chdir('vuplus')
                brand = 'vuplus'
                rootfname = 'root_cfe_auto.jffs2'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno'):
                    os.chdir('uno')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo'):
                    os.chdir('duo')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo'):
                    os.chdir('ultimo')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo'):
                    os.chdir('solo')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo2'):
                    os.chdir('duo2')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo2'):
                    os.chdir('solo2')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solose'):
                    os.chdir('solose')
                    rootfname = 'root_cfe_auto.bin'
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/zero'):
                    os.chdir('zero')
                    rootfname = 'root_cfe_auto.bin'
                    
            #osmini
            if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmini'):
                os.chdir('osmini')
                brand = 'osmini'


            #Instalacja image nandsim                                     
            os.system('echo "Instalacja - nandsim w toku..."') 
            rc = os.system('insmod /lib/modules/%s/kernel/drivers/mtd/nand/nandsim.ko cache_file=' + getNeoLocation() + 'image_cache first_id_byte=0x20 second_id_byte=0xaa third_id_byte=0x00 fourth_id_byte=0x15;sleep 5' % getKernelVersion())
            cmd = 'dd if=%s of=/dev/mtdblock%s bs=2048' % (rootfname, mtd)
            rc = os.system(cmd)
            cmd = 'ubiattach /dev/ubi_ctrl -m %s -O 2048' % mtd
            rc = os.system(cmd)
            rc = os.system('mount -t ubifs ubi1_0 ' + getNeoLocation() + 'ubi')
            os.chdir('/home/root')
            cmd = 'cp -r ' + getNeoLocation() + 'ubi/* ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            rc = os.system('umount ' + getNeoLocation() + 'ubi')
            cmd = 'ubidetach -m %s' % mtd
            rc = os.system(cmd)              
            rc = os.system('rmmod nandsim')
            rc = os.system('rm ' + getNeoLocation() + 'image_cache')

            if '.tar.xz' not in source and not os.path.exists('%s/ImageBoot/%s/etc/issue' % (media, target)):
                os.system("echo 3 > /proc/sys/vm/drop_caches")

                os.system('echo ""; echo "Nie zainstalowano systemu ! Powodem b\xc5\x82\xc4\x99du instalacji mo\xc5\xbce by\xc4\x87 kernel-module-nandsim."')
                os.system('echo "By uzyc innego narzedzia do rozpakowania image, ponow instalacje image jeszcze raz po restarcie tunera."')
                os.system('echo "RESTART ZA 15 sekund..."')

                rc = os.system('rm -rf /lib/modules/%s/kernel/drivers/mtd/nand/nandsim.ko ' % getKernelVersion())
                               
                os.system('rm -r %s/ImageBoot/%s' % (media, target))
                os.system('sleep 5; init 4; sleep 5; init 3 ')

        #UBI_READER
        elif os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/ubi_extract_files.py'):
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/venton-hdx'):
                    os.chdir('venton-hdx')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hde'):
                    os.chdir('hde')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hdx'):
                    os.chdir('hdx')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hdp'):
                    os.chdir('hdp')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox'):
                    os.chdir('miraclebox')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/mini'):
                        os.chdir('mini')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/miniplus'):
                        os.chdir('miniplus')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/minihybrid'):
                        os.chdir('minihybrid')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/twin'):
                        os.chdir('twin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra'):
                        os.chdir('ultra')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/micro'):
                        os.chdir('micro')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/microv2'):
                        os.chdir('microv2')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/twinplus'):
                        os.chdir('twinplus')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/mini4k'):
                        os.chdir('mini4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra4k'):
                        os.chdir('ultra4k')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio'):
                    os.chdir('atemio')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/5x00'):
                        os.chdir('5x00')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6000'):
                        os.chdir('6000')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6100'):
                        os.chdir('6100')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/6200'):
                        os.chdir('6200')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/atemio/8x00'):
                        os.chdir('8x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx'):
                    os.chdir('xpeedlx')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xpeedlx3'):
                    os.chdir('xpeedlx3')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/bwidowx'):
                    os.chdir('bwidowx')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/bwidowx2'):
                    os.chdir('bwidowx2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz'):
                    os.chdir('beyonwiz')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz/hdx'):
                        os.chdir('hdx')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz/hdp'):
                        os.chdir('hdp')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/beyonwiz/hde2'):
                        os.chdir('hde2')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus'):
                    os.chdir('vuplus')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo'):
                        os.chdir('duo')
                        os.system('mv root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo'):
                        os.chdir('solo')
                        os.system('mv -f root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solose'):
                        os.chdir('solose')
                        os.system('mv -f root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo'):
                        os.chdir('ultimo')
                        os.system('mv -f root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno'):
                        os.chdir('uno')
                        os.system('mv -f root_cfe_auto.jffs2 rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo2'):
                        os.chdir('solo2')
                        os.system('mv -f root_cfe_auto.bin rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo2'):
                        os.chdir('duo2')
                        os.system('mv -f root_cfe_auto.bin rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/zero'):
                        os.chdir('zero')
                        os.system('mv -f root_cfe_auto.bin rootfs.bin')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo4k'):
                        os.chdir('solo4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno4k'):
                        os.chdir('uno4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo4k'):
                        os.chdir('ultimo4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo4k'):
                        os.chdir('duo4k')                        
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/zero4k'):
                        os.chdir('zero4k')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno4kse'):
                        os.chdir('uno4kse')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et10000'):
                    os.chdir('et10000')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et9x00'):
                    os.chdir('et9x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et8500'):
                    os.chdir('et8500')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et8000'):
                    os.chdir('et8000')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et7x00'):
                    os.chdir('et7x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et6x00'):
                    os.chdir('et6x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et5x00'):
                    os.chdir('et5x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/et4x00'):
                    os.chdir('et4x00')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf8'):
                    os.chdir('sf')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf98'):
                    os.chdir('sf98')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf108'):
                    os.chdir('sf108')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf128'):
                    os.chdir('sf128')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf138'):
                    os.chdir('sf138')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf208'):
                    os.chdir('sf208')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf228'):
                    os.chdir('sf228')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf3038'):
                    os.chdir('sf3038')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf4008'):
                    os.chdir('sf4008')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/octagon/sf8008'):
                    os.chdir('sf8008')                    
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue'):
                    os.chdir('gigablue')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/quad'):
                        os.chdir('quad')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd2400'):
                    os.chdir('hd2400')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd51'):
                    os.chdir('hd51')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma'):
                    os.chdir('zgemma')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h3'):
                        os.chdir('h3')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h5'):
                        os.chdir('h5')
                    if os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h7'):
                        os.chdir('h7')
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm900'):
                    os.chdir('dm900')
                #osmini
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmini'):
                    os.chdir('osmini')
                #xp1000
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/xp1000'):
                    os.chdir('xp1000')

                #Instalacja image ubi_reader  
                os.system('echo "Instalacja - ubi_reader w toku..."')            
                if os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/root_cfe_auto.*'):
                    os.system('mv -f root_cfe_auto.* rootfs.bin') 
                cmd = 'chmod 777 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/ubi_extract_files.py'
                rc = os.system(cmd)
                cmd = 'python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o' + getNeoLocation() + 'ubi'
                rc = os.system(cmd)
                os.chdir('/home/root')
                os.system('mv ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/%s/' % target)                
                cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
                rc = os.system(cmd)

        else:
                os.system('echo "NeoBoot wykrył błąd !!! Prawdopodobnie brak ubi_reader lub nandsim."')
                
#ARM
    elif getCPUtype() == 'ARMv7':
        os.chdir('' + getNeoLocation() + 'ImagesUpload')
        if os.path.exists('' + getNeoLocation() + 'ImagesUpload/h9/rootfs.ubi'):
            os.chdir('h9')
            os.system('mv -f rootfs.ubi rootfs.bin')                    
            os.system('echo "Instalacja - ubi_reader w toku..."')            
            print '[NeoBoot] Extracting UBIFS image and moving extracted image to our target'
            cmd = 'chmod 777 /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/ubi_extract_files.py'
            rc = os.system(cmd)
            cmd = 'python /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/ubi_reader/ubi_extract_files.py rootfs.bin -o ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)
            os.chdir('/home/root')
            cmd = 'cp -r -p ' + getNeoLocation() + 'ubi/rootfs/* ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'chmod -R +x ' + getNeoLocation() + 'ImageBoot/' + target
            rc = os.system(cmd)
            cmd = 'rm -rf ' + getNeoLocation() + 'ubi'
            rc = os.system(cmd)

        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/sf4008'):
            os.system('echo "Please wait. System installation Octagon SF4008."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/sf4008/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/sf4008/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/octagon/sf8008'):
            os.system('echo "Please wait. System installation Octagon SF8008."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/octagon/sf8008/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/octagon/sf8008/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/osmio4k'):
            os.system('echo "Please wait. System installation EDISION osmio4k"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/osmio4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/osmio4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dm900'):
            os.system('echo "Please wait. System installation Dreambox DM900."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dm900/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/dm900/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/%s.tar.xz' % source):
            os.system('echo "Please wait. System installation spakowanego w plik tar.xz w toku..."')
            os.system('cp -r ' + getNeoLocation() + 'ImagesUpload/%s.tar.xz  ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz' % source)
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz; tar -jJxvf ' + getNeoLocation() + 'ImagesUpload/rootfs.tar.xz -C  ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd51/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation AX 4K Box HD51 "')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/hd51/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/hd51/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)         
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/hd60'):
            os.system('echo "Please wait. System installation AX HD60 4K"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/hd60/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/hd60/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/quad4k'):
            os.system('echo "Please wait. System installation GigaBlue quad4k"')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/gigablue/quad4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/gigablue/quad4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/gigablue/ue4k'):
            os.system('echo "Please wait. System installation GigaBlue ue4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/gigablue/ue4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/gigablue/ue4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/solo4k'):
            os.system('echo "Please wait. System installation VuPlus Solo4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/solo4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/vuplus/solo4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno4k'):
            os.system('echo "Please wait. System installation dla modelu VuPlus Uno4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/uno4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/vuplus/uno4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/uno4kse'):
            os.system('echo "Please wait. System installation VuPlus Uno4kse."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/uno4kse/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/vuplus/uno4kse/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/zero4k'):
            os.system('echo "Please wait. System installation VuPlus zero4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/zero4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/vuplus/zero4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo4k'):
            os.system('echo "Please wait. System installation VuPlus Ultimo4K."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/vuplus/ultimo4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/vuplus/duo4k'):
            os.system('echo "Please wait. System installation VuPlus Duo4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/vuplus/duo4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/vuplus/duo4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/revo4k'):
            os.system('echo "Please wait. System installation Revo4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/revo4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/update/revo4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/galaxy4k'):
            os.system('echo "Please wait. System installation Galaxy4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/galaxy4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/update/galaxy4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h7/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma H7."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/zgemma/h7/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/zgemma/h7/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)   
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/zgemma/h9/rootfs.tar.bz2'):
            os.system('echo "Please wait. System installation Zgemma H9S ."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/zgemma/h9/rootfs.tar.bz2; tar -jxf ' + getNeoLocation() + 'ImagesUpload/zgemma/h9/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)                                                                          
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/mini4k'):
            os.system('echo "Please wait. System installation Miraclebox mini4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/miraclebox/mini4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/miraclebox/mini4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra4k'):
            os.system('echo "Please wait. System installation Miraclebox ultra4k."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra4k/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/miraclebox/ultra4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/e4hd'):
            os.system('echo "Please wait. System installation Axas E4HD 4K Ultra w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/e4hd/rootfs.tar.bz2; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/e4hd/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/update/lunix3-4k'):
            os.system('echo "Please wait. System installation Qviart lunix3-4k w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/update/lunix3-4k; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/update/lunix3-4k/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/dinobot/u5'):
            os.system('echo "Please wait. System installation dinobot w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/dinobot/u5; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/dinobot/u5/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/uclan/ustym4kpro'):
            os.system('echo "Please wait. System installation ustym4kpro w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/uclan/ustym4kpro; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/uclan/ustym4kpro/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/et1x000'):
            os.system('echo "Please wait. System installation GI ET-11000 4K w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/et1x000; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/et1x000/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        elif os.path.exists('' + getNeoLocation() + 'ImagesUpload/e2/update'):
            os.system('echo "Please wait. System installation Ferguson Ariva 4K Combo w toku..."')
            cmd = 'chmod 777 ' + getNeoLocation() + 'ImagesUpload/e2/update; tar -jxvf ' + getNeoLocation() + 'ImagesUpload/e2/update/rootfs.tar.bz2 -C ' + getNeoLocation() + 'ImageBoot/' + target + ' > /dev/null 2>&1'
            rc = os.system(cmd)
        else:
            os.system('echo "NeoBoot wykrył dłąd!!! Prawdopodobnie brak pliku instalacyjnego."')


    if BlackHole == 'True':
        if 'BlackHole' in source and os.path.exists('%s/ImageBoot/%s/usr/lib/enigma2/python/Blackhole' % (media, target)):
            ver = source.replace('BlackHole-', '')
            try:
                text = ver.split('-')[0]
            except:
                text = ''  
                      
            cmd = 'mkdir ' + getNeoLocation() + 'ImageBoot/%s/boot/blackhole' % target
            rc = os.system(cmd)
            cmd = 'cp -f /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/version ' + getNeoLocation() + 'ImageBoot/%s/boot/blackhole' % target
            rc = os.system(cmd)
            cmd = 'mv ' + getNeoLocation() + 'ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.pyo ' + getNeoLocation() + 'ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.pyo.org' % (target, target)
            rc = os.system(cmd)
            cmd = 'cp -rf /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/bin/utilsbh ' + getNeoLocation() + 'ImageBoot/%s/usr/lib/enigma2/python/Blackhole/BhUtils.py' % target
            rc = os.system(cmd)
            localfile = '' + getNeoLocation() + 'ImageBoot/%s/boot/blackhole/version' % target
            temp_file = open(localfile, 'w')
            temp_file.write(text)
            temp_file.close()
            cmd = 'mv ' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2 ' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2-or' % (target, target)
            rc = os.system(cmd)
            fail = '' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2-or' % target
            f = open(fail, 'r')
            content = f.read()
            f.close()
            localfile2 = '' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2' % target
            temp_file2 = open(localfile2, 'w')
            temp_file2.write(content.replace('/proc/blackhole/version', '/boot/blackhole/version'))
            temp_file2.close()
            cmd = 'chmod -R 0755 %s' % localfile2
            rc = os.system(cmd)
            cmd = 'rm -r ' + getNeoLocation() + 'ImageBoot/%s/usr/bin/enigma2-or' % target
            rc = os.system(cmd)

    return 0
#END            
