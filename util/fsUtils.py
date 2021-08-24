# -*- coding:utf-8 -*-

__all__=[
    'isExist',
    'isDir',
    'isFile',
    'Join',
    'DirName',
    'Relative',
    'RealPath',
    'BaseName',
    'FileSize',
    'PathSplit',
    'SplitExt',
    'GetSize',
    'DirCheck',
    'Copy',
    'Delete',
    'Walk',
]

################################################################################

import os
import shutil

################################################################################

isExist   = os.path.exists
isDir     = os.path.isdir
isFile    = os.path.isfile
Join      = os.path.join
DirName   = os.path.dirname
Relative  = os.path.relpath
RealPath  = os.path.realpath
BaseName  = os.path.basename
FileSize  = os.path.getsize
PathSplit = os.path.split
SplitExt  = os.path.splitext
GetSize   = os.path.getsize

def DirCheck(dp, created:bool = True, mask:int = 0o755) -> bool:
    if isExist(dp) is True:
        if isDir(dp) is True:
            return True
        return False

    if created is False:
        return False

    try:
        os.makedirs(dp, mask)
        return True
    except:
        return False

def Copy(src, dst) -> bool:
    if isDir(src):
        return CopyDir(src, dst)
    else:
        return CopyFile(src, dst)

def CopyDir(src, dst) -> bool:
    if isExist(dst) is True:
        Delete(dst)

    try:
        shutil.copytree(src, dst)
        return True
    except:
        shutil.rmtree(dst)
        return False

def CopyFile(src, dst) -> bool:
    if DirCheck(DirName(dst)) is False:
        raise Exception('Copy destination check failed')

    try:
        shutil.copy(src, dst)
        return True
    except:
        return False

def Delete(path):
    if isDir(path):
        return DeleteDir(path)
    else:
        return DeleteFile(path)

def DeleteDir(path):
    try:
        shutil.rmtree(path)
        return True
    except:
        return False

def DeleteFile(path):
    try:
        os.unlink(path)
        return True
    except:
        return False

def Walk(path):
    for _r, _d, _fl in os.walk(path):
        for fn in _fl:
            yield os.path.join(_r, fn)
    #raise StopIteration
