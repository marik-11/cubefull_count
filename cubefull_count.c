#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

typedef unsigned __int128 u128;
typedef __int128 i128;

#define TABLE_SIZE 20000000u

static uint32_t *pair_table;

static int power_exceeds(u128 r, int k, u128 n)
{
    u128 acc = 1;
    for (int i = 0; i < k; i++) {
        if (acc > n / r)
            return 1;
        acc *= r;
    }
    return 0;
}

static u128 iroot(u128 n, int k)
{
    if (n < 2)
        return n;
    u128 r = (u128)powl((long double)n, 1.0L / k);
    while (r > 0 && power_exceeds(r, k, n))
        r--;
    while (!power_exceeds(r + 1, k, n))
        r++;
    return r;
}

static u128 pow_u(u128 b, int e)
{
    u128 r = 1;
    while (e--)
        r *= b;
    return r;
}

static u128 pair_count(u128 z)
{
    if (z < 1)
        return 0;
    if (z <= TABLE_SIZE)
        return pair_table[(uint32_t)z];
    u128 a_max = iroot(z, 7);
    u128 total = 0;
    for (u128 a = 1; a <= a_max; a++) {
        u128 a3 = a * a * a;
        total += iroot(z / a3, 4);
        total += iroot(z / (a3 * a), 3);
    }
    return total - a_max * a_max;
}

static u128 triple_count(u128 y)
{
    u128 c_max = iroot(y, 5);
    u128 total = 0;
    for (u128 c = 1; c <= c_max; c++) {
        u128 c5 = c * c * c * c * c;
        total += pair_count(y / c5);
    }
    return total;
}

typedef struct {
    u128 r;
    int w;
} term_t;

static term_t *terms;
static size_t nterms, cap_terms;
static uint32_t *primes;
static size_t nprimes;
static u128 limit;

static void push(u128 r, int w)
{
    if (nterms == cap_terms) {
        cap_terms = cap_terms ? cap_terms * 2 : 1024;
        terms = realloc(terms, cap_terms * sizeof(term_t));
    }
    terms[nterms].r = r;
    terms[nterms].w = w;
    nterms++;
}

static void walk(size_t start, u128 t, int w)
{
    static const int exps[5] = {8, 9, 10, 13, 14};
    static const int coef[5] = {-1, -1, -1, 1, 1};
    for (size_t k = start; k < nprimes; k++) {
        u128 p = primes[k];
        if (power_exceeds(p, 8, limit / t))
            break;
        for (int i = 0; i < 5; i++) {
            if (power_exceeds(p, exps[i], limit / t))
                break;
            u128 q = t * pow_u(p, exps[i]);
            push(q, w * coef[i]);
            walk(k + 1, q, w * coef[i]);
        }
    }
}

static void print_u128(u128 v)
{
    char buf[64];
    int len = 0;
    if (!v)
        buf[len++] = '0';
    while (v) {
        buf[len++] = '0' + (int)(v % 10);
        v /= 10;
    }
    while (len)
        putchar(buf[--len]);
}

static u128 parse(const char *s)
{
    u128 v = 0;
    for (; *s; s++)
        v = v * 10 + (u128)(*s - '0');
    return v;
}

int main(int argc, char **argv)
{
    if (argc < 2)
        return 1;
    limit = parse(argv[1]);
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);
    pair_table = calloc(TABLE_SIZE + 1, sizeof(uint32_t));
    for (uint64_t b = 1; b * b * b * b <= TABLE_SIZE; b++)
        for (uint64_t a = 1; a * a * a * b * b * b * b <= TABLE_SIZE; a++)
            pair_table[a * a * a * b * b * b * b]++;
    for (uint32_t i = 1; i <= TABLE_SIZE; i++)
        pair_table[i] += pair_table[i - 1];
    u128 root = iroot(limit, 8);
    char *comp = calloc((size_t)root + 2, 1);
    primes = malloc(((size_t)root + 2) * sizeof(uint32_t));
    for (uint64_t i = 2; i <= root; i++) {
        if (comp[i])
            continue;
        primes[nprimes++] = (uint32_t)i;
        for (uint64_t j = i * i; j <= root; j += i)
            comp[j] = 1;
    }
    push(1, 1);
    walk(0, 1, 1);
    i128 total = 0;
    for (size_t i = 0; i < nterms; i++)
        total += (i128)terms[i].w * (i128)triple_count(limit / terms[i].r);
    clock_gettime(CLOCK_MONOTONIC, &t1);
    print_u128((u128)total);
    printf(" time=%.3fs terms=%zu\n", (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec) * 1e-9, nterms);
    return 0;
}
