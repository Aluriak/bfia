#include "bfinterp.h"


const uint64_t MEMORY_SIZE = 2048;
const uint64_t MAXIMAL_MATCH_NUMBER = 512*2;
const uint64_t MAXIMAL_INSTRUCTION_EXECUTION = 2048*2048*8;


char* get_matching_bracket(char const* position, char*** opening, char*** closing, uint64_t nb_match) {
    LOGOK
    for(uint64_t i = 0; i < nb_match; i++) {
        LOGOK
        if((*opening)[i] == position) {
            LOGOK
            return (*closing)[i];
        }
    }
    LOGOK
    return NULL;  // no matching char
}

// return number of matching structure
uint64_t get_matching_structs(char* source_code, uint64_t source_code_size, char*** opening, char*** closing) {
    LOGOK
    uint64_t cur_struct = 0;
    *opening = (char**)malloc(MAXIMAL_MATCH_NUMBER * sizeof(char*));
    *closing = (char**)malloc(MAXIMAL_MATCH_NUMBER * sizeof(char*));
    if(opening == NULL) {
        fprintf(stderr, "Malloc of opening brackets container failed.\n");
        exit(1);
    }
    if(closing == NULL) {
        fprintf(stderr, "Malloc of opening brackets container failed.\n");
        exit(1);
    }
    char** stack = (char**)malloc(MAXIMAL_MATCH_NUMBER * sizeof(char*));
    char** p_stack = stack;
    for(uint64_t i = 0 ; i < MAXIMAL_MATCH_NUMBER; i++) {
        (*opening)[i] = NULL;
        (*closing)[i] = NULL;
    }
    LOGOK
    for(uint64_t i = 0 ; i < source_code_size; i++) {
        switch (source_code[i]) {
            case '[':
                (*p_stack) = &source_code[i];
                ++p_stack;
                break;
            case ']':
                if(p_stack == stack) {  // nothing on stack
                    (*opening)[cur_struct] = NULL;
                } else {  // regular case: something on stack
                    --p_stack;
                    (*opening)[cur_struct] = *p_stack;
                }
                (*closing)[cur_struct] = &source_code[i];
                ++cur_struct;
                break;
        }
    }
    LOGOK
    while(p_stack > stack) {
        (*opening)[cur_struct] = *p_stack;
        (*closing)[cur_struct] = NULL;
        ++cur_struct;
        --p_stack;
    }
    LOGOK
    return cur_struct;
}


void interpret_bf(char* source_code, char* input, char* output, const uint64_t output_size) {

    uint64_t instruction_count = 0;  // incremented at each instruction
    const uint64_t SOURCE_SIZE = strlen(source_code);
    const uint64_t INPUT_SIZE = strlen(input);
    uint8_t memory[MEMORY_SIZE];
    for(uint64_t i = 0 ; i < MEMORY_SIZE ; i++) { memory[i] = 0; }
    uint8_t* p_mem = memory;
    char const* p_src = source_code;
    char const* p_input = input;
    char* p_output = output;

    // Get matching brackets
    char** openings;
    char** closings;
    uint64_t nb_match = get_matching_structs(source_code, SOURCE_SIZE, &openings, &closings);

#ifdef DEBUG
    printf("%d matches = {", (int)nb_match);
    for(uint64_t i = 0; i < nb_match ; i++) {
        printf("\t%p -> %p\n", openings[i], closings[i]);
    }
    printf("}\n");
#endif

    while(p_src != NULL && p_src < &source_code[SOURCE_SIZE] && instruction_count < MAXIMAL_INSTRUCTION_EXECUTION) {
        LOGOK
        const char statement = *p_src;
        //printf("%c %i\n", statement, (int)statement);
        switch(statement) {
            case '>':
                // avoid going beyond memory
                p_mem < &memory[MEMORY_SIZE-1] ? ++p_mem : NULL ;
                ++p_src;
                break;
            case '<':
                // avoid going before memory
                p_mem > memory ? --p_mem : NULL ;
                ++p_src;
                break;
            case '+':
                ++(*p_mem);
                ++p_src;
                break;
            case '-':
                --(*p_mem);
                ++p_src;
                break;
            case ',':
                LOGOK
                if(p_input < &input[INPUT_SIZE]) {
                    *p_mem = *p_input;
                    ++p_input;
                } else {
                    *p_mem = '\0';
                }
                ++p_src;
                break;
            case '.':
#ifdef NO_EXTENDED_ASCII
                // The modulo 128 is here to prevent output of extended
                //  ascii letters, that are encoded on two bytes and
                //  that have an ascii number > 128.
                *p_output = (*p_mem) % 128;
#else
                *p_output = *p_mem;
#endif
                ++p_output;
                ++p_src;
                if(p_output >= &output[output_size-1]) {
#ifdef LOG_TOO_MUCH_OUTPUT
                    fprintf(stderr, "ERROR: too much output. End.\n");
#endif
                    return;
                }
                break;
#ifdef EXT_SET_ZERO
            case '0':  // replaces [-]
                *p_mem = 0;
                ++p_src;
                break;
#endif
            case '[':
                LOGOK
                if(!*p_mem) {
                    LOGOK
                    p_src = get_matching_bracket(
                        p_src,
                        &openings,
                        &closings,
                        nb_match
                    );
                    LOGOK
                    // go directly to next instruction, not to matching bracket
                    if(p_src != NULL) ++p_src;
                    LOGOK
                } else {
                    LOGOK
                    ++p_src;
                }
                LOGOK
                break;
            case ']':
                LOGOK
                if(*p_mem) {
                    LOGOK
                    p_src = get_matching_bracket(
                        p_src,
                        &closings,  // revert the search
                        &openings,
                        nb_match
                    );
                    // go directly to next instruction, not to matching bracket
                    if(p_src != NULL) ++p_src;
                } else {
                    ++p_src;
                }
                break;
            case '!':
                LOGOK
                printf("BREAKPOINT\n|");
                for(uint8_t* i = p_mem-10 >= memory ? p_mem-10 : memory ; i <= p_mem+10; i++) {
                    printf(" %i ", (int)*i);
                }
                printf("|\n|");
                for(uint8_t* i = p_mem-10 >= memory ? p_mem-10 : memory ; i <= p_mem+10; i++) {
                    if(isalnum(*i)) {
                        printf(" %c ", *i);
                    } else {
                        printf(" _ ");
                    }
                }
                printf("|\n");
                for(uint8_t* i = p_mem-10 >= memory ? p_mem-10 : memory ; i < p_mem ; i++) {
                    printf("   ");
                }
                printf("  ^\n");
                getchar();
                ++p_src;
                break;
            default:
                ++p_src;
#ifdef DEBUG
                fprintf(stderr, "ERROR: Non valid character '%c' found in source code. Exit.\n", *p_src);
                //exit(1);
#endif
        } // end switch
        LOGOK
#ifdef DEBUG
        printf("END: Now at %i\n", (int)(p_src - source_code));
        print_source_code(source_code, p_src, SOURCE_SIZE);
#endif
        ++instruction_count;
    } // end while
#ifdef LOG_TOO_MUCH_INSTRUCTION
    if(instruction_count >= MAXIMAL_INSTRUCTION_EXECUTION) {
        fprintf(stderr, "ERROR: too much instructions (Maximal of %" PRIu64 " reached).\n", MAXIMAL_INSTRUCTION_EXECUTION);
    }
#endif
    return;
}


#ifdef DEBUG
void print_source_code(char const * const source_code, char const* const p_src, const uint64_t source_code_size) {
    printf("SOURCE CODE\n");
    char* i = (char*)((p_src-10 >= source_code) ? p_src-10 : source_code);
    for(; i <= p_src+10 && (int)(i - source_code) <= source_code_size; i++) {
        printf("%c", *i);
    }
    printf("\n");
    i = (char*)((p_src-10 >= source_code) ? p_src-10 : source_code);
    for(; i < p_src && (int)(i - source_code) <= source_code_size ; i++) {
        printf(" ");
    }
    printf("^\n");
}
#endif

