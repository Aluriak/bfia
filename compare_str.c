
#include <string.h>
#include <stdint.h>
#include <inttypes.h>  // allows printf of stdint types
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include <limits.h>

/* #define DEBUG */
#define ZIP_LONGEST  // ifdef, additionnal characters will be counted
#define PENALTY_VALUE UINT8_MAX

/*
 * Naming conventions:
 *
 *  - aligned: perform alignment ; eliminate bias du to non valid leading chars.
 *  - letter dist: use distance between letters, non only a boolean equality
 */
uint64_t unaligned_letter_dist(char*, char*, const uint64_t, const uint64_t);


// Entry point of the module
// return the distance
uint64_t distance(char* found, char* expected, const uint64_t found_len,
                    const uint64_t expected_len) {
    return unaligned_letter_dist(found, expected, found_len, expected_len);
}


uint64_t unaligned_letter_dist(char* first, char* secnd, const uint64_t first_len,
                               const uint64_t secnd_len) {
    const uint64_t min_size = first_len < secnd_len ? first_len : secnd_len;
    const uint64_t max_size = first_len > secnd_len ? first_len : secnd_len;
    assert(UINT8_MAX == 255);
#ifdef DEBUG
    printf("######################\n");
    printf("FIRSTLEN: %" PRIu64 "\n", first_len);
    printf("SECNDLEN: %" PRIu64 "\n", secnd_len);
#endif

    uint64_t distance = 0;  // returned

    for(uint64_t i = 0; i < min_size; i++) {
        int8_t one = (int8_t)(first[i] % (INT8_MAX + 1));
        int8_t two = (int8_t)(secnd[i] % (INT8_MAX + 1));
        int64_t diff = one - two;
        distance += (uint64_t)(fabs(diff)) % (INT8_MAX + 1);
#ifdef DEBUG
        printf("DISTANCE: %" PRIu64 "\n", distance);
#endif
    }

#ifdef ZIP_LONGEST
    // Decrease distance for each supplementary/missing character
    assert(max_size >= min_size);
    uint64_t penalty = 0;
#ifdef PENALTY_VALUE
    penalty = PENALTY_VALUE * (max_size - min_size);
    if(max_size != min_size) {
        assert(max_size > min_size);
        assert(penalty > 0);
    }
#else
    char* longer = first_len > secnd_len ? first : secnd;
    for(uint64_t i = min_size; i < max_size; i++) {
        penalty += longer[i];
    }
#endif
    /* printf("PENALTY: %" PRIu64 "\n", penalty); */
    distance += penalty;
#endif

    return distance;
}
