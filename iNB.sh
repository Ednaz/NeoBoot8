#!/bin/sh
#
#skrypt instaluje neoboot-a
#
if `grep -q 'osd.language=pl_PL' </etc/enigma2/settings`; then
  PL=1
fi
[ -e /tmp/neoboot.zip ] && rm -f /tmp/neoboot.zip
[ -e /tmp/neoboot-master ] && rm -rf /tmp/neoboot-master
[ $PL ] && echo "Pobieranie archiwum..." || echo "Downloading archive file..."
URL='https://github.com/gutosie/NeoBoot8/archive/master.zip'
curl -kLs $URL  -o /tmp/neoboot.zip
cd /tmp/
if [ ! -e /tmp/master.zip ]; then 
   wget $URL  
   mv -f /tmp/master.zip /tmp/neoboot.zip  
fi
unzip -qn ./neoboot.zip
rm -f /tmp/neoboot.zip
#kopiowanie
[ $PL ] && echo "Instalowanie..." || echo "Instaling..."
Cel="/usr/lib/enigma2/python/Plugins/Extensions"
[ -e $Cel/NeoBoot ] && rm -rf $Cel/NeoBoot/* || mkdir -p $Cel/NeoBoot
mv -f /tmp/NeoBoot8-master/NeoBoot/* $Cel/NeoBoot
[ -e /tmp/NeoBoot8-master ] && rm -rf /tmp/NeoBoot8-master
cd $Cel/NeoBoot
chmod 755 ./bin/*
chmod 755 ./ex_init.py
chmod 755 ./files/*.sh
chmod 755 ./files/neo_location
chmod -R +x ./ubi_reader/*
if [ $PL ] ; then
  echo ""
  echo "#####################################################"
  echo "#          NEOBOOT ZOSTAL ZAINSTALOWANY             #"
  echo "#####################################################"
  echo "#                ZRESTARTUJ TUNER                   #"
  echo "#####################################################"
  echo ""
else
  echo ""
  echo "#####################################################"
  echo "#          NEOBOOT  INSTALLED SUCCESSFULLY           #"
  echo "#####################################################"
  echo "#             PLEASE RESTART YOUR STB               #"
  echo "#####################################################"
  echo ""
fi
exit 0
  echo "#####################################################"
  echo "#          NEOBOOT INSTALLED SUCCESSFULLY           #"
  echo "#####################################################"
  echo "#             PLEASE RESTART YOUR STB               #"
  echo "#####################################################"
  echo ""
fi
exit 0
