from PIL import Image, ExifTags  # 安装依赖包：pip3 install pillow
from utils.file.compress import dynamic_quality
import os
import time


"""
PIL读取的图像发生自动旋转：https://blog.csdn.net/mizhenpeng/article/details/82794112
使用python批量压缩图片文件：https://blog.csdn.net/weixin_41855010/article/details/120723943
"""


def compress_jpg_png(filename, originpath):
    name = filename.rstrip('.png').rstrip('.jpg')
    im = Image.open(os.path.join(originpath, filename))
    # 解决图像方向问题
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation': break
            exif = dict(im._getexif().items())
            if exif[orientation] == 3:
                im = im.rotate(180, expand=True)
            elif exif[orientation] == 6:
                im = im.rotate(270, expand=True)
            elif exif[orientation] == 8:
                im = im.rotate(90, expand=True)
    except:
        pass
    # print(im.format,im.size,im.mode)
    im = im.convert('RGB')
    im.format = "JPEG"
    new_photo = im.copy()
    new_photo.thumbnail(im.size, resample=Image.ANTIALIAS)
    save_args = {'format': im.format}
    # print(save_args)
    # if im.format=='JPEG':
    # save_args['quality']=20
    save_args['quality'], value = dynamic_quality.jpeg_dynamic_quality(im)
    save_args['optimize'] = True
    save_args['progressive=True'] = True
    # print("JPEG Quality Changed")
    # elif im.format=='PNG':
    #     save_args['format']='JPEG'
    #     save_args['quality']=5
    #     print("PNG Quality Changed")
    new_file = os.path.join(originpath, name + str(int(time.time())) + ".jpg")
    new_photo.save(new_file, **save_args)
    return new_file


if __name__ == '__main__':
    print(compress_jpg_png("1.jpg", "E:\\test"))
