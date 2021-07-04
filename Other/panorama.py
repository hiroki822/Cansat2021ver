import cv2
import os
import glob
import time


def panorama(srcdir,prefix='',srcext='.jpg',dstext='.jpg'):
    """
    パノラマを合成するための関数
    ソースディレクトリ内に合成用の写真を番号をつけて入れておく。（例：IMG0.jpg,IMG1.jpg）
    srcdir:ソースディレクトリ
    prefix:番号の前につける文字
    srcext:ソースの拡張子
    dstext:できたものの拡張子
    """
    srcfilecount = len(glob.glob1(srcdir + '/', '*'+srcext))
    resultcount = len(glob.glob1('result/', srcdir, '*'+dstext))
    photos = []

    for i in range(0, srcfilecount):
        photos.append(cv2.imread(srcdir +'/' + prefix + str(i) + srcext))

    stitcher = cv2.Stitcher.create(0)
    status, result = stitcher.stitch(photos)
    cv2.imwrite('result/' + srcdir + '-' + str(resultcount) + srcext, result)

    if status == 0:
        print("success")
    else:
        print('failed')


if __name__ == "__main__":
    try:
        tratTime = time.time()  # プログラムの開始時刻
        panorama(srcdir)
        endTime = time.time() #プログラムの終了時間
        runTime = endTime - stratTime
        print(runTime)
    except:
        print('Error')
