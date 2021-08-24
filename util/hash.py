# -*- coding:utf-8 -*-

__all__=[
    'getMD5',
    'getSHA256',
    'encodeBase64',
    'decodeBase64'
]

################################################################################

import hashlib
import base64

################################################################################


def getMD5(path):
    with open(path, 'rb') as fr:
        m = hashlib.md5()
        for chunk in iter(lambda: fr.read(m.block_size * 128), b''):
            m.update(chunk)

        return m.hexdigest()


def getSHA256(path):
    with open(path, 'rb') as fr:
        m = hashlib.sha256()
        for chunk in iter(lambda: fr.read(m.block_size * 128), b''):
            m.update(chunk)

        return m.hexdigest()


def encodeBase64(path):
    return base64.b64encode(getMD5(path).encode())


def decodeBase64(encoded):
    return base64.b64decode(encoded)
