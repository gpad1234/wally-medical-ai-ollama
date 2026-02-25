/**
 * simple_db.c — Chained hash-table key-value store
 *
 * Design:
 *   - Open addressing via separate chaining (linked-list buckets)
 *   - FNV-1a 64-bit hash
 *   - Automatic resize at load factor > 0.75 (doubles capacity)
 *   - All keys and values are heap-allocated copies
 */

#include "simple_db.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* -------------------------------------------------------------------------
 * Internal structures
 * ---------------------------------------------------------------------- */

#define INITIAL_CAPACITY  64u
#define LOAD_FACTOR_MAX   0.75

typedef struct Entry {
    char        *key;
    char        *value;
    struct Entry *next;       /* chained collision list */
} Entry;

struct SimpleDB {
    Entry  **buckets;
    size_t   capacity;
    size_t   count;
};

/* -------------------------------------------------------------------------
 * FNV-1a 64-bit hash
 * ---------------------------------------------------------------------- */

static uint64_t fnv1a(const char *s)
{
    uint64_t hash  = UINT64_C(14695981039346656037);
    uint64_t prime = UINT64_C(1099511628211);
    while (*s) {
        hash ^= (uint8_t)(*s++);
        hash *= prime;
    }
    return hash;
}

static inline size_t bucket_index(uint64_t hash, size_t capacity)
{
    return (size_t)(hash & (uint64_t)(capacity - 1));
}

/* -------------------------------------------------------------------------
 * Helpers
 * ---------------------------------------------------------------------- */

static char *dup_str(const char *s)
{
    size_t n = strlen(s) + 1;
    char *d = malloc(n);
    if (d) memcpy(d, s, n);
    return d;
}

static void free_entries(Entry **buckets, size_t capacity)
{
    for (size_t i = 0; i < capacity; i++) {
        Entry *e = buckets[i];
        while (e) {
            Entry *next = e->next;
            free(e->key);
            free(e->value);
            free(e);
            e = next;
        }
    }
}

/* Resize: rehash all entries into a new bucket array of new_cap (must be power-of-2). */
static bool rehash(SimpleDB *db, size_t new_cap)
{
    Entry **new_buckets = calloc(new_cap, sizeof(Entry *));
    if (!new_buckets) return false;

    for (size_t i = 0; i < db->capacity; i++) {
        Entry *e = db->buckets[i];
        while (e) {
            Entry *next = e->next;
            size_t idx = bucket_index(fnv1a(e->key), new_cap);
            e->next = new_buckets[idx];
            new_buckets[idx] = e;
            e = next;
        }
    }

    free(db->buckets);
    db->buckets  = new_buckets;
    db->capacity = new_cap;
    return true;
}

/* -------------------------------------------------------------------------
 * Lifecycle
 * ---------------------------------------------------------------------- */

SimpleDB *db_create(void)
{
    SimpleDB *db = malloc(sizeof(SimpleDB));
    if (!db) return NULL;

    db->buckets = calloc(INITIAL_CAPACITY, sizeof(Entry *));
    if (!db->buckets) { free(db); return NULL; }

    db->capacity = INITIAL_CAPACITY;
    db->count    = 0;
    return db;
}

void db_destroy(SimpleDB *db)
{
    if (!db) return;
    free_entries(db->buckets, db->capacity);
    free(db->buckets);
    free(db);
}

/* -------------------------------------------------------------------------
 * CRUD
 * ---------------------------------------------------------------------- */

bool db_set(SimpleDB *db, const char *key, const char *value)
{
    if (!db || !key || !value) return false;

    /* Resize if load factor exceeded */
    if ((double)(db->count + 1) / (double)db->capacity > LOAD_FACTOR_MAX) {
        if (!rehash(db, db->capacity * 2)) return false;
    }

    uint64_t hash = fnv1a(key);
    size_t   idx  = bucket_index(hash, db->capacity);
    Entry   *e    = db->buckets[idx];

    /* Update existing entry */
    while (e) {
        if (strcmp(e->key, key) == 0) {
            char *new_val = dup_str(value);
            if (!new_val) return false;
            free(e->value);
            e->value = new_val;
            return true;
        }
        e = e->next;
    }

    /* Insert new entry at head of chain */
    Entry *ne = malloc(sizeof(Entry));
    if (!ne) return false;

    ne->key = dup_str(key);
    if (!ne->key) { free(ne); return false; }

    ne->value = dup_str(value);
    if (!ne->value) { free(ne->key); free(ne); return false; }

    ne->next          = db->buckets[idx];
    db->buckets[idx]  = ne;
    db->count++;
    return true;
}

const char *db_get(SimpleDB *db, const char *key)
{
    if (!db || !key) return NULL;

    size_t  idx = bucket_index(fnv1a(key), db->capacity);
    Entry  *e   = db->buckets[idx];

    while (e) {
        if (strcmp(e->key, key) == 0) return e->value;
        e = e->next;
    }
    return NULL;
}

bool db_delete(SimpleDB *db, const char *key)
{
    if (!db || !key) return false;

    size_t  idx  = bucket_index(fnv1a(key), db->capacity);
    Entry **prev = &db->buckets[idx];
    Entry  *e    = *prev;

    while (e) {
        if (strcmp(e->key, key) == 0) {
            *prev = e->next;
            free(e->key);
            free(e->value);
            free(e);
            db->count--;
            return true;
        }
        prev = &e->next;
        e    = e->next;
    }
    return false;
}

bool db_exists(SimpleDB *db, const char *key)
{
    return db_get(db, key) != NULL;
}

/* -------------------------------------------------------------------------
 * Utility
 * ---------------------------------------------------------------------- */

size_t db_count(SimpleDB *db)
{
    return db ? db->count : 0;
}

void db_clear(SimpleDB *db)
{
    if (!db) return;
    free_entries(db->buckets, db->capacity);
    memset(db->buckets, 0, db->capacity * sizeof(Entry *));
    db->count = 0;
}

char **db_keys(SimpleDB *db, size_t *out_count)
{
    if (!db || !out_count) return NULL;
    *out_count = 0;

    if (db->count == 0) return NULL;

    char **arr = malloc(db->count * sizeof(char *));
    if (!arr) return NULL;

    size_t pos = 0;
    for (size_t i = 0; i < db->capacity && pos < db->count; i++) {
        Entry *e = db->buckets[i];
        while (e) {
            arr[pos] = dup_str(e->key);
            if (!arr[pos]) {
                /* allocation failure: free what we have */
                for (size_t j = 0; j < pos; j++) free(arr[j]);
                free(arr);
                return NULL;
            }
            pos++;
            e = e->next;
        }
    }

    *out_count = pos;
    return arr;
}

DBStats db_stats(SimpleDB *db)
{
    DBStats s = {0, 0, 0, 0};
    if (!db) return s;

    s.total_entries = db->count;

    for (size_t i = 0; i < db->capacity; i++) {
        Entry  *e     = db->buckets[i];
        if (!e) continue;

        size_t chain = 0;
        s.used_buckets++;

        while (e) {
            chain++;
            e = e->next;
        }

        if (chain > 1) s.total_collisions += (chain - 1);
        if (chain > s.max_chain_length) s.max_chain_length = chain;
    }

    return s;
}

void db_print(SimpleDB *db)
{
    if (!db) { printf("(null database)\n"); return; }

    printf("Database Contents (%zu entries):\n", db->count);
    for (size_t i = 0; i < db->capacity; i++) {
        Entry *e = db->buckets[i];
        while (e) {
            printf("  %s -> %s\n", e->key, e->value);
            e = e->next;
        }
    }
}
