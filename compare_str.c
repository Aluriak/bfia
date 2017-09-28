
#include <string.h>
#include <stdint.h>
#include <inttypes.h>  // allows printf of stdint types
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include <limits.h>

/* #define DEBUG */
#define PENALTY_VALUE UINT8_MAX

/*
 * Naming conventions:
 *
 *  - aligned: perform alignment ; eliminate bias du to non valid leading chars.
 *  - letter dist: use distance between letters, non only a boolean equality
 */
uint64_t unaligned_letter_dist(
        char*, char*, const uint64_t, const uint64_t,
        const uint64_t, const int, const int
);


// Entry point of the module
// return the distance
uint64_t distance(char* found, char* expected, const uint64_t found_len,
                    const uint64_t expected_len, const uint64_t length_penalty,
                    const int apply_length_penaly,
                    const int apply_penalty_for_missing_letters) {
    return unaligned_letter_dist(
            found, expected, found_len, expected_len,
            length_penalty, apply_length_penaly,
            apply_penalty_for_missing_letters
    );
}


uint64_t unaligned_letter_dist(char* first, char* secnd, const uint64_t first_len,
                               const uint64_t secnd_len,
                               const uint64_t length_penalty,
                               const int apply_length_penalty,
                               const int apply_penalty_for_missing_letters) {
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

    // Decrease distance for each supplementary/missing character
    assert(max_size >= min_size);
    uint64_t penalty = 0;
    if(apply_length_penalty) {
        penalty = length_penalty * (max_size - min_size);
        if(max_size != min_size) {
            assert(max_size > min_size);
            assert(penalty > 0);
        }
    }
    if(apply_penalty_for_missing_letters) {
        char* longer = first_len > secnd_len ? first : secnd;
        for(uint64_t i = min_size; i < max_size; i++) {
            penalty += longer[i];
        }
    }
    /* printf("PENALTY: %" PRIu64 "\n", penalty); */
    distance += penalty;

    return distance;
}
