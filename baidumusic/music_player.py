#! /usr/bin/env python
# -*- coding: utf-8 -*-

from events import event_manager

try:
    from simplejson import json
except ImportError:    
    import json
    
from resources import parse_to_dsong    


class MusicPlayer(object):        
    down_type = 0
    
    @property
    def ClientInfo(self):
        info = dict(bduss="",
                    client_version="8.0.0.5",
                    is_hq_enabled=0,
                    vip_level=1,
                    )
        return json.dumps(info)
    
    def AddSongs(self, dummy_songs):
        ''' '''
        songs = self.parse_dummy_songs(dummy_songs)
        if songs:        
            event_manager.emit("add-songs", songs)
        
    def PlaySongs(self, dummy_songs):    
        songs = self.parse_dummy_songs(dummy_songs)
        if songs:
            event_manager.emit("play-songs", songs)
            
    def FavoriteSongs(self, dummy_songs):
        pass
    
    def DownloadSongs(self, args):    
        print args
        
    @classmethod    
    def parse_dummy_songs(cls, dummy_songs):    
        songs = []
        for i in dummy_songs:
            song = parse_to_dsong(dummy_songs[i])
            if song:
                songs.append(song)
        return songs        
    
    def Login(self):
        print "login"
        
    def alert(self, *args):    
        print args
    
                
class PlayerInterface(object):
    
    def setLoginCallBackType(self, down_type):
        MusicPlayer.down_type = down_type
        
        
class TTPDownload(object):        
    
    def init(self, down_type, dummy_songs):
        print "Don't support"
        # print MusicPlayer.parse_dummy_songs(dummy_songs)
