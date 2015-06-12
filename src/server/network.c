#include "network.h"

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <time.h>

////////////////////////////////////////////////////////////////////////////////////////////////////
int openListeningSocket(int port)
{
    int sock;
    struct sockaddr_in address;

    // Creates the socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    address.sin_family = AF_INET;
    address.sin_port = (in_port_t)htons(port);
    address.sin_addr.s_addr = htonl(INADDR_ANY);

    // Binds the socket to TCP port
    if ((bind(sock, (struct sockaddr*)&address, sizeof(struct sockaddr_in))) < 0)
    {
        perror("bind");
        exit(EXIT_FAILURE);
    }

    return sock;
}

////////////////////////////////////////////////////////////////////////////////////////////////////
int waitClientConnection(int listeningSocket)
{
    // Waits for a client to connect
    if (listen(listeningSocket, 1) < 0)
    {
        perror("listen");
        shutdown(listeningSocket, SHUT_RDWR);
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in clientAddress;
    socklen_t clientLength;
    int clientSocket;

    // Open a new socket for the client
    if ((clientSocket = accept(listeningSocket, (struct sockaddr*)&clientAddress, &clientLength)) < 0)
    {
        perror("accept");
        shutdown(listeningSocket, SHUT_RDWR);
        exit(EXIT_FAILURE);
    }

    return clientSocket;
}

////////////////////////////////////////////////////////////////////////////////////////////////////
int getRequest(int sock, Request* req)
{
    uint8_t* buffer = (uint8_t*)req;
    int nbByte;
    int offset = 0;
    int lengthToRead = REQUEST_HEADER_SIZE;
    int headerReceived = 0;
    clock_t start = clock();

    while(1)
    {
        // Reads bytes from the socket
        if ((nbByte = read(sock, &buffer[offset], lengthToRead - offset)) < 0)
        {
            perror("read");
            shutdown(sock, SHUT_RDWR);
            exit(EXIT_FAILURE);
        }

        // If bytes were received, increments the offset and restarts the timer
        if (nbByte > 0)
        {
            offset += nbByte;
            start = clock();
        }

        // If enough bytes were received
        if (offset == lengthToRead)
        {
            // Header received
            if (!headerReceived)
            {
                printf("header received\n");

                req->magic = ntohl(req->magic);
                req->type = ntohl(req->type);
                req->handle = ntohl(req->handle);
                req->offset = ntohl(req->offset);
                req->length = ntohl(req->length);

                if(req->magic != REQUEST_MAGIC || (req->type != CMD_READ && req->type != CMD_WRITE))
                {
                    printf("bad header\n");
                    return 0;
                }
                if(req->type == CMD_READ || req->length == 0)
                {
                    return 1;
                }
                lengthToRead += req->length;
                headerReceived = 1;
            }
            else // Payload received
            {
                printf("payload received\n");
                return 1;
            }
        }

        // Checks if timeout
        if ((clock() - start) * 1000 / CLOCKS_PER_SEC > RECEPTION_TIMEOUT)
        {
            printf("timeout\n");
            return 0;
        }
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////
int sendResponse(int sock, Response* resp, uint32_t payloadLength)
{
    resp->magic = htonl(resp->magic);
    resp->handle = htonl(resp->handle);
    resp->error = htonl(resp->error);

    // Sends the response header
    if (write(sock, resp, RESPONSE_HEADER_SIZE) < 0)
    {
        perror("write");
        return 0;
    }
    // Sends the response payload
    if (payloadLength > 0 && write(sock, resp->payload, payloadLength) < 0)
    {
        perror("write");
        return 0;
    }
    return 1;
}
