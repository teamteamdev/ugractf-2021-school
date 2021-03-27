#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <zlib.h>

uint64_t __attribute__((section("compressed_size"))) compressed_section_size = 0;

const char* __attribute__((section("compressed"))) no_flag(void)
{
  return "Ну тогда до свидания";
}

const char* __attribute__((section("compressed"))) still_no_flag(void)
{
  return "Не положено";
}

const char* __attribute__((section("compressed"))) really_no_flag(void)
{
  return "Это вообще что такое";
}

extern const char* __attribute__((section("compressed"))) get_flag(void);

void __attribute__((section("compressed"))) decide_if_show_flag(void)
{
  printf("Показать флаг? (y/n)");
  char answer = getchar();
  printf("\n");
  const char* result;
  if (answer == 'y') {
    result = still_no_flag();
  } else if (answer == 'n') {
    result = no_flag();
  } else {
    result = really_no_flag();
    //result = get_flag();
  }
  printf("%s\n", result);
}

extern void* __start_compressed;
extern void* __stop_compressed;

int main()
{
  size_t uncompressed_size = (intptr_t)&__stop_compressed - (intptr_t)&__start_compressed;
  void* uncompressed_text = malloc(uncompressed_size);
  z_stream infstream = {0};
  infstream.avail_in = compressed_section_size;
  infstream.next_in = (Bytef*)&__start_compressed;
  infstream.avail_out = uncompressed_size;
  infstream.next_out = (Bytef*)uncompressed_text;

  inflateInit(&infstream);
  inflate(&infstream, Z_NO_FLUSH);
  inflateEnd(&infstream);
  memcpy(&__start_compressed, uncompressed_text, uncompressed_size);
  free(uncompressed_text);

  decide_if_show_flag();
  return 0;
}
