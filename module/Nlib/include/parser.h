#ifndef __PARSER_H__
#define __PARSER_H__


int EhrParser(unsigned char*, struct Elf32_Ehdr*, char*);
int PhrParser(unsigned char*, struct Elf32_Ehdr*, struct Elf32_Phdr*, char*);
int ShrParser(unsigned char*, struct Elf32_Ehdr*, struct Elf32_Section_Linker*, char*);
int DynParser(unsigned char*, struct Elf32_Ehdr*, struct Elf32_Dyn_Linker*, char*);
int SymParser(unsigned char*, struct Elf32_Ehdr*, struct Elf32_Section_Linker*, struct Elf32_Sym_Linker*, char*, char*);
int RelParser(unsigned char*, struct Elf32_Ehdr*, struct Elf32_Section_Linker*, struct Elf32_Sym_Linker*, struct Elf32_Rel_Linker*, char*, char*);

char* GetSetionName(unsigned char*, struct Elf32_Ehdr*, Elf32_Word);


#endif // __PARSER_H__
