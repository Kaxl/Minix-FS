#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <stdint.h>
#include <string.h>
#include "network.h"
#include "file.h"

int running = 1;

int main(int argc, char* argv[])
{
    if (argc < 2)
    {
        printf("Usage : %s <file_path>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char* filePath = malloc(strlen(argv[1]) * sizeof(char));
    strcpy(filePath, argv[1]);
    Request req;
    Response resp = {RESPONSE_MAGIC};
    int listeningSocket = openListeningSocket(LISTENING_PORT);

    while (running)
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

        if (!sendResponse(clientSocket, &resp, req.length))
        {
            printf("error sending response\n");
        }
        close(clientSocket);
    }

    close(listeningSocket);

    return 0;
}
