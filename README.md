E2iPlayer m4sport HU host

Install:

~~~
wget --no-check-certificate https://github.com/e2iplayerhosts/m4sport/archive/master.zip -q -O /tmp/m4sport.zip
unzip -q -o /tmp/m4sport.zip -d /tmp
cp -r -f /tmp/m4sport-master/IPTVPlayer/* /usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer
rm -r -f /tmp/m4sport*
~~~

restart enigma2 GUI
