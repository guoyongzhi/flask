# import os
# import time
# path = os.path.dirname(os.path.abspath(__file__))
# print(path)
#
# alis = ["Media", time.strftime("%Y-%m"), time.strftime("%d")]
# uploads_dir = path
# for i in alis:
#     uploads_dir = os.path.join(uploads_dir, i)
#     if os.path.exists(uploads_dir) and os.path.isdir(uploads_dir):
#         pass
#     else:
#         os.mkdir(uploads_dir)
# print(uploads_dir)
# filename = '0144574.jpg'
#
# print(os.path.join('\\'.join(alis), filename))


import requests as req
from PIL import Image
from io import BytesIO


def make_thumb(url, sizes=(128, 128)):
    """
    生成指定尺寸缩略图
    :param url: 图像链接
    :param sizes: 指定尺寸
    :return: 无返回，直接保存图片
    """
    response = req.get(url)
    im = Image.open(BytesIO(response.content))
    mode = im.mode
    if mode not in ('L', 'RGB'):
        if mode == 'RGBA':
            # 透明图片需要加白色底
            alpha = im.split()[3]
            bgmask = alpha.point(lambda x: 255 - x)
            im = im.convert('RGB')
            im.paste((255, 255, 255), None, bgmask)
        else:
            im = im.convert('RGB')
    
    # 切成方图，避免变形
    width, height = im.size
    if width == height:
        region = im
    else:
        if width > height:
            # h*h
            delta = (width - height) / 2
            box = (delta, 0, delta + height, height)
        else:
            # w*w
            delta = (height - width) / 2
            box = (0, delta, width, delta + width)
        region = im.crop(box)
    
    # resize
    thumb = region.resize((sizes[0], sizes[1]), Image.ANTIALIAS)
    # 保存图片
    filename = url.split('/')[-1]
    name, ext = filename.split('.')
    savename = name + str(sizes[0]) + '_' + str(sizes[1]) + '.' + ext
    thumb.save(savename, quality=100)


url = 'http://lh3.ggpht.com/_S0f-AWxKVdM/SdeJxV3uhDI/AAAAAAAAHrY/FVTEpdNf4X0/lenna%5B4%5D.jpg'
make_thumb(url)