# -*- coding:utf-8 -*-

import os
os.environ['PATH']=os.getcwd()+';'+os.environ['PATH']
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPalette,QBrush, QPixmap
import ui
import functions
import re
from urllib import request
import shutil
import time
import subprocess
import glob

threads_list=[]#子线程列表
PLAY_LIST=None#m3u8链接列表

class MyWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
    def closeEvent(self, event):
        for thread in threads_list:
            if thread.poll()==None:
                thread.terminate()
        event.accept()
        sys.exit()

def btn_event_login(url,textlbl,label_movieName,label_episode,spinBox_episode,btn_login):
    global  PLAY_LIST
    PLAY_LIST=None
    spinBox_episode.setDisabled(True)
    spinBox_episode.setVisible(False)
    label_movieName.clear()
    spinBox_episode.setValue(-1)
    try:
        resp = functions.login(url)
    except:
        textlbl.append("网页登陆异常，请检查输入地址是否可用!")
        return
    textlbl.append("Retriving movie resources......")
    try:
        playlist = re.findall('var \$playlist="(.*?)"', resp)[0]
        movieName = re.findall('正在播放：(.*?) ', resp)[0]  # 电影名
        label_movieName.setText('正在下载: ' + movieName)
    except:
        textlbl.append('页面打开错误，请输入播放页面的网页地址.')
        return
    if len(playlist.split('+++')) > 1:
        label_episode.setText('共%d集,请选择集数(输入0则下载全集)：' % len(playlist.split('+++')))
        spinBox_episode.setDisabled(False)
        spinBox_episode.setVisible(True)
        myWin.spinBox_episode.setMaximum(len(playlist.split('+++')))
        myWin.spinBox_episode.setValue(-1)
    else:
        label_episode.setText("电影，无需选择集数")
    PLAY_LIST=playlist


def btn_event_download(textlbl,spinBox_episode,label_movieName,btn_download,btn_login):
    btn_download.setDisabled(True)
    btn_login.setDisabled(True)
    label_movieName_Original=label_movieName.text()
    if PLAY_LIST==None:
        textlbl.append('请先点击search按钮搜索资源......')
        btn_download.setDisabled(False)
        btn_login.setDisabled(False)
        return
    if len(PLAY_LIST.split('+++'))>1:
        if spinBox_episode.value()==-1:
            textlbl.append('请选择集数......')
            btn_download.setDisabled(False)
            btn_login.setDisabled(False)
            return
        spinBox_episode.setDisabled(True)
        if spinBox_episode.value()==0:
            textlbl.append('有点贪，想要下载全集，需要花费很长时间哦~~~')
            wait_for_seconds(5,textlbl)
            for i in range(len(PLAY_LIST.split('+++'))):
                textlbl.append('正在下载第%d集，/(ㄒoㄒ)/~~'%(i+1))
                label_movieName.setText(label_movieName_Original + ' 第%d集'%(i+1))
                wait_for_seconds(3,textlbl)
                savePath=r'downloads\第%d集'%(i+1)
                playurl = 'http://532movie.bnu.edu.cn/' + PLAY_LIST.split('+++')[i]
                download_single_episode(savePath,playurl,textlbl,btn_download)
        else:
            playurl = 'http://532movie.bnu.edu.cn/' + PLAY_LIST.split('+++')[spinBox_episode.value()-1]
            label_movieName.setText(label_movieName_Original+' 第%d集'%(spinBox_episode.value()))
            wait_for_seconds(5,textlbl)
            savePath = r'downloads\第%d集'%(spinBox_episode.value())
            download_single_episode(savePath,playurl,textlbl,btn_download)
    else:
        playurl = 'http://532movie.bnu.edu.cn/' + PLAY_LIST.split('+++')[0]
        savePath='downloads'
        wait_for_seconds(5,textlbl)
        download_single_episode(savePath,playurl,textlbl,btn_download)

    btn_download.setDisabled(False)
    btn_login.setDisabled(False)
    spinBox_episode.setDisabled(False)


#下载单集
def download_single_episode(savePath,playurl,textlbl,btn_download):
    resources_list=get_tf_resources(playurl,textlbl)
    textlbl.append("Downloading ts files......")
    try:
        download(savePath,resources_list,textlbl)
    except:
        textlbl.append("下载ts文件失败，请检查网络状况!")
        btn_download.setDisabled(False)
        return
    textlbl.append('Merging mp4, please wait......')
    mergets(savePath)
    textlbl.append("Code transferring......")
    try:
        p=ffmpeg(savePath)
        counter=0
        while True:
            counter+=1
            status=p.poll()
            if status!=None:
                if status==0:
                    break
                else:
                    textlbl.append("编码转换失败，请联系技术人员解决!")
                    btn_download.setDisabled(False)
                    return
            else:
                if(counter>2):
                    counter=1
                if(counter==1):
                    textlbl.append('code transferring, please wait O(∩_∩)O')
                else:
                    textlbl.append('code transferring, please wait (#^.^#)')
            QApplication.processEvents()
            time.sleep(0.01)

    except:
        textlbl.append("编码转换失败，请联系技术人员解决!")
        btn_download.setDisabled(False)
        return
    try:
        clean(savePath)
    except:
        textlbl.append("清理程序执行失败，请手动删除downloads里的临时文件!")
    textlbl.append('Merge finish! Enjoy your movie!(*^_^*)')




def get_tf_resources(playurl,textlbl):
    resp=functions.login(playurl)
    resources_list = re.findall('http://.*?ts', resp)
    textlbl.append('------------Movie resources retrived successfully-------------')
    for i in resources_list:
        textlbl.append(i)
    return resources_list

def download(savePath,resources_list,textlbl):
    time_Start=time.time()
    if not (os.path.exists(savePath)):
        os.mkdir(savePath)
    else:
        shutil.rmtree(savePath)
        os.mkdir(savePath)
    iter=0
    for i in resources_list:
        iter+=1
        textlbl.append('Downloading file %s, entire percentage: %.2f'%(i,100.0*iter/len(resources_list)))
        filename = savePath+'\\' + i.split('/')[-1]
        request.urlretrieve(i,filename)
        QApplication.processEvents()
    time_end=time.time()
    time_elapsed=time_end-time_Start
    textlbl.append('Finish download! Time elapsed: %s s'%time_elapsed)

def mergets(savePath):
    with open(savePath+r'\movie.ts','wb') as f:
        for i in glob.glob(savePath+r'\*.ts'):
            with open(i,'rb') as f2:
                f.write(f2.read())

def ffmpeg(savePath):
    if (os.path.exists(savePath+r'\movie.mp4')):
        os.remove(savePath+r'\movie.mp4')
    p=subprocess.Popen(os.getcwd()+r'\ffmpeg\bin\ffmpeg.exe -i '+os.getcwd()+'\\'+savePath+r'\movie.ts -vcodec h264 '+os.getcwd()+'\\'+savePath+r'\movie.mp4')
    threads_list.append(p)
    return p

#删除临时文件
def clean(savePath):
    ts_list=glob.glob(savePath+r'\*.ts')
    for i in ts_list:
        if(os.path.exists(i)):
            os.remove(i)
    if(os.path.exists(savePath+r'\movie.ts')):
        os.remove(savePath+r'\movie.ts')

def wait_for_seconds(seconds,textlbl):
    for i in range(seconds,0,-1):
        textlbl.append('下载将于%d秒后开始......'%i)
        time.sleep(1)
        QApplication.processEvents()



if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.mkdir('downloads')
    else:
        shutil.rmtree('downloads')
        os.mkdir('downloads')
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.setFixedSize(886, 391)
    palette = QPalette()
    palette.setBrush(QPalette.Background, QBrush(QPixmap("bg2.jpg")))
    myWin.setPalette(palette)
    myWin.spinBox_episode.setVisible(False)
    myWin.spinBox_episode.setDisabled(True)
    myWin.btn_login.clicked.connect(lambda:btn_event_login(myWin.label_movieUrl.text(),myWin.textlbl,myWin.label_movieName,myWin.label_episode,myWin.spinBox_episode,myWin.btn_login))
    myWin.btn_download.clicked.connect(lambda: btn_event_download(myWin.textlbl,myWin.spinBox_episode,myWin.label_movieName,myWin.btn_download,myWin.btn_login))
    myWin.show()
    myWin.textlbl.append('请勿用作非法用途......\n技术交流请联系 wangqr@mail.bnu.edu.cn')
    sys.exit(app.exec_())


