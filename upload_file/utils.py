"""
1/ get_file_md5: 获取文件的md5
2/ hummanize_byte 返回可读的文件大小
 hummanize_bytes(100)
3/get_file_path 根据上传文件的目录获取文件路径
"""

import os
import hashlib
from functools import partial
from config import UPLOAD_FOLDER


#here表示本文件的当前目录路径
HERE=os.path.abspath(os.path.dirname(__file__))
def get_file_md5(f,chunk_size=8192):
    h=hashlib.md5()
    while True:
        chunk=f.read(chunk_size)
        if not chunk:
            break
        h.update(chunk)
    return h.hexdigest()

def humansize_bytes(bytesize,precision=2):
    abbrevs=(
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'bytes'),
    )
    if bytesize==1:
        return '1 byte'
    for factor,suffix in abbrevs:
        if bytesize>=factor:
            break
    return '%.*f %s' %(precision,bytesize/factor,suffix)


get_file_path=partial(os.path.join,HERE,UPLOAD_FOLDER)