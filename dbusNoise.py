import dbus
import sys

bus=dbus.SessionBus()
noise=bus.get_object('org.mpris.MediaPlayer2.noise','/org/mpris/MediaPlayer2')
properties_manager = dbus.Interface(noise, 'org.freedesktop.DBus.Properties')
infos=properties_manager.Get('org.mpris.MediaPlayer2.Player','Metadata')
album=infos[dbus.String('xesam:album')]
titre=infos[dbus.String('xesam:title')]
artiste=infos[dbus.String('xesam:artist')][0]

if sys.argv[1]=='artiste':
    print(artiste)
elif sys.argv[1]=='titre':
    print(titre)
elif sys.argv[1]=='album':
    print(album)
else:
    print('You have to use artiste,titre or album')
