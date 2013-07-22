#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gobject
import copy
import time

from dtk.ui.treeview import TreeView
from dtk.ui.threads import post_gui

from widget.ui_utils import draw_alpha_mask
from widget.song_item import SongItem
from player import Player
from events import event_manager
from resources import request_songinfo

import utils
from xdg_support import get_config_file
from song import Song

class MusicView(TreeView):
    
    __gsignals__ = {
        "begin-add-items" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        "empty-items" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
        }
    
    
    def __init__(self):
        TreeView.__init__(self, enable_drag_drop=False, enable_multiple_select=True)        
        
        self.connect("double-click-item", self.on_music_view_double_click)
        self.connect("press-return", self.on_music_view_press_return)
        
        event_manager.connect("add-songs", self.on_event_add_songs)
        event_manager.connect("play-songs", self.on_event_play_songs)
        
        self.db_file = get_config_file("baidumusic.db")
        self.load()
        
        self.request_thread_id = 0
        
    def on_event_add_songs(self, obj, data):    
        self.add_songs(data)
        
    def on_event_play_songs(self, obj, data):
        self.add_songs(data, play=True)
        
    @property    
    def items(self):
        return self.get_items()
    
    def on_music_view_double_click(self, widget, item, colume, x, y):
        if item:
            song = item.get_song()
            self.request_song(song, play=True)
    
    def on_music_view_press_return(self, widget, items):
        if items:
            song = items[0].get_song()
            self.request_song(song, play=True)
            
    def draw_mask(self, cr, x, y, width, height):            
        draw_alpha_mask(cr, x, y, width, height, "layoutMiddle")
            
    def set_current_source(self):        
        if Player.get_source() != self:
            Player.set_source(self)
            
    def emit_add_signal(self):
        self.emit("begin-add-items")
    
    def request_song(self, song, play=True):        
        if self.adjust_uri_expired(song):
            self.request_thread_id += 1
            thread_id = copy.deepcopy(self.request_thread_id)
            utils.ThreadFetch(
                fetch_funcs=(request_songinfo, (song,)),
                success_funcs=(self.render_play_song, (play, thread_id))
                ).start()
        else:    
            self.play_song(song, play=True)
        
    def adjust_uri_expired(self, song):    
        expire_time = song.get("uri_expire_time", None)
        duration = song.get("#duration", None)        
        fetch_time = song.get("fetch_time", None)
        if not expire_time or not duration or not fetch_time or not song.get("uri", None):
            return True
        now = time.time()
        past_time = now - fetch_time
        if past_time > (expire_time - duration) / 1000 :
            return True
        return False
            
    def play_song(self, song, play=False):    
        if not song: return None        
        
        # update song info
        self.update_songitem(song)
        
        # clear current select status
        del self.select_rows[:]
        self.queue_draw()
            
        # set item highlight
        self.set_highlight_song(song)
        
        if play:
            # play song now
            Player.play_new(song)
            
            # set self as current global playlist
            self.set_current_source()
            
        return song    
    
    @post_gui
    def render_play_song(self, song, play, thread_id):
        if thread_id != self.request_thread_id:
            return
        
        song["fetch_time"] = time.time()
        self.play_song(song, play)
    
    def get_songs(self):    
        songs = []
        self.update_item_index()
        for song_item in self.items:
            songs.append(song_item.get_song())
        return songs    
        
    def add_songs(self, songs, pos=None, sort=False, play=False):    
        if not songs:
            return
        
        if not isinstance(songs, (list, tuple, set)):
            songs = [ songs ]
            
        song_items = [ SongItem(song) for song in songs if song not in self.get_songs() ]
        
        if song_items:
            if not self.items:
                self.emit_add_signal()
            self.add_items(song_items, pos, False)
            
            # save songs
            self.save()
            
        if len(songs) >= 1 and play:
            song = songs[0]
            self.request_song(song, play=True)

            
    def set_highlight_song(self, song):        
        if not song: return 
        if SongItem(song) in self.items:
            self.set_highlight_item(self.items[self.items.index(SongItem(song))])
            self.visible_highlight()
            self.queue_draw()
            
    def update_songitem(self, song):        
        if not song: return 
        if SongItem(song) in self.items:
            self.items[self.items.index(SongItem(song))].update(song, True)
            
    def get_next_song(self, maunal=False):        
        if len(self.items) <= 0:
            return 
        
        if self.highlight_item:
            if self.highlight_item in self.items:
                current_index = self.items.index(self.highlight_item)
                next_index = current_index + 1
                if next_index > len(self.items) - 1:
                    next_index = 0
                highlight_item = self.items[next_index]    
            else:    
                highlight_item = self.items[0]
        else:        
            highlight_item = self.items[0]
            
        self.request_song(highlight_item.get_song(), play=True)
    
    def get_previous_song(self):
        if len(self.items) <= 0:
            return 
        
        if self.highlight_item != None:
            if self.highlight_item in self.items:
                current_index = self.items.index(self.highlight_item)
                prev_index = current_index - 1
                if prev_index < 0:
                    prev_index = len(self.items) - 1
                highlight_item = self.items[prev_index]    
        else:        
            highlight_item = self.items[0]
            
        self.request_song(highlight_item.get_song(), play=True)
    
    def save(self):
        objs = [ song.get_dict() for song in self.get_songs() ]
        utils.save_db(objs, self.db_file)
        
    def load(self):    
        objs = utils.load_db(self.db_file)
        songs = []
        if objs:
            for obj in objs:
                s = Song()
                s.init_from_dict(obj, cmp_key="sid")
                songs.append(s)
        if songs:        
            self.add_songs(songs)
