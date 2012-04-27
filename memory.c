#include <stdlib.h>
#include "memory.h"

free_list* free_list_make(size_t size) {
  free_list *l = malloc(sizeof(free_list));
  l->size = size;
  l->pos = 0;
  l->data = calloc(sizeof(void*), size);
  return l;
}

void free_list_add(free_list *l, void* ptr) {
  l->data[l->pos] = ptr;
  l->pos++;
}

void free_list_cleaunp(free_list *l) {
  while (pos >= 0) {
    free(l->data[l->pos]);
    l->pos--;
  }
}
  
