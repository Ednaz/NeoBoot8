#!/bin/sh
#script - gutosie 
if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi

if [ -f /proc/stb/info/vumodel ];  then  
    VUMODEL=$( cat /proc/stb/info/vumodel )     
fi 

if [ -f /proc/stb/info/boxtype ];  then  
    BOXTYPE=$( cat /proc/stb/info/boxtype )    
fi

if [ -f /proc/stb/info/chipset ];  then  
    CHIPSET=$( cat /proc/stb/info/chipset )    
fi

if [ -f /tmp/zImage ];  then  
    rm -f /tmp/zImage    
fi

KERNEL=`uname -r` 
IMAGE=ImageBoot
IMAGENEXTBOOT=/ImageBoot/.neonextboot
NEOBOOTMOUNT=$( cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location) 
BOXNAME=$( cat /etc/hostname) 
UPLOAD=ImagesUpload

if [ -f $NEOBOOTMOUNT$IMAGENEXTBOOT ]; then
  TARGET=`cat $NEOBOOTMOUNT$IMAGENEXTBOOT`
else
  TARGET=Flash              
fi

echo "NEOBOOT is booting image from " $TARGET

if [ $BOXNAME = "vuultimo4k" ] || [ $BOXNAME = "vusolo4k" ] || [ $BOXNAME = "vuuno4kse" ] || [ $BOXNAME = "vuuno4k" ]; then                    
    if [ $TARGET = "Flash" ]; then                                                              
                INFOBOOT=$( cat /.multinfo )
                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image " $TARGET
                elif [ -e /.multinfo ]; then
                                [ $PL ] && echo "Instalacja pliku kernel bin /dev/mmcblk0p1......" || echo "Instaling kernel bin file /dev/mmcblk0p1... "                                                                                                              
                                cd /media/mmc; ln -sfn /sbin/init.sysvinit /media/mmc/sbin/init
                                if [ -e $NEOBOOTMOUNT$UPLOAD/.kernel/flash-kernel-$BOXNAME.bin ] ; then                                                                                                                                                                                                                       
                                    if [ -d /proc/stb ] ; then
                      	    	            dd if=$NEOBOOTMOUNT$UPLOAD/.kernel/flash-kernel-$BOXNAME.bin of=/dev/mmcblk0p1
                                    fi
                                    echo "Boot - Flash. "                                                                                                                                                                                        
                                    echo "Start image Flash z dysku hdd lub usb za 5 sekund _RESTART_..." 
                                fi                                                                                                                              
                elif [ ! -e /.multinfo ]; then 
                                    [ $PL ] && echo "Instalacja pliku kernel bin /dev/mmcblk0p1......" || echo "Instaling kernel bin file /dev/mmcblk0p1... "                                   
                                    if [ -e $NEOBOOTMOUNT$UPLOAD/.kernel/flash-kernel-$BOXNAME.bin ] ; then
                                        [ $PL ] && echo "Instalacja pliku kernel bin..." || echo "Instaling kernel bin file "                                                                                                                  
                                        if [ -d /proc/stb ] ; then
                                                    dd if=$NEOBOOTMOUNT$UPLOAD/.kernel/flash-kernel-$BOXNAME.bin conv=noerror conv=sync of=/dev/mmcblk0p1
                                        fi                                                                                                                                              
                                        echo "Start-restart Flash image..."                                                                                 
                                        echo "Reboot image Flash za 5 sekund =RESTART=...; " 
                                    fi                                                                                                     
                fi                
                update-alternatives --remove vmlinux vmlinux-`uname -r` || true
                [ $PL ] && echo " Zainstalowano kernel image  " $TARGET  " "  || echo " Installed kernel image - "$TARGET" "
                cat /dev/mmcblk0p1 | grep "kernel"                             
                echo "Used Kernel: " $TARGET > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel
                echo "CHIPSET: " $CHIPSET " BOXNAME: "$BOXNAME" MODEL: "$VUMODEL" "
                echo "...............shutdown now..............."; sleep 5; reboot -d -f -h -i
    else              	    
        if [ $TARGET != "Flash" ]; then                                             
                        if [ -e /.multinfo ] ; then
                                INFOBOOT=$( cat /.multinfo )
                                if [ $TARGET = $INFOBOOT ] ; then
                                    echo "NEOBOOT is booting image " $TARGET
                                else
                                    [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."                                     
                                    sleep 2
                                    cp -fR $NEOBOOTMOUNT$IMAGE/$TARGET/boot/zImage.$BOXNAME /tmp/zImage
                                    echo "Instalacja kernel do /dev/mmcblk0p1..."
                                    sleep 2                                   
                                    if [ -d /proc/stb ] ; then
                                                    dd if=/tmp/zImage of=/dev/mmcblk0p1
                                    fi                                                                                                                                               
                                    echo "Start image z Flash..."
                                    echo "Kernels for image " $TARGET " changed..."                                                                        
                                    echo "Start innego image z Flash za 5 sekund *RESTART*..."
                                fi
                        else
                                    [ $PL ] && echo "Przenoszenie pliku kernel do /tmp..." || echo "Moving the kernel file to..."                                
                                    sleep 2
                                    cp -fR $NEOBOOTMOUNT$IMAGE/$TARGET/boot/zImage.$BOXNAME /tmp/zImage
                                    echo "Instalacja kernel bin do /dev/mmcblk0p1..."
                                    sleep 2 
                                    if [ -d /proc/stb ] ; then
                                            dd if=/tmp/zImage of=/dev/mmcblk0p1
                                    fi                                                                         
                                    echo "Kernel dla potrzeb startu systemu " $TARGET " VU+ zmieniony."                                                                                                                                                      
                                    echo "Start innego image z Flash za 5 sekund -RESTART-..."
                        fi                         
                        rm -f /tmp/zImage
                        cat /dev/mmcblk0p1 | grep "kernel"
                        update-alternatives --remove vmlinux vmlinux-`uname -r` || true                        
                        echo "Used Kernel: " $TARGET  > $NEOBOOTMOUNT$UPLOAD/.kernel/used_flash_kernel 
                        echo "CHIPSET: " $CHIPSET " BOXNAME: "$BOXNAME" MODEL: "$VUMODEL" "
                        echo "...............Shutdown Now..............."; sleep 5; reboot -d -f -h -i 
        fi
    fi                               
else
                    ln -sfn /sbin/init.sysvinit /sbin/init
                    echo "CHIPSET: " $CHIPSET " BOXNAME: "$BOXNAME" MODEL: "$VUMODEL" "
                    echo "$TARGET "  > $NEOBOOTMOUNT/ImageBoot/.neonextboot
                    echo "Error - Nie wpierany model STB !!! "
                    exit 0
fi
exit 0