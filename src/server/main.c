#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include "network.h"
#include "file.h"

int main(int argc, char* argv[])
{
    if (argc < 1)
    {
        printf("Usage : %s <file_path>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char* filePath = argv[1];
    Request req;
    Response resp = {RESPONSE_MAGIC};
    int listeningSocket = openListeningSocket(LISTENING_PORT);

    while (1)
    {
        int clientSocket = waitClientConnection(listeningSocket);

        // TODO : Meilleurs gestion des erreurs

        if (getRequest(clientSocket, &req))
        {
            int fd;
            resp.error = 0;

            if (req.type == CMD_READ)
            {
                if ((fd = open(filePath, O_RDONLY)) < 0)
                {
                    perror("open");
                    resp.error = 1;
                }
                else if (!readData(fd, req.offset, req.length, resp.payload))
                {
                    resp.error = 1;
                }
            }
            else if (req.type == CMD_WRITE)
            {
                if ((fd = open(filePath, O_WRONLY)) < 0)
                {
                    perror("open");
                    resp.error = 1;
                }
                else if (!writeData(fd, req.offset, req.length, req.payload))
                {
                    resp.error = 1;
                }
            }
            close(fd);
        }
        else
        {
            resp.error = 1;
            req.length = 0;
            printf("Bad request received.\n");
        }

        resp.handle = req.handle;

        sendResponse(clientSocket, &resp, req.length);

        close(clientSocket);
    }

    close(listeningSocket);

    return 0;
}
