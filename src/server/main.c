#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
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

        if(getRequest(clientSocket, &req))
        {
            resp.error = 0;
            int fd = openFile(filePath);

            if (req.type == CMD_READ)
            {
                readData(fd, req.offset, req.length, resp.payload);
            }
            else if (req.type == CMD_WRITE)
            {
                writeData(fd, req.offset, req.length, req.payload);
            }
        }
        else
        {
            resp.error = 1;
            printf("Bad request received.\n");
        }

        resp.handle = req.handle;

        //sendResponse(???, &resp);

        close(clientSocket);
    }

    close(listeningSocket);

    return 0;
}
