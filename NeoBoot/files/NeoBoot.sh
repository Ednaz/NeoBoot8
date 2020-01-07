#!/bin/sh
IMAGE=ImageBoot
NEOBOOTMOUNT=$( cat /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot/.location) 

if [ -f $NEOBOOTMOUNT/NeoBoot_Backup.tar.gz  ] ; then
        rm -R $NEOBOOTMOUNT/NeoBoot_Backupt.tar.gz         
        /bin/tar -czf $NEOBOOTMOUNT/NeoBoot_Backup.tar.gz /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot*/
        echo " "
        echo "Kopia o nazwie NeoBoot_Backup.tar.gz zostala utworzona w lokalizacji:"    $NEOBOOTMOUNT" . " 
        echo " "
else
        /bin/tar -czf $NEOBOOTMOUNT/NeoBoot_Backup.tar.gz /usr/lib/enigma2/python/Plugins/Extensions/NeoBoot*/
        echo " "
        echo "Kopia o nazwie NeoBoot_Backup.tar.gz zostala utworzona w lokalizacji:"    $NEOBOOTMOUNT" . " 
        echo " "
fi      

exit 0
  
