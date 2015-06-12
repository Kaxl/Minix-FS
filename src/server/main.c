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

    // Makes a copy of the file path given in arguments
    char* filePath = malloc(strlen(argv[1]) * sizeof(char));
    strcpy(filePath, argv[1]);

    Request req;
    Response resp = {RESPONSE_MAGIC};
    int listeningSocket = openListeningSocket(LISTENING_PORT);

    while (running)
    {
        int clientSocket = waitClientConnection(listeningSocket);

        resp.error = 0;
        resp.payload = NULL;

        if (getRequest(clientSocket, &req))
        {
            int fd;

            if (req.type == CMD_READ)
            {
                resp.payload = malloc(req.length);

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
            printf("Bad request received.\n");
        }

        resp.handle = req.handle;

        // Sets the length of the payload to 0 if an error occured or if the request was of type WRITE
        if (resp.error || req.type == CMD_WRITE)
        {
            req.length = 0;
        }

        if (!sendResponse(clientSocket, &resp, req.length))
        {
            printf("Error sending response\n");
        }

        free(resp.payload);
        close(clientSocket);
    }

    close(listeningSocket);
    free(filePath);

    return 0;
}
