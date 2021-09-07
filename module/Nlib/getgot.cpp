#define PY_SSIZE_T_CLEAN

//////////////////////////////////////////////////////////////////////////////////

#include "elfformat.h"

#define TMP_STRING_SIZE					500

//////////////////////////////////////////////////////////////////////////////////


int GetLibraryOffset(unsigned char* 			pchBuffer,
					 Elf32_Off 					GOT_Offset,
					 Elf32_Off 					GOT_EndOffset,
					 struct Elf32_Sym_Linker* 	e32_sym_linker,
					 struct Elf32_Rel_Linker*	e32_rel_linker,
					 struct Elf32_GotMap_Linker* e32_gotmap_linker,
					 char*						pchGotBuffer)
{

	//////////////////////////////////////////////////////////////////////////////////

	int i 										= 0;
	Elf32_Word symbol_idx						= -1;

	GOT_Offset 									+= 12;
	int GOT_Size								= (GOT_EndOffset - GOT_Offset) / 4;


	struct Elf32_Rel_Linker* e32_rel_Node 		= e32_rel_linker;
	struct Elf32_Sym_Linker* e32_sym_Node 		= e32_sym_linker;

	unsigned int* LibraryAddress = (unsigned int*) (pchBuffer + GOT_Offset);


	struct Elf32_GotMap_Linker* e32_gotmap_Node = e32_gotmap_linker;
	struct Elf32_GotMap_Linker* e32_gotmap_NextNode = NULL;


	char* tmpStrBuffer					= (char*) malloc(sizeof(char) * TMP_STRING_SIZE);
	memset(tmpStrBuffer, 0, sizeof(char) * TMP_STRING_SIZE);

	//////////////////////////////////////////////////////////////////////////////////

	
	while (i < GOT_Size)
	{
		symbol_idx 		= e32_rel_Node->e32_rel.getSymbol();
		e32_sym_Node 	= e32_sym_linker;

		for (int j=0; j < symbol_idx; j++)
		{
			
			e32_sym_Node = e32_sym_Node->nextPoint;
		}

/*
		if (*LibraryAddress == 0)
		{
			break;
		}
*/

		//printf("%d: 0x%08x %s\n", i, *LibraryAddress, e32_sym_Node->e32_sym_name);

		//////////////////////////////////////////////////////////////////////////////////

		e32_gotmap_Node->e32_rela = *LibraryAddress;
		e32_gotmap_Node->dynsym = e32_sym_Node->e32_sym_name;

		sprintf(tmpStrBuffer, "0x%08x %s\n", e32_gotmap_Node->e32_rela, e32_gotmap_Node->dynsym);
		strcat(pchGotBuffer, tmpStrBuffer);


		e32_gotmap_NextNode = (struct Elf32_GotMap_Linker*) malloc(sizeof(struct Elf32_GotMap_Linker));
		memset(e32_gotmap_NextNode, 0, sizeof(struct Elf32_GotMap_Linker));
		e32_gotmap_Node->nextPoint = e32_gotmap_NextNode;

		e32_gotmap_Node = e32_gotmap_NextNode;

		//////////////////////////////////////////////////////////////////////////////////

		e32_rel_Node = e32_rel_Node->nextPoint;

		LibraryAddress += 1;
		i += 1;

	}


	//////////////////////////////////////////////////////////////////////////////////

	free(tmpStrBuffer);

	return 0;
}


Elf32_Off GetGotSize(struct Elf32_Section_Linker* 	e32_section_linker,
			   Elf32_Off 						GOT_Offset)
{

	struct Elf32_Section_Linker* e32_section_Node 	= e32_section_linker;

	Elf32_Off StartOffset = 0;
	int EndOffset = 0;


	while(e32_section_Node->nextPoint != NULL)
	{
		StartOffset = e32_section_Node->e32_shdr.sh_offset;
		EndOffset = StartOffset + e32_section_Node->e32_shdr.sh_size;

		if ( StartOffset <= GOT_Offset && EndOffset > GOT_Offset )
		{
			//printf("GOT EndOffset: 0x%08x\n", EndOffset);
			break;
		}
		
		e32_section_Node = e32_section_Node->nextPoint;
	}

	return EndOffset;
}


Elf32_Off GetGotOffset(struct Elf32_Dyn_Linker* e32_dyn_linker)
{

	struct Elf32_Dyn_Linker* e32_dyn_Node 	= e32_dyn_linker;
	Elf32_Off GOT_Offset 					= 0;


	while(e32_dyn_Node->nextPoint != NULL)
	{
		if (strcmp(DYNAMIC_TAG[e32_dyn_Node->e32_dyn.d_tag].c_str(), "PLTGOT") == 0)
		{
			GOT_Offset = e32_dyn_Node->e32_dyn.d_un.d_ptr - 0x1000;			// align: 0x1000
			break;
		}

		e32_dyn_Node = e32_dyn_Node->nextPoint;
	}

	//printf("GOT Offset: 0x%08x\n", GOT_Offset);

	return GOT_Offset;
}
