百度音乐插件(深度音乐播放器)
========================

安装
----


```bash

sudo apt-get install cython libwebkitgtk-dev 

git clone https://github.com:sumary/pyjavascriptcore.git
cd pyjavascriptcore
sudo python setup.py install


git clone https://github.com:sumary/dmusic-plugin-baidumusic.git
cd dmusic-plugin-baidumusic
cp -r baidumusic ~/.local/share/deepin-music-player/plugins/
```
运行深度音乐， 选项设置->附加组件 中启用百度音乐即可
