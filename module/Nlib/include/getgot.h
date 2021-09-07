#ifndef __GETGOT_H__
#define __GETGOT_H__


int GetLibraryOffset(unsigned char*,
					 Elf32_Off,
					 Elf32_Off,
					 struct Elf32_Sym_Linker*,
					 struct Elf32_Rel_Linker*,
					 struct Elf32_GotMap_Linker*,
					 char*);

Elf32_Off GetGotOffset(struct Elf32_Dyn_Linker*);
Elf32_Off GetGotSize(struct Elf32_Section_Linker*, Elf32_Off);


#endif // __GETGOT_H__
