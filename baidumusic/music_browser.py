#! /usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import webkit
import javascriptcore as jscore

from widget.ui import NetworkConnectFailed, LoadingBox
from deepin_utils.net import is_network_connected
from widget.ui_utils import switch_tab

from music_player import MusicPlayer, PlayerInterface, TTPDownload

class MusicBrowser(gtk.VBox):
    
    def __init__(self):
        super(MusicBrowser, self).__init__()
        
        # check network status
        self.loading_box = LoadingBox("正在加载数据，如果长时间没有响应，点击此处刷新", "此处", self.reload_browser)
        self.network_failed_box = NetworkConnectFailed(self.check_network_connection)
        self.check_network_connection(auto=True)

        self.webview = webkit.WebView()
        self.webview.set_transparent(True)
        
        settings = self.webview.get_settings()
        settings.set_property('enable-plugins', False)
        self.webview.set_settings(settings)
        
        self.webview.open("http://musicmini.baidu.com/static/recommend/recommend.html")
        self.js_context = jscore.JSContext(self.webview.get_main_frame().get_global_context()).globalObject                        
        self.webview.connect("load-finished", self.on_webview_load_finished)
        # self.webview.connect("load-started", self.on_webview_load_started)
        
        self._player = MusicPlayer()
        self._player_interface = PlayerInterface()
        self._ttp_download = TTPDownload()
        self.is_reload_flag = False
        
    def on_webview_load_started(self, widget, event):    
        self.injection_object()
        
    def check_network_connection(self, auto=False):    
        if is_network_connected():
            switch_tab(self, self.loading_box)
            if not auto:
                self.reload_browser()
        else:    
            switch_tab(self, self.network_failed_box)
            
    def reload_browser(self):        
        self.is_reload_flag = False
        self.webview.reload()
            
    def injection_object(self):
        self.js_context.player = self._player
        self.js_context.window.top.ttp_download = self._ttp_download
        self.js_context.window.top.playerInterface = self._player_interface
        self.js_context.link_support = True
        self.js_context.alert = self._player.alert
        
    def injection_js(self):    
        js_e = self.js_context.document.createElement("script")
        js_e.src = "http://musicmini.baidu.com/resources/js/jquery.js"
        self.js_context.document.appendChild(js_e)
        
    def on_webview_load_finished(self, widget, event):    
        if not self.is_reload_flag:
            self.webview.reload()
            self.is_reload_flag = True
        else:    
            self.injection_object()
            switch_tab(self, self.webview)
