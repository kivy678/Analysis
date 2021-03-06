# -*- coding:utf-8 -*-

__all__ = [
    "runDecodeMono",
    "runDecodeil2cpp",
]

#############################################################################

from util.fsUtils import *

from module.android.cmd import shell

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

def clean(path):
    Delete(path)
    DirCheck(path)


def searchFile(dir, fileName):
    for i in Walk(dir):
        if PathSplit(i)[1] == fileName:
            return i


def isIl2cpp(path):
    if searchFile(Join(path, 'lib'), IL2CPP_FILE):
        return True
    else:
        return False


def isMono(path):
    if searchFile(Join(path, 'assets'), CSHARP_FILE):
        return True
    else:
        return False


def runDecodeMono(path, fileName):
    out = Join(DECODE_DIR, fileName, 'mono')
    clean(out)

    if isMono(path):
        LOG.info(f"{'[*]':<5}Start mono Decode: {fileName}")

        csharppath = searchFile(Join(path, r'assets\bin\Data\Managed'), CSHARP_FILE)

        cmd = f"{JUST_DECOMPILE_PATH} /lang:csharp /out:{out} /target:{csharppath}"
        shell.runCommand(cmd)

        for name in FILTER_LIST:
            Delete(Join(out, name))

        LOG.info(f"{'[*]':<5}End mono Decode: {fileName}")

        return csharppath

    return None


def runDecodeil2cpp(path, fileName):
    out = Join(DECODE_DIR, fileName, 'il2cpp')
    clean(out)

    if isIl2cpp(path):
        LOG.info(f"{'[*]':<5}Start il2cpp Decode: {fileName}")

        libpath = searchFile(Join(path, 'lib'), IL2CPP_FILE)
        global_metadatapath = searchFile(Join(path, r'assets\bin\Data\Managed\Metadata'), GLOBAL_META)

        cmd = f"{IL2CPP_DUMPER_PATH} {libpath} {global_metadatapath} {out}"
        shell.runCommand(cmd)

        LOG.info(f"{'[*]':<5}End il2cpp Decode: {fileName}")

        return libpath

    return None
