# -*- coding:utf-8 -*-

from enum import Enum, unique, auto

@unique
class STATUS(Enum):
    INIT              = 'INIT'
    FILE_INIT         = 'FILE_INIT'
    ANALYSIS          = 'ANALYSIS'
    FAILED            = 'FAILED'




DEV_LIB_COLUMNS=[
    'model',
    'lib',
]

LIB_COLUMNS=[
    'func',
    'addr',
    'lib_fk',
]


UNITY_COLUMNS=[
    'fileName',
    'fileSize',
    'build',
    'parent',
    'status',
]

IL2CPP_COLUMNS=[
    'ref_id',
    'function',
    'offset',
    'opcode',
    'cmp_ref',
]

OPCDOE_COLUMNS=[
    'pkg',
    'func',
    'opcode',
    'binary',
    'engine',
    'arch',
]
