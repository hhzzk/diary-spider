# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file
import qiniu.config

from qiniu_conf import access_key, secret_key, bucket_name

def push_file(localfile):

    # File name in qiniu server
    key = localfile;

    q = Auth(access_key, secret_key)
    # Generate Token
    token = q.upload_token(bucket_name, key, 60)

    ret, info = put_file(token, key, localfile)

    if ret['key'] != key:
        return False

    return True
