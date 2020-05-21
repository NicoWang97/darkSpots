# coding: utf-8
from PIL import Image


def resize(src_path_name,resize_path_name):
    file = src_path_name
    img = Image.open(file)
    w,h = img.size
    w,h = round(w * 0.2),round(h * 0.2)		# 去掉浮点，防报错
    img = img.resize((w,h), Image.ANTIALIAS)
    img.save(resize_path_name, optimize=True, quality=85)	# 质量为85效果最好




