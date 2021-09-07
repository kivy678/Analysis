#define PY_SSIZE_T_CLEAN

//////////////////////////////////////////////////////////////////////////////////

#include "elfformat.h"
#include "parser.h"
#include "getgot.h"
#include "heapfree.h"


#define ELFMAGIC_SIZE 					sizeof(ElfMagic)-1
#define HEADER_SIZE						500
#define PROGRAM_SIZE					3000
#define SECTION_SIZE					3000
#define DYNAMIC_SIZE					3000
#define SYMTAB_SIZE						5000000
#define REL_SIZE						5000000
#define GOT_SIZE						5000000


//////////////////////////////////////////////////////////////////////////////////

PyObject* ElfFormatException = NULL;

//////////////////////////////////////////////////////////////////////////////////


static PyObject *
GetGot(PyObject* self, PyObject* a_args)
{

	//////////////////////////////////////////////////////////////////////////////////

	PyObject* 		returnString = NULL;
	FILE* 			pstRStream 	= NULL;
	unsigned char* 	pchBuffer	= NULL;

	const char* 	args		= NULL;

	Elf32_Off GOT_Offset = 0;

	struct Elf32_Ehdr 				e32_ehdr 			= {0};
	struct Elf32_Section_Linker* 	e32_section_linker 	= NULL;
	struct Elf32_Dyn_Linker* 		e32_dyn_linker 		= NULL;
	struct Elf32_Sym_Linker* 		e32_dsym_linker 	= NULL;
	struct Elf32_Rel_Linker* 		e32_relp_linker 	= NULL;
	struct Elf32_GotMap_Linker* 	e32_gotmap_linker 	= NULL;


	char*	pchEhrBuffer 	= (char*) malloc(sizeof(char) * HEADER_SIZE);
	char*	pchShrBuffer 	= (char*) malloc(sizeof(char) * SECTION_SIZE);
	char*	pchDynBuffer 	= (char*) malloc(sizeof(char) * DYNAMIC_SIZE);
	char*	pchDsymBuffer 	= (char*) malloc(sizeof(char) * SYMTAB_SIZE);
	char*	pchRelpBuffer 	= (char*) malloc(sizeof(char) * REL_SIZE);
	char*	pchGotBuffer 	= (char*) malloc(sizeof(char) * GOT_SIZE);


	memset(pchEhrBuffer, 0, sizeof(char) * HEADER_SIZE);
	memset(pchShrBuffer, 0, sizeof(char) * SECTION_SIZE);
	memset(pchDynBuffer, 0, sizeof(char) * DYNAMIC_SIZE);
	memset(pchDsymBuffer, 0, sizeof(char) * SYMTAB_SIZE);
	memset(pchRelpBuffer, 0, sizeof(char) * REL_SIZE);
	memset(pchGotBuffer, 0, sizeof(char) * GOT_SIZE);


	e32_section_linker = (struct Elf32_Section_Linker*) malloc(sizeof(struct Elf32_Section_Linker));
	memset(e32_section_linker, 0, sizeof(struct Elf32_Section_Linker));

	e32_dyn_linker = (struct Elf32_Dyn_Linker*) malloc(sizeof(struct Elf32_Dyn_Linker));
	memset(e32_dyn_linker, 0, sizeof(struct Elf32_Dyn_Linker));

	e32_dsym_linker = (struct Elf32_Sym_Linker*) malloc(sizeof(struct Elf32_Sym_Linker));
	memset(e32_dsym_linker, 0, sizeof(struct Elf32_Sym_Linker));

	e32_relp_linker = (struct Elf32_Rel_Linker*) malloc(sizeof(struct Elf32_Rel_Linker));
	memset(e32_relp_linker, 0, sizeof(struct Elf32_Rel_Linker));

	e32_gotmap_linker = (struct Elf32_GotMap_Linker*) malloc(sizeof(struct Elf32_GotMap_Linker));
	memset(e32_gotmap_linker, 0, sizeof(struct Elf32_GotMap_Linker));


	//////////////////////////////////////////////////////////////////////////////////

	if(!PyArg_ParseTuple(a_args, "s", &args))
	{
		ELFFORMAT_EXCEPTION(-1, "ARGS PASS FAILED!!!\n");
		return NULL;
	}
	else
	{
		pstRStream 	= fopen(args, "rb");
	}

	//////////////////////////////////////////////////////////////////////////////////

	if(pstRStream != NULL)
	{
		fseek(pstRStream, 0, SEEK_END);
		long nBytes = ftell(pstRStream);

		pchBuffer 	= (unsigned char*) malloc(sizeof(unsigned char) * nBytes);

		fseek(pstRStream, 0, SEEK_SET);
		fread(pchBuffer, sizeof(unsigned char), nBytes, pstRStream);

		fclose(pstRStream);
	}
	else
	{
		ELFFORMAT_EXCEPTION(-1, "FILE OPEN FAILED!!!\n");

		free(pchBuffer);

		return 0;
	}

	//////////////////////////////////////////////////////////////////////////////////

	EhrParser(pchBuffer, &e32_ehdr, pchEhrBuffer);

	ShrParser(pchBuffer, &e32_ehdr, e32_section_linker, pchShrBuffer);
	DynParser(pchBuffer, &e32_ehdr, e32_dyn_linker, pchDynBuffer);
	SymParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_dsym_linker, pchDsymBuffer, ".dynsym");
	RelParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_dsym_linker, e32_relp_linker, pchRelpBuffer, ".rel.plt");


	if ((GOT_Offset = GetGotOffset(e32_dyn_linker)) != 0)
	{
		GetLibraryOffset(pchBuffer,
						 GOT_Offset,
						 GetGotSize(e32_section_linker, GOT_Offset),
						 e32_dsym_linker,
						 e32_relp_linker,
						 e32_gotmap_linker,
						 pchGotBuffer);
	};

	//////////////////////////////////////////////////////////////////////////////////

	returnString =  Py_BuildValue("s", pchGotBuffer);

	GotHeapFree(pchBuffer,
				 pchEhrBuffer,
				 pchShrBuffer,
				 pchDynBuffer,
				 pchDsymBuffer,
				 pchRelpBuffer,
				 pchGotBuffer,
				 e32_section_linker,
				 e32_dyn_linker,
				 e32_dsym_linker,
				 e32_relp_linker,
				 e32_gotmap_linker);


	return returnString;

}


static PyObject *
parser(PyObject* self, PyObject* a_args)
{

	//////////////////////////////////////////////////////////////////////////////////

	PyObject* 		returnString = NULL;
	FILE* 			pstRStream 	= NULL;
	unsigned char* 	pchBuffer	= NULL;

	const char* 	args		= NULL;
	const char*		option		= NULL;
	const char*		option2		= NULL;

	struct Elf32_Ehdr 				e32_ehdr 			= {0};
	struct Elf32_Phdr 				e32_phdr 			= {0};
	struct Elf32_Section_Linker* 	e32_section_linker 	= NULL;
	struct Elf32_Dyn_Linker* 		e32_dyn_linker 		= NULL;
	struct Elf32_Sym_Linker* 		e32_sym_linker 		= NULL;
	struct Elf32_Sym_Linker* 		e32_dsym_linker 	= NULL;
	struct Elf32_Rel_Linker* 		e32_rel_linker 		= NULL;
	struct Elf32_Rel_Linker* 		e32_relp_linker 	= NULL;


	char*	pchEhrBuffer 	= (char*) malloc(sizeof(char) * HEADER_SIZE);
	char*	pchPhrBuffer 	= (char*) malloc(sizeof(char) * PROGRAM_SIZE);
	char*	pchShrBuffer 	= (char*) malloc(sizeof(char) * SECTION_SIZE);
	char*	pchDynBuffer 	= (char*) malloc(sizeof(char) * DYNAMIC_SIZE);
	char*	pchSymBuffer 	= (char*) malloc(sizeof(char) * SYMTAB_SIZE);
	char*	pchDsymBuffer 	= (char*) malloc(sizeof(char) * SYMTAB_SIZE);
	char*	pchRelBuffer 	= (char*) malloc(sizeof(char) * REL_SIZE);
	char*	pchRelpBuffer 	= (char*) malloc(sizeof(char) * REL_SIZE);


	memset(pchEhrBuffer, 0, sizeof(char) * HEADER_SIZE);
	memset(pchPhrBuffer, 0, sizeof(char) * PROGRAM_SIZE);
	memset(pchShrBuffer, 0, sizeof(char) * SECTION_SIZE);
	memset(pchDynBuffer, 0, sizeof(char) * DYNAMIC_SIZE);
	memset(pchSymBuffer, 0, sizeof(char) * SYMTAB_SIZE);
	memset(pchDsymBuffer, 0, sizeof(char) * SYMTAB_SIZE);
	memset(pchRelBuffer, 0, sizeof(char) * REL_SIZE);
	memset(pchRelpBuffer, 0, sizeof(char) * REL_SIZE);


	e32_section_linker = (struct Elf32_Section_Linker*) malloc(sizeof(struct Elf32_Section_Linker));
	memset(e32_section_linker, 0, sizeof(struct Elf32_Section_Linker));

	e32_dyn_linker = (struct Elf32_Dyn_Linker*) malloc(sizeof(struct Elf32_Dyn_Linker));
	memset(e32_dyn_linker, 0, sizeof(struct Elf32_Dyn_Linker));

	e32_sym_linker = (struct Elf32_Sym_Linker*) malloc(sizeof(struct Elf32_Sym_Linker));
	memset(e32_sym_linker, 0, sizeof(struct Elf32_Sym_Linker));

	e32_dsym_linker = (struct Elf32_Sym_Linker*) malloc(sizeof(struct Elf32_Sym_Linker));
	memset(e32_dsym_linker, 0, sizeof(struct Elf32_Sym_Linker));

	e32_rel_linker = (struct Elf32_Rel_Linker*) malloc(sizeof(struct Elf32_Rel_Linker));
	memset(e32_rel_linker, 0, sizeof(struct Elf32_Rel_Linker));

	e32_relp_linker = (struct Elf32_Rel_Linker*) malloc(sizeof(struct Elf32_Rel_Linker));
	memset(e32_relp_linker, 0, sizeof(struct Elf32_Rel_Linker));


	//////////////////////////////////////////////////////////////////////////////////

	if(!PyArg_ParseTuple(a_args, "sss", &args, &option, &option2))
	{
		ELFFORMAT_EXCEPTION(-1, "ARGS PASS FAILED!!!\n");
		return NULL;
	}
	else
	{
		pstRStream 	= fopen(args, "rb");
	}

	//////////////////////////////////////////////////////////////////////////////////

	if(pstRStream != NULL)
	{
		fseek(pstRStream, 0, SEEK_END);
		long nBytes = ftell(pstRStream);

		pchBuffer 	= (unsigned char*) malloc(sizeof(unsigned char) * nBytes);

		fseek(pstRStream, 0, SEEK_SET);
		fread(pchBuffer, sizeof(unsigned char), nBytes, pstRStream);

		fclose(pstRStream);
	}
	else
	{
		ELFFORMAT_EXCEPTION(-1, "FILE OPEN FAILED!!!\n");

		free(pchBuffer);

		return 0;
	}

	//////////////////////////////////////////////////////////////////////////////////

	EhrParser(pchBuffer, &e32_ehdr, pchEhrBuffer);
	PhrParser(pchBuffer, &e32_ehdr, &e32_phdr, pchPhrBuffer);

	if ((strcmp(OBJECT_FILE_CLASS[e32_ehdr.getFileClass()].c_str(), "ELF32") == 0) &&
		(strcmp(option2, "f") == 0))
	{
		ShrParser(pchBuffer, &e32_ehdr, e32_section_linker, pchShrBuffer);
		DynParser(pchBuffer, &e32_ehdr, e32_dyn_linker, pchDynBuffer);
		SymParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_sym_linker, pchSymBuffer, ".symtab");
		SymParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_dsym_linker, pchDsymBuffer, ".dynsym");
		//RelParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_dsym_linker, e32_rel_linker, pchRelBuffer, ".rel.dyn");		// Size over flow
		RelParser(pchBuffer, &e32_ehdr, e32_section_linker, e32_dsym_linker, e32_relp_linker, pchRelpBuffer, ".rel.plt");
	}


	//////////////////////////////////////////////////////////////////////////////////

	if (strcmp(option, "h") == 0)
		returnString = Py_BuildValue("s", pchEhrBuffer);

	else if (strcmp(OBJECT_FILE_CLASS[e32_ehdr.getFileClass()].c_str(), "ELF64") == 0)
		returnString = Py_BuildValue("s", pchEhrBuffer);

	else if (strcmp(option, "p") == 0)
		returnString = Py_BuildValue("s", pchPhrBuffer);

	else if (strcmp(option, "s") == 0)
		returnString = Py_BuildValue("s", pchShrBuffer);

	else if (strcmp(option, "d") == 0)
		returnString = Py_BuildValue("s", pchDynBuffer);

	else if (strcmp(option, "S") == 0)
		returnString = Py_BuildValue("s", pchSymBuffer);

	else if (strcmp(option, "dS") == 0)
		returnString = Py_BuildValue("s", pchDsymBuffer);

	else if (strcmp(option, "r") == 0)
		returnString = Py_BuildValue("s", pchRelBuffer);

	else if (strcmp(option, "rp") == 0)
		returnString = Py_BuildValue("s", pchRelpBuffer);

	else
		returnString = Py_BuildValue("sss", pchEhrBuffer, pchPhrBuffer, pchShrBuffer);


	HeapFree(pchBuffer,
			 pchEhrBuffer,
			 pchPhrBuffer,
			 pchShrBuffer,
			 pchDynBuffer,
			 pchSymBuffer,
			 pchDsymBuffer,
			 pchRelBuffer,
			 pchRelpBuffer,
			 e32_section_linker,
			 e32_dyn_linker,
			 e32_sym_linker,
			 e32_dsym_linker,
			 e32_rel_linker,
			 e32_relp_linker);


	return returnString;

}


//////////////////////////////////////////////////////////////////////////////////

static PyMethodDef ElfFormatMethods[] = {
	{"parser", parser, METH_VARARGS, "ELF Parser"},
	{"GetGot", GetGot, METH_VARARGS, "Get Got And Reloc"},
	{NULL, NULL, 0, NULL}
};


static struct PyModuleDef elfformatmodule = {
	PyModuleDef_HEAD_INIT,
	"elfformat",
	NULL,
	-1,
	ElfFormatMethods
};

PyMODINIT_FUNC
PyInit_elfformat(void)
{
	PyObject* m = NULL;


	if(NULL == (m = PyModule_Create(&elfformatmodule)))
	{
		DEPRINT("ElfFormatException Module Exception");
		return NULL;
	}

	if (NULL == (ElfFormatException = PyErr_NewException("ElfFormatException.Exception",
													PyExc_Exception,
													NULL)))
	{
		DEPRINT("NewException");
		return NULL;
	}

	Py_INCREF(ElfFormatException);

	if (PyModule_AddObject(m, "ElfFormatException", ElfFormatException) < 0)
	{
		Py_DECREF(ElfFormatException);
		Py_CLEAR(ElfFormatException);
		Py_DECREF(m);

		return NULL;
	}

	return m;
}

//////////////////////////////////////////////////////////////////////////////////
