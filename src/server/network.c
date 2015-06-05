#include "network.h"

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <arpa/inet.h>

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
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in clientAddress;
    socklen_t clientLength;
    int clientSocket;

    // Open a new socket for the client
    if ((clientSocket = accept(listeningSocket, (struct sockaddr*)&clientAddress, &clientLength)) < 0)
    {
        perror("accept");
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

    // Reads the header of the request message
    for (int i = 0; i < RECEPTION_TIMEOUT && offset < REQUEST_HEADER_SIZE; i++)
    {
        if ((nbByte = read(sock, &buffer[offset], REQUEST_HEADER_SIZE - offset)) < 0)
        {
            perror("read");
            exit(EXIT_FAILURE);
        }
        offset += nbByte;
    }

    // Returns FALSE if the header is not complete or incorrect
    if (offset != REQUEST_HEADER_SIZE || req->magic != REQUEST_MAGIC ||
        (req->type != CMD_READ && req->type != CMD_WRITE))
    {
        return 0;
    }

    // Reads the payload
    for (int i = 0; i < RECEPTION_TIMEOUT && offset < REQUEST_HEADER_SIZE + req->length; i++)
    {
        if ((nbByte = read(sock, &buffer[offset], REQUEST_HEADER_SIZE - offset)) < 0)
        {
            perror("read");
            exit(EXIT_FAILURE);
        }
        offset += nbByte;
    }

    // Returns FALSE if the payload isn't complete
    return (offset == REQUEST_HEADER_SIZE + req->length);
}
