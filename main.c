#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "bfinterp.h"


const uint64_t MAXIMAL_SOURCE_CODE_SIZE = 2048*2048*16;


char* readFile(char* fileName) {
    LOGOK
    FILE *file = fopen(fileName, "r");
    char *code;
    size_t n = 0;
    int c;

    if (file == NULL)
        return NULL; // could not open file

    code = malloc(MAXIMAL_SOURCE_CODE_SIZE);

    while ((c = fgetc(file)) != EOF) {
        code[n++] = (char) c;
    }

    // don't forget to terminate with the null character
    code[n] = '\0';

    LOGOK
    return code;
}


int main(int argc, char *argv[]) {
    LOGOK
    if(argc < 2) {
        printf("usage: <source> [input].\n");
        exit(1);
    }
    LOGOK
    char* source_code = readFile(argv[1]);
    if(source_code == NULL) {
        printf("Given filename can't be read.\n");
        exit(1);
    }
    LOGOK
    char* output = malloc(MAXIMAL_SOURCE_CODE_SIZE);
    for(uint64_t i = 0; i < MAXIMAL_SOURCE_CODE_SIZE; i++) output[i] = '\0';
    if(output == NULL) {
        printf("Output can't be malloc'd.\n");
        exit(1);
    }
    char* input = "";
    if(argc > 2) {
        input = argv[2];
    }
    LOGOK
    interpret_bf(source_code, input, output, MAXIMAL_SOURCE_CODE_SIZE);
    LOGOK
    printf("%s\n", output);
    return 0;
}
