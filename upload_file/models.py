import os
import uuid
import magic
from datetime import datetime

try:
    from urllib import quote
except:
    from urllib.parse import quote
import cropresize2
import short_url
from PIL import Image
from flask import abort,request
from werkzeug.utils import cached_property

from .mimes import IMAGE_MIMES,AUDIO_MIMES,VIDEO_MIMES
from .utils import get_file_md5,get_file_path
from .ext import db

class PasteFile(db.Model):
    __tablename__='PasteFile'
    id=db.Column(db.Integer,primary_key=True)
    filename=db.Column(db.String(5000),nullable=True)
    filehash=db.Column(db.String(128),nullable=False)
    filemd5=db.Column(db.String(128),nullable=False)
    uploadtime=db.Column(db.DateTime,nullable=False)
    mimetype=db.Column(db.String(256),nullable=False)
    size=db.Column(db.Integer,nullable=False)

    def __init__(self,filename='',mimetype='application/octet-stream',
                 size=0, filehash=None, filemd5=None):
        self.uploadtime = datetime.now()
        self.mimetype = mimetype
        self.size = int(size)
        self.filehash = filehash if filehash else self._hash_filename(filename)
        self.filename=filename if filename else self.filehash
        self.filemd5 = filemd5

    @staticmethod
    def _hash_filename(filename):
        _, _, suffix = filename.rpartition('.')
        return '%s.%s' % (uuid.uuid4().hex, suffix)

    @cached_property
    def symlink(self):
        return short_url.encode_url(self.id)

    #cls 表示这个类别的代表
    @classmethod
    def get_by_filehash(cls,symlink,code=404):
        id=short_url.decode_url(symlink)
        return cls.query.filter_by(id=id).first() or abort(code)

    @classmethod
    def get_by_filehash(cls, filehash, code=404):
        return cls.query.filter_by(filehash=filehash).first() or abort(code)

    @classmethod
    def get_by_md5(cls, filemd5):
        return cls.query.filter_by(filemd5=filemd5).first()

    @classmethod
    def create_by_upload_file(cls,uploaded_file):
        rst=cls(uploaded_file.filename)
