#define PY_SSIZE_T_CLEAN

//////////////////////////////////////////////////////////////////////////////////

#include "elfformat.h"

//////////////////////////////////////////////////////////////////////////////////


int GotHeapFree(unsigned char* pchBuffer,
				 char* pchEhrBuffer,
				 char* pchShrBuffer,
				 char* pchDynBuffer,
				 char* pchDsymBuffer,
				 char* pchRelpBuffer,
				 char* pchGotBuffer,
				 struct Elf32_Section_Linker* 	e32_section_linker,
				 struct Elf32_Dyn_Linker* 		e32_dyn_linker,
				 struct Elf32_Sym_Linker* 		e32_dsym_linker,
				 struct Elf32_Rel_Linker* 		e32_relp_linker,
				 struct Elf32_GotMap_Linker* 	e32_gotmap_linker)
{

	//////////////////////////////////////////////////////////////////////////////////

	struct Elf32_Section_Linker* 	NextNode1 = NULL;
	struct Elf32_Dyn_Linker* 		NextNode2 = NULL;
	struct Elf32_Sym_Linker* 		NextNode3 = NULL;
	struct Elf32_Rel_Linker* 		NextNode4 = NULL;
	struct Elf32_GotMap_Linker* 	NextNode5 = NULL;

	//////////////////////////////////////////////////////////////////////////////////

	free(pchBuffer);

	free(pchEhrBuffer);
	free(pchShrBuffer);
	free(pchDynBuffer);
	free(pchDsymBuffer);
	free(pchRelpBuffer);
	free(pchGotBuffer);

	//////////////////////////////////////////////////////////////////////////////////

		
	while(e32_section_linker->nextPoint != NULL)
	{
		NextNode1 = e32_section_linker->nextPoint;
		free(e32_section_linker);

		e32_section_linker = NextNode1;
	}
	free(e32_section_linker);


	while(e32_dyn_linker->nextPoint != NULL)
	{
		NextNode2 = e32_dyn_linker->nextPoint;
		free(e32_dyn_linker);

		e32_dyn_linker = NextNode2;
	}
	free(e32_dyn_linker);


	while(e32_dsym_linker->nextPoint != NULL)
	{
		NextNode3 = e32_dsym_linker->nextPoint;
		free(e32_dsym_linker);

		e32_dsym_linker = NextNode3;
	}
	free(e32_dsym_linker);

	while(e32_relp_linker->nextPoint != NULL)
	{
		NextNode4 = e32_relp_linker->nextPoint;
		free(e32_relp_linker);

		e32_relp_linker = NextNode4;
	}
	free(e32_relp_linker);

	while(e32_gotmap_linker->nextPoint != NULL)
	{
		NextNode5 = e32_gotmap_linker->nextPoint;
		free(e32_gotmap_linker);

		e32_gotmap_linker = NextNode5;
	}
	free(e32_gotmap_linker);


	//////////////////////////////////////////////////////////////////////////////////


	return 0;
}


int HeapFree(unsigned char* pchBuffer,
			 char* pchEhrBuffer,
			 char* pchPhrBuffer,
			 char* pchShrBuffer,
			 char* pchDynBuffer,
			 char* pchSymBuffer,
			 char* pchDsymBuffer,
			 char* pchRelBuffer,
			 char* pchRelpBuffer,
			 struct Elf32_Section_Linker* 	e32_section_linker,
			 struct Elf32_Dyn_Linker* 		e32_dyn_linker,
			 struct Elf32_Sym_Linker* 		e32_sym_linker,
			 struct Elf32_Sym_Linker* 		e32_dsym_linker,
			 struct Elf32_Rel_Linker* 		e32_rel_linker,
			 struct Elf32_Rel_Linker* 		e32_relp_linker)
{

	//////////////////////////////////////////////////////////////////////////////////

	struct Elf32_Section_Linker* 	NextNode1 = NULL;
	struct Elf32_Dyn_Linker* 		NextNode2 = NULL;
	struct Elf32_Sym_Linker* 		NextNode3 = NULL;
	struct Elf32_Rel_Linker* 		NextNode4 = NULL;

	//////////////////////////////////////////////////////////////////////////////////

	free(pchBuffer);

	free(pchEhrBuffer);
	free(pchPhrBuffer);
	free(pchShrBuffer);
	free(pchDynBuffer);
	free(pchSymBuffer);
	free(pchDsymBuffer);
	free(pchRelBuffer);
	free(pchRelpBuffer);

	//////////////////////////////////////////////////////////////////////////////////

		
	while(e32_section_linker->nextPoint != NULL)
	{
		NextNode1 = e32_section_linker->nextPoint;
		free(e32_section_linker);

		e32_section_linker = NextNode1;
	}
	free(e32_section_linker);


	while(e32_dyn_linker->nextPoint != NULL)
	{
		NextNode2 = e32_dyn_linker->nextPoint;
		free(e32_dyn_linker);

		e32_dyn_linker = NextNode2;
	}
	free(e32_dyn_linker);


	while(e32_sym_linker->nextPoint != NULL)
	{
		NextNode3 = e32_sym_linker->nextPoint;
		free(e32_sym_linker);

		e32_sym_linker = NextNode3;
	}
	free(e32_sym_linker);


	while(e32_dsym_linker->nextPoint != NULL)
	{
		NextNode3 = e32_dsym_linker->nextPoint;
		free(e32_dsym_linker);

		e32_dsym_linker = NextNode3;
	}
	free(e32_dsym_linker);


	while(e32_rel_linker->nextPoint != NULL)
	{
		NextNode4 = e32_rel_linker->nextPoint;
		free(e32_rel_linker);

		e32_rel_linker = NextNode4;
	}
	free(e32_rel_linker);


	while(e32_relp_linker->nextPoint != NULL)
	{
		NextNode4 = e32_relp_linker->nextPoint;
		free(e32_relp_linker);

		e32_relp_linker = NextNode4;
	}
	free(e32_relp_linker);


	//////////////////////////////////////////////////////////////////////////////////


	return 0;
}
