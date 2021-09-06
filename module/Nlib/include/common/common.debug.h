#ifndef __COMMON_COMMON_DEBUG_H__
#define __COMMON_COMMON_DEBUG_H__

static inline void
DBG_PRINT(FILE *out,
		const char *ident,
		const char *filename,
		const char *funcname,
		int lineno,
		const char *fmt,
		...)
{
	va_list arg;

	fprintf(out, "[DEBUG][%s][%s][%s][%d]\t",
			ident,
			filename,
			funcname,
			lineno);

	va_start(arg, fmt);
	vfprintf(out, fmt, arg);
	va_end(arg);
	fprintf(out, "\n");
}

#define DOPRINT(...) DBG_PRINT(stdout, "OUTPUT",  __FILE__, __func__, __LINE__, ##__VA_ARGS__)
#define DIPRINT(...) DBG_PRINT(stdout, "INFO",    __FILE__, __func__, __LINE__, ##__VA_ARGS__)
#define DEPRINT(...) DBG_PRINT(stderr, "ERROR",   __FILE__, __func__, __LINE__, ##__VA_ARGS__)
#define DFPRINT(...) DBG_PRINT(stderr, "FAILED",  __FILE__, __func__, __LINE__, ##__VA_ARGS__)
#define DWPRINT(...) DBG_PRINT(stderr, "WARNING", __FILE__, __func__, __LINE__, ##__VA_ARGS__)

#define DCHECK()     DBG_PRINT(stdout, "CHECK", __FILE__, __func__, __LINE__, "CHECK")

#endif // __COMMON_COMMON_DEBUG_H__