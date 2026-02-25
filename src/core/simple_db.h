/**
 * simple_db.h — Chained hash-table key-value store
 *
 * All keys and values are NUL-terminated UTF-8 strings.
 * Thread-safety: NOT thread-safe (single-threaded use only).
 */

#ifndef SIMPLE_DB_H
#define SIMPLE_DB_H

#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* -------------------------------------------------------------------------
 * Types
 * ---------------------------------------------------------------------- */

typedef struct SimpleDB SimpleDB;

typedef struct {
    size_t total_entries;
    size_t total_collisions;
    size_t max_chain_length;
    size_t used_buckets;
} DBStats;

/* -------------------------------------------------------------------------
 * Lifecycle
 * ---------------------------------------------------------------------- */

/** Create a new database.  Returns NULL on allocation failure. */
SimpleDB *db_create(void);

/** Destroy database and free ALL memory (including stored strings). */
void db_destroy(SimpleDB *db);

/* -------------------------------------------------------------------------
 * CRUD
 * ---------------------------------------------------------------------- */

/** Insert or update a key-value pair.  Returns true on success. */
bool db_set(SimpleDB *db, const char *key, const char *value);

/**
 * Return value for key, or NULL if not found.
 * The pointer is valid until the next db_set / db_delete / db_clear on the
 * same key, so decode it immediately.
 */
const char *db_get(SimpleDB *db, const char *key);

/** Delete key. Returns true if key existed and was removed. */
bool db_delete(SimpleDB *db, const char *key);

/** Return true if key exists. */
bool db_exists(SimpleDB *db, const char *key);

/* -------------------------------------------------------------------------
 * Utility
 * ---------------------------------------------------------------------- */

/** Return number of stored entries. */
size_t db_count(SimpleDB *db);

/** Remove all entries. */
void db_clear(SimpleDB *db);

/**
 * Return an array of *count keys (heap-allocated copies).
 * The caller is responsible for freeing each string and the array itself.
 * Returns NULL if the database is empty or allocation fails.
 */
char **db_keys(SimpleDB *db, size_t *count);

/** Return statistics about the hash table. */
DBStats db_stats(SimpleDB *db);

/** Print all key-value pairs to stdout (debugging). */
void db_print(SimpleDB *db);

#ifdef __cplusplus
}
#endif

#endif /* SIMPLE_DB_H */
