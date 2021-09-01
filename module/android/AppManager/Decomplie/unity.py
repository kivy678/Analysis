# -*- coding:utf-8 -*-

__all__ = [
    "runDecodeMono",
    "runDecodeil2cpp",
]

#############################################################################

from util.fsUtils import *

from module.mobile.cmd import shell

from common import getSharedPreferences
from webConfig import SHARED_PATH

from util.Logger import LOG

#############################################################################

sp                  = getSharedPreferences(SHARED_PATH)
JUST_DECOMPILE_PATH = sp.getString('JUST_DECOMPILE_PATH')
IL2CPP_DUMPER_PATH  = sp.getString('IL2CPP_DUMPER_PATH')
DECODE_DIR          = sp.getString('DECODE_DIR')

CSHARP_FILE         = "Assembly-CSharp.dll"
IL2CPP_FILE         = "libil2cpp.so"
GLOBAL_META         = "global-metadata.dat"

FILTER_LIST         = ["Assembly-CSharp.csproj", "Assembly-CSharp.sln", "Assembly-CSharpReferences"]

#############################################################################

def clean(_path):
    Delete(_path)
    DirCheck(_path)


def searchFile(dir, fileName):
    for i in Walk(dir):
        if PathSplit(i)[1] == fileName:
            return i


def isIl2cpp(_path):
    if searchFile(Join(_path, 'lib'), IL2CPP_FILE):
        return True
    else:
        return False


def isMono(_path):
    if searchFile(Join(_path, 'assets'), CSHARP_FILE):
        return True
    else:
        return False


def runDecodeMono(_path, fileName):
    out = Join(DECODE_DIR, fileName, 'mono')
    clean(out)

    if isMono(_path):
        LOG.info(f"{'[*]':<5}Start mono Decode: {fileName}")

        csharp_path = searchFile(Join(_path, r'assets\bin\Data\Managed'), CSHARP_FILE)

        cmd = f"{JUST_DECOMPILE_PATH} /lang:csharp /out:{out} /target:{csharp_path}"
        shell.runCommand(cmd)

        for name in FILTER_LIST:
            Delete(Join(out, name))

        LOG.info(f"{'[*]':<5}End mono Decode: {fileName}")

        return csharp_path

    return None


def runDecodeil2cpp(_path, fileName):
    out = Join(DECODE_DIR, fileName, 'il2cpp')
    clean(out)

    if isIl2cpp(_path):
        LOG.info(f"{'[*]':<5}Start il2cpp Decode: {fileName}")

        lib_path = searchFile(Join(_path, 'lib'), IL2CPP_FILE)
        global_metadata_path = searchFile(Join(_path, r'assets\bin\Data\Managed\Metadata'), GLOBAL_META)

        cmd = f"{IL2CPP_DUMPER_PATH} {lib_path} {global_metadata_path} {out}"
        shell.runCommand(cmd)

        LOG.info(f"{'[*]':<5}End il2cpp Decode: {fileName}")

        return lib_path

    return None
