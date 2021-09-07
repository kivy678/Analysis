#ifndef __ELFFORMAT_H__
#define __ELFFORMAT_H__

#include "common/module.h"
#include "common/common.cpp.h"

#include "elf.h"


#define ELFFORMAT_EXCEPTION(ret, ...) 	__EXCEPTION((ret), ElfFormatException, ##__VA_ARGS__)


struct Elf32_Dyn_Linker
{
	struct Elf32_Dyn 		 e32_dyn;
	struct Elf32_Dyn_Linker* nextPoint;
};


struct Elf32_Section_Linker
{
	struct Elf32_Shdr 		 	 e32_shdr;
	struct Elf32_Section_Linker* nextPoint;
};


struct Elf32_Sym_Linker
{
	struct Elf32_Sym 		 	 e32_sym;
	char*			 	 	 	 e32_sym_name;
	struct Elf32_Sym_Linker* 	 nextPoint;
};

struct Elf32_Rel_Linker
{
	struct Elf32_Rel 		 	 e32_rel;
	struct Elf32_Rel_Linker* 	 nextPoint;
};


struct Elf32_Rela_Linker
{
	struct Elf32_Rela 		 	 e32_rela;
	struct Elf32_Rela_Linker* 	 nextPoint;
};


struct Elf32_GotMap_Linker
{
	Elf32_Off 		 	 		e32_rela;
	char* 	 					dynsym;
	struct Elf32_GotMap_Linker* nextPoint;
};




#ifdef __cplusplus
extern "C"
{
#endif

	extern std::map<int, std::string> FILE_TYPE;
	extern std::map<int, std::string> OBJECT_FILE_CLASS;
	extern std::map<int, std::string> OS_ABI;
	extern std::map<int, std::string> MACHINE_ARCHITECTURES;

	extern std::map<int, std::string> PROGRAM_TYPE;
	extern std::map<int, std::string> PROGRAM_FLAG;

	extern std::map<int, std::string> SECTION_TYPE;

	extern std::map<int, std::string> DYNAMIC_TAG;
	extern std::map<int, std::string> DYNAMIC_ENTRY;

	extern std::map<int, std::string> SYMBOL_BINDING;
	extern std::map<int, std::string> SYMBOL_TYPES;

	extern std::map<int, std::string> R_386;
	extern std::map<int, std::string> R_X86_64;
	extern std::map<int, std::string> R_ARM;

#ifdef __cplusplus
}
#endif

#endif // __ELFFORMAT_H__
