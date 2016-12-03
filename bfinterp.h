#pragma once


#include <stdio.h>
#include <stdint.h>
#include <inttypes.h>  // allows printf of stdint types
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <ctype.h>


// #define DEBUG
#define LOGOK
#define NO_EXTENDED_ASCII  // comment to allow output of extended ASCII letters
// #define LOGOK fprintf(stderr, "OK:%s:%d\n", __FILE__, __LINE__);
// #define LOG_TOO_MUCH_OUTPUT
// #define LOG_TOO_MUCH_INSTRUCTION


void interpret_bf(
        char* source_code, char* input,
        char* output, const uint64_t output_size
);

#ifdef DEBUG
void print_source_code(
        char const * const source_code,
        char const* const p_src,
        const uint64_t source_code_size
);
#endif
