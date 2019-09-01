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

class MyWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
    def closeEvent(self, event):
        for thread in threads_list:
            if thread.poll()==None:
                thread.terminate()
        event.accept()

def start(url,textlbl,btn_login):
    textlbl.clear()
    btn_login.setDisabled(True)
    try:
        resp=functions.login(url)
    except:
        textlbl.append("网页登陆异常，请检查输入地址是否可用!")
        btn_login.setDisabled(False)
        return
    textlbl.append("Retriving movie resources......")
    playlist = re.findall('var \$playlist="(.*?)"', resp)[0]
    playurl='http://532movie.bnu.edu.cn/'+playlist.split('+++')[0]
    textlbl.append(playurl)
    resources_list=get_tf_resources(playurl,textlbl)
    textlbl.append("Downloading ts files......")
    try:
        download(resources_list,textlbl)
    except:
        textlbl.append("下载ts文件失败，请检查网络状况!")
        btn_login.setDisabled(False)
        return
    textlbl.append('Merging mp4, please wait......')
    mergets()
    textlbl.append("Code transferring......")
    try:
        p=ffmpeg()
        counter=0
        while True:
            counter+=1
            status=p.poll()
            if status!=None:
                if status==0:
                    break
                else:
                    textlbl.append("编码转换失败，请联系技术人员解决!")
                    btn_login.setDisabled(False)
                    return
            else:
                if(counter>2):
                    counter=1
                if(counter==1):
                    textlbl.append('code transferring, please wait O(∩_∩)O')
                else:
                    textlbl.append('code transferring, please wait (#^.^#)')
            QApplication.processEvents()
            time.sleep(1)

    except:
        textlbl.append("编码转换失败，请联系技术人员解决!")
        btn_login.setDisabled(False)
        return
    try:
        clean()
    except:
        textlbl.append("清理程序执行失败，请手动删除downloads里的临时文件!")
    textlbl.append('Merge finish! Enjoy your movie!(*^_^*)')
    btn_login.setDisabled(False)




def get_tf_resources(playurl,textlbl):
    resp=functions.login(playurl)
    resources_list = re.findall('http://.*?ts', resp)
    textlbl.append('------------Movie resources retrived successfully-------------')
    for i in resources_list:
        textlbl.append(i)
    return resources_list

def download(resources_list,textlbl):
    time_Start=time.time()
    if not (os.path.exists('downloads')):
        os.mkdir('downloads')
    else:
        shutil.rmtree('downloads')
        os.mkdir('downloads')
    iter=0
    for i in resources_list:
        iter+=1
        textlbl.append('Downloading file %s, entire percentage: %.2f'%(i,100.0*iter/len(resources_list)))
        filename = 'downloads/' + i.split('/')[-1]
        request.urlretrieve(i,filename)
        QApplication.processEvents()
    time_end=time.time()
    time_elapsed=time_end-time_Start
    textlbl.append('Finish download! Time elapsed: %s s'%time_elapsed)

def mergets():
    with open(r'downloads\movie.ts','wb') as f:
        for i in glob.glob(r'downloads\*.ts'):
            with open(i,'rb') as f2:
                f.write(f2.read())

def ffmpeg():
    if (os.path.exists(r'downloads\movie.mp4')):
        os.remove(r'downloads\movie.mp4')
    p=subprocess.Popen(os.getcwd()+r'\ffmpeg\bin\ffmpeg.exe -i '+os.getcwd()+r'\downloads\movie.ts -vcodec h264 '+os.getcwd()+r'\downloads\movie.mp4')
    threads_list.append(p)
    return p

#删除临时文件
def clean():
    ts_list=glob.glob(r'downloads\*.ts')
    for i in ts_list:
        if(os.path.exists(i)):
            os.remove(i)
    if(os.path.exists(r'downloads\movie.ts')):
        os.remove(r'downloads\movie.ts')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.setFixedSize(886, 391)
    palette = QPalette()
    palette.setBrush(QPalette.Background, QBrush(QPixmap("bg2.jpg")))
    myWin.setPalette(palette)
    myWin.btn_login.clicked.connect(lambda:start(myWin.label_movieUrl.text(),myWin.textlbl,myWin.btn_login))
    myWin.show()
    sys.exit(app.exec_())


