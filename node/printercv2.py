#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cv2

if __name__ == "__main__":
   f = open("cv.txt","w")
   text = str(dir(cv2))
   f.write(text)
   f.close()
