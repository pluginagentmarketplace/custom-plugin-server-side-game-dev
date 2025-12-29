# Socket Programming Guide for Games

## Socket Types

### TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| Reliability | Guaranteed | None |
| Ordering | Preserved | None |
| Latency | Higher | Lower |
| Use case | Chat, login | Positions |

## Socket Options

### TCP Optimizations
```c
int flag = 1;
setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));
```

### UDP Buffer Sizes
```c
int bufsize = 1024 * 1024;  // 1MB
setsockopt(sock, SOL_SOCKET, SO_RCVBUF, &bufsize, sizeof(bufsize));
```

## Game Networking Patterns

### 1. Position Updates (UDP)
```
[4 bytes: player_id][4 bytes: x][4 bytes: y][4 bytes: rotation]
```

### 2. Reliable UDP
- Sequence numbers
- ACK packets
- Retransmission timer

### 3. Delta Compression
- Only send changed values
- Reduce bandwidth 60-80%

## Performance Tips

1. **Use non-blocking sockets**
2. **Batch small packets**
3. **Implement MTU discovery**
4. **Use binary protocols**
5. **Pool socket buffers**

## Example: Reliable UDP Header
```
[2: seq_num][2: ack_num][1: flags][1: channel][2: length][N: payload]
```
