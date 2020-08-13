#!/usr/bin/env python
# -*- coding:utf-8 -*-
#图片批量加水印
#20200812
#author:harry
#addWate.py
from time import time
from threading import Thread
from PIL import Image
import os,random

"""
定义一个class，图片的所有属性包括在其中，宽，高，自适应，resize

"""
def addWater(logo,image,n):

    image_log = Image.open(logo)
    w,h = image_log.size
    image_log = image_log.resize((int(w*n),int(h*n)),Image.ANTIALIAS)
    layer = Image.new('RGBA',(800,800),(0,0,0,0))
    layer.paste(image_log,(100,100))
    out = Image.composite(layer,image,layer)
    return out




class Picture(object):

    def __init__(self,path):
        self._path = path
        self._basename = os.path.split(self._path)[-1]
        self._img = Image.open(self._path)
        self.__width =0
        self.__heigth = 0

    @property
    def width(self):
        return self._img.size[0]

    @property
    def heigth(self):
        return self._img.size[1]

    def resize(self):
        #按长边等比例缩放
        print(self.width,self.heigth)
        if self.width != self.heigth:
            if self.width > self.heigth:
                self.width,self.heigth = self.heigth,self.width
            scale = self.width/self.heigth
            new_img = self._img.resize((int(800*scale),800),Image.ANTIALIAS)
            return new_img

    def addLayer(self,c1):
        #添加一层空白图层
        #parmer：c1:图片resize后的image对象
        #返回两边空白，图片(800*800)在中间的image对象
        layer = Image.new("RGBA",(800,800),(0,0,0,0))
        w1=400 - c1.size[0]/2
        layer.paste(c1,(int(w1),0))
        return layer
    
    def autoFill(self,c1,c2):
        #判断边界像素，向左或向右自动填充边界像素值
        w1,h1 = c1.size
        w_left = int(400-w1/2) +1#左边界
        w_right = 800-w_left-1#右边界
        for h in range(0,800):
            pixel1 = c1.getpixel((0,h))
            pixel2 = c1.getpixel((w1-1,h))
            for w in range(0,w_left):
                c2.putpixel((w,h),pixel1)
            for w in range(w_right,800):
                c2.putpixel((w,h),pixel2)
        self._img = c2
        return c2    
        #c2.save("./c2.png")
    def run(self,logo,n):
        c1 = self.resize()
        c2 = self.addLayer(c1)
        self.autoFill(c1,c2)
        out = addWater(logo,c2,n)
        out = out.convert('RGB')
        if not os.path.exists("./result"):
            print("不存在result文件夹")
            os.mkdir("./result")
        des_path = os.path.split(self._path)[0] + "/"+"result"
        filename = des_path +"/"+ self._basename
        #统一生成jpg格式的图片
        if os.path.splitext(filename)[-1] != ".jpg":
            print("改名为jpg")
            filename = os.path.splitext(filename)[0]+'.jpg'
            
        out.save(filename)

class PictureHandler(Thread):

    def __init__(self,picture,logo,n):
        super().__init__()
        self.pic=picture
        self.logo = logo
        self.n = n

    def run(self):
        pic1 = Picture(self.pic)
        pic1.run(self.logo,self.n)


def main():
    src_path = input("请输入处理的图片所在的目录（例：G:\练手项目\批量加水印）：")
    logo_path = input("请输入logo所在的目录（例：G:\练手项目\批量加水印\logo.png）：")
    picFiles = [os.path.join(src_path,fn) for fn in os.listdir(src_path) if fn.endswith(('.jpg','.gif','.png'))]
    print(picFiles)
    start = time()
    threads = []
    for pic in picFiles:
        Picture(pic).run(logo_path,1.5)
        #t = PictureHandler(pic,"./logo.png",1.5)
        #t.start()
        #threads.append(t)
    for t in threads:
        t.join()
    end = time()
    print("Done, 用时：",(end-start),"s")
if __name__ =="__main__":
    main()
