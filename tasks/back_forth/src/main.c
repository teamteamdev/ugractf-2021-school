#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/socket.h>

extern const char* get_flag(void);

inline static void send_line(int fd, const char* line)
{
  size_t len = strlen(line);
  write(fd, line, len);
  write(fd, "\n", 1);
}

inline static void receive_line(int fd)
{
  char buf[1024];
  size_t pos = 0;
  while (true) {
    ssize_t ret = read(fd, buf + pos, sizeof(buf) - pos);
    if (ret <= 0) {
      exit(0);
    }
    pos += ret;
    if (buf[pos - 1] == '\n') {
      buf[pos] = '\0';
      break;
    }
  }
}

void run_alice(int fd)
{
  printf("Party 1 started, using secure channel\n");
  while (true) {
#include "alice.h"
    sleep(3);
  }
}

void run_bob(int fd)
{
  printf("Party 2 started, using secure channel\n");
  while (true) {
#include "bob.h"
    sleep(3);
  }
}

int main()
{
  int sv[2];
  printf("Creating secure connection\n");
  socketpair(AF_UNIX, SOCK_STREAM, 0, sv);
  if (fork()) {
    close(sv[0]);
    run_alice(sv[1]);
  } else {
    close(sv[1]);
    run_bob(sv[0]);
  }
  return 0;
}
