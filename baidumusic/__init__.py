#! /usr/bin/env python
# -*- coding: utf-8 -*-

from music_browser import MusicBrowser
from music_view import MusicView
from nls import _
from helper import Dispatcher, SignalCollector
from widget.tab_box import  ListTab

music_browser = MusicBrowser()
music_list = MusicView()
radio_list_tab = ListTab(_("百度音乐"), music_list, music_browser)

def enable(dmusic):
    SignalCollector.connect("baidumusic", Dispatcher, "being-quit", lambda w: music_list.save())
    Dispatcher.emit("add-source", radio_list_tab)
    
def disable(dmusic):    
    SignalCollector.disconnect_all("baidumusic")
    Dispatcher.emit("remove-source", radio_list_tab)
