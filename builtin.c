#include "stdio.h"
#include "stdlib.h"


int bi_print(const char* s) {
  printf(": %s\n", s);
  return 0;
}

int gt(int lhs, int rhs) {
  return lhs > rhs;
}
int gte(int lhs, int rhs) {
  return lhs >= rhs;
}
int lt(int lhs, int rhs) {
  return lhs < rhs;
}
int lte(int lhs, int rhs) {
  return lhs < rhs;
}
int eq(int lhs, int rhs) {
  return lhs == rhs;
}
int neq(int lhs, int rhs) {
  return lhs != rhs;
}

const char* int2str(int arg) {
  char * s = malloc(33);
  sprintf(s, "%d", arg);
  return s;
}

int str2int(const char* arg) {
  return atoi(arg);
}

int add(int v1, int v2) {
  return v1 + v2;
}

int subtract(int v1, int v2) {
  return v1 - v2;
}


