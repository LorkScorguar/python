#!/usr/bin/python2.7
import pynotify

pynotify.init("moc")

def notify(title,body):
	n = pynotify.Notification(title,body)
	n.show()

notify("Next Song","Artiste-Title")
