#ifndef FILE_H_INCLUDED
#define FILE_H_INCLUDED

#include <stdint.h>

int readData(int fd, int offset, int length, uint8_t* target);
int writeData(int fd, int offset, int length, uint8_t* source);

#endif // FILE_H_INCLUDED
