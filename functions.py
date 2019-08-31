# -*- coding: utf-8 -*-
from urllib import request,parse
from http.cookiejar import CookieJar
import cv2
import os
import shutil
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow

def login(url):
    #cookieJar=bc.chrome()
    cookieJar=CookieJar()
    handler=request.HTTPCookieProcessor(cookieJar)
    opener=request.build_opener(handler)
    resobj=opener.open(url)
    res=resobj.read().decode('utf-8')
    return res



# def download_multiThread(url_list):
#     max_threading_count=16
#     if not (os.path.exists('downloads')):
#         os.mkdir('downloads')
#     else:
#         shutil.rmtree('downloads')
#         os.mkdir('downloads')
#     iter=0
#     for url in url_list:
#         iter+=1
#         filename='downloads/'+url.split('/')[-1]
#         t=threading.Thread(target=download_singleThread,args=(url,filename,))
#         t.start()
#         while True:
#             if (len(threading.enumerate())<max_threading_count):
#                 break
#     while True:
#         if (len(threading.enumerate())==0):
#             break
#
#
#
# def download_singleThread(url,filePath):
#     request.urlretrieve(url, filePath)


