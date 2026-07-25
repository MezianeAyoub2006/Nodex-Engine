#ifndef NX_POOL_H
#define NX_POOL_H

#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "nodex/status/status.h"

#define NX_DEFINE_POOL(T, NAME)                                                     \
typedef struct {                                                                    \
    T* data;                                                                        \
    uint32_t* generation;                                                           \
    bool* active;                                                                   \
    uint32_t* free_list;                                                            \
    size_t capacity;                                                                \
    size_t free_count;                                                              \
} NAME##Pool;                                                                       \
\
static NxStatus NAME##_Pool_Init(NAME##Pool* pool, size_t capacity) {               \
    if (!pool || capacity == 0) return NX_ERR_INVALID_ARGS;                         \
    pool->data = (T*)malloc(capacity * sizeof(T));                                  \
    pool->generation = (uint32_t*)calloc(capacity, sizeof(uint32_t));               \
    pool->active = (bool*)calloc(capacity, sizeof(bool));                           \
    pool->free_list = (uint32_t*)malloc(capacity * sizeof(uint32_t));               \
    if (!pool->data || !pool->generation || !pool->active || !pool->free_list)      \
        return NX_ERR_NULLPTR;                                                      \
    for (size_t i = 0; i < capacity; i++)                                           \
        pool->free_list[i] = (uint32_t)(capacity - 1 - i);                          \
    pool->capacity = capacity;                                                      \
    pool->free_count = capacity;                                                    \
    return NX_OKAY;                                                                 \
}                                                                                   \
\
static NxStatus NAME##_Pool_Grow(NAME##Pool* pool, size_t new_capacity) {           \
    if (!pool || new_capacity <= pool->capacity)                                    \
        return NX_ERR_INVALID_ARGS;                                                 \
    T* new_data = (T*)realloc(pool->data, new_capacity * sizeof(T));                \
    uint32_t* new_gen = (uint32_t*)realloc(                                         \
        pool->generation,                                                           \
        new_capacity * sizeof(uint32_t)                                             \
    );                                                                              \
    bool* new_active = (bool*)realloc(                                              \
        pool->active,                                                               \
        new_capacity * sizeof(bool)                                                 \
    );                                                                              \
    uint32_t* new_free = (uint32_t*)realloc(                                        \
        pool->free_list,                                                            \
        new_capacity * sizeof(uint32_t)                                             \
    );                                                                              \
    if (!new_data || !new_gen || !new_active || !new_free)                          \
        return NX_ERR_NULLPTR;                                                      \
    pool->data = new_data;                                                          \
    pool->generation = new_gen;                                                     \
    pool->active = new_active;                                                      \
    pool->free_list = new_free;                                                     \
    for (size_t i = pool->capacity; i < new_capacity; i++) {                        \
        pool->generation[i] = 0;                                                    \
        pool->active[i] = false;                                                    \
        pool->free_list[pool->free_count++] = (uint32_t)i;                          \
    }                                                                               \
    pool->capacity = new_capacity;                                                  \
    return NX_OKAY;                                                                 \
}                                                                                   \
\
static inline int32_t NAME##_Pool_Acquire(NAME##Pool* pool) {                       \
    if (!pool) return -1;                                                           \
    if (pool->free_count == 0) {                                                    \
        size_t new_cap = pool->capacity == 0 ? 1 : pool->capacity * 2;              \
        if (NAME##Pool_Grow(pool, new_cap) != NX_OKAY) return -1;                   \
    }                                                                               \
    uint32_t idx = pool->free_list[--pool->free_count];                             \
    pool->active[idx] = true;                                                       \
    memset(&pool->data[idx], 0, sizeof(T));                                         \
    return (int32_t)idx;                                                            \
}                                                                                   \
\
static inline NxStatus NAME##_Pool_Release(NAME##Pool* pool, int32_t index) {       \
    if (!pool || index < 0 || (size_t)index >= pool->capacity)                      \
        return NX_ERR_INVALID_ARGS;                                                 \
    if (!pool->active[index]) return NX_ERR_INVALID_ARGS;                           \
    pool->active[index] = false;                                                    \
    pool->generation[index]++;                                                      \
    pool->free_list[pool->free_count++] = (uint32_t)index;                          \
    return NX_OKAY;                                                                 \
}                                                                                   \
\
static inline T* NAME##_Pool_Get(NAME##Pool* pool, int32_t index, uint32_t gen) {   \
    if (!pool || index < 0 || (size_t)index >= pool->capacity)                      \
        return NULL;                                                                \
    if (!pool->active[index] || pool->generation[index] != gen)                     \
        return NULL;                                                                \
    return &pool->data[index];                                                      \
}                                                                                   \
\
static inline uint32_t NAME##_Pool_GetGeneration(NAME##Pool* pool, int32_t index) { \
    if (!pool || index < 0 || (size_t)index >= pool->capacity)                      \
        return 0;                                                                   \
    return pool->generation[index];                                                 \
}                                                                                   \
\
static void NAME##Pool_Destroy(NAME##Pool* pool) {                                  \
    if (!pool) return;                                                              \
    free(pool->data);                                                               \
    free(pool->generation);                                                         \
    free(pool->active);                                                             \
    free(pool->free_list);                                                          \
    memset(pool, 0, sizeof(NAME##Pool));                                            \
}

#endif              

