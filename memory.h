#ifndef LENGUA_MEMORY_H
#define LENGUA_MEMORY_H

typedef struct {
  size_t size;
  int pos;
  void** data;
} free_list;

free_list* free_list_make(size_t size);
void free_list_add(free_list *l, void* ptr);
void free_list_cleaunp(free_list *l);
