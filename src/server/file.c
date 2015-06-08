#include "file.h"

#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>

////////////////////////////////////////////////////////////////////////////////////////////////////
int readData(int fd, int offset, int length, uint8_t* target)
{
    if (lseek(fd, offset, SEEK_SET) < 0)
    {
        perror("lseek");
        return 0;
    }

    if (read(fd, target, length) < 0)
    {
        perror("read");
        return 0;
    }

    return 1;
}

////////////////////////////////////////////////////////////////////////////////////////////////////
int writeData(int fd, int offset, int length, uint8_t* source)
{
    if (lseek(fd, offset, SEEK_SET) < 0)
    {
        perror("lseek");
        return 0;
    }

    if (write(fd, source, length) < 0)
    {
        perror("write");
        return 0;
    }

    return 1;
}
