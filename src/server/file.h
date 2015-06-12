#ifndef FILE_H_INCLUDED
#define FILE_H_INCLUDED

#include <stdint.h>

// Reads data from a file
int readData(int fd, int offset, int length, uint8_t* target);

// Writes data into a file
int writeData(int fd, int offset, int length, uint8_t* source);

#endif // FILE_H_INCLUDED
