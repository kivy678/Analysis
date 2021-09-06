#ifndef __DISASM_H__
#define __DISASM_H__

#include "common/module.h"



#define DISASSEMBLE_EXCEPTION(ret, ...) 	__EXCEPTION((ret), DisassembleException, ##__VA_ARGS__)


#endif // __DISASM_H__
