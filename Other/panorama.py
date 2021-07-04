import cv2
import os
import glob
import time


def panorama(srcdir,prefex='',file='.jpeg'):
    srcfilecount = len(glob.glob1(srcdir + '/', '*'+file))
    resultcount = len(glob.glob1('result/', srcdir+'*.jpeg'))
    photos = []

    for i in range(0, srcfilecount):
        photos.append(cv2.imread(srcdir +'/' + prefex + str(i) + file))

    stitcher = cv2.Stitcher.create(0)
    status, result = stitcher.stitch(photos)
    cv2.imwrite('result/' + srcdir + '-' + str(resultcount) + '.jpeg', result)

    if status == 0:
        print("success")
    else:
        print('failed')




stratTime = time.time()  # プログラムの開始時刻

# 処理
panorama(srcdir='nisho-ground12_640×480',prefex='',file='.jpg')

endTime = time.time()
runTime = endTime - stratTime

print(runTime)
