#ifndef __HEAPFREE_H__
#define __HEAPFREE_H__


int HeapFree(unsigned char*,
			 char*,
			 char*,
			 char*,
			 char*,
			 char*,
			 char*,
			 char*,
			 char*,
			 struct Elf32_Section_Linker*,
			 struct Elf32_Dyn_Linker*,
			 struct Elf32_Sym_Linker*,
			 struct Elf32_Sym_Linker*,
			 struct Elf32_Rel_Linker*,
			 struct Elf32_Rel_Linker*);

int GotHeapFree(unsigned char*,
			 char*,
			 char*,
			 char*,
			 char*,
			 char*,
			 char*,
			 struct Elf32_Section_Linker*,
			 struct Elf32_Dyn_Linker*,
			 struct Elf32_Sym_Linker*,
			 struct Elf32_Rel_Linker*,
			 struct Elf32_GotMap_Linker*);

#endif // __HEAPFREE_H__
