# I/O Multiplexing for Game Servers

## Models Comparison

| Model | Max Connections | Performance | Complexity |
|-------|-----------------|-------------|------------|
| select | ~1024 | Low | Simple |
| poll | No limit | Medium | Simple |
| epoll (Linux) | Millions | High | Medium |
| kqueue (BSD/Mac) | Millions | High | Medium |
| io_uring (Linux 5.1+) | Millions | Highest | Complex |

## When to Use

### epoll (Linux Production)
```c
int epoll_fd = epoll_create1(0);
struct epoll_event event;
event.events = EPOLLIN | EPOLLET;  // Edge-triggered
epoll_ctl(epoll_fd, EPOLL_CTL_ADD, socket_fd, &event);
```

### kqueue (macOS/BSD)
```c
int kq = kqueue();
struct kevent event;
EV_SET(&event, socket_fd, EVFILT_READ, EV_ADD, 0, 0, NULL);
kevent(kq, &event, 1, NULL, 0, NULL);
```

## Best Practices

1. **Use edge-triggered mode** for high performance
2. **Handle EAGAIN/EWOULDBLOCK** properly
3. **Batch syscalls** when possible
4. **Use io_uring** for Linux 5.1+ systems
