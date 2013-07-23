百度音乐插件(深度音乐播放器)
========================

LinuxDeepin系统安装方法
----------------------
```
sudo apt-get install python-javascriptcore git

git clone https://github.com/sumary/dmusic-plugin-baidumusic.git
cd dmusic-plugin-baidumusic
cp -r baidumusic ~/.local/share/deepin-music-player/plugins/
```

其它Linux发行版
------------------

```
# 安装 cython libwebkitgtk-dev python-dev gtk, 例如:
sudo apt-get install cython libwebkitgtk-dev git

# 安装pyjavascriptcore
git clone https://github.com/sumary/pyjavascriptcore.git
cd pyjavascriptcore
sudo python setup.py install

# 安装百度音乐插件
git clone https://github.com/sumary/dmusic-plugin-baidumusic.git
cd dmusic-plugin-baidumusic
cp -r baidumusic ~/.local/share/deepin-music-player/plugins/
```

使用
----
运行深度音乐， 选项设置->附加组件 中启用百度音乐即可
