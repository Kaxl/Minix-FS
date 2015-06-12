#ifndef NETWORK_H_INCLUDED
#define NETWORK_H_INCLUDED

#include <stdint.h>

#define LISTENING_PORT          2200
#define RECEPTION_TIMEOUT       5000

#define REQUEST_HEADER_SIZE     20
#define RESPONSE_HEADER_SIZE    12
#define PAYLOAD_SIZE            1024

#define REQUEST_MAGIC   0x76767676
#define RESPONSE_MAGIC  0x87878787

#define CMD_READ    0
#define CMD_WRITE   1

typedef struct __attribute__ ((__packed__)) Request
{
    uint32_t magic;
    uint32_t type;
    uint32_t handle;
    uint32_t offset;
    uint32_t length;
    uint8_t payload[PAYLOAD_SIZE];
} Request;

typedef struct __attribute__ ((__packed__)) Response
{
    uint32_t magic;
    uint32_t error;
    uint32_t handle;
    uint8_t payload[PAYLOAD_SIZE];
} Response;

int openListeningSocket(int port);
int waitClientConnection(int listeningSocket);
int getRequest(int sock, Request* req);
int sendResponse(int sock, Response* resp, uint32_t payloadLength);

#endif // NETWORK_H_INCLUDED
