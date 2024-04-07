#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>

// clang -O2 dump_ip.c && sudo ./a.out

#define GC_BASE_ADDR 0xA000
#define regCP_MEC_RS64_INSTR_PNTR  0x2908

#define DUMP_COUNT 0x100000
//int dumps[DUMP_COUNT];

#define MAX_ADDR 0x100000
int histogram[MAX_ADDR] = {0};

int main() {
  int fd = open("/sys/kernel/debug/dri/0/amdgpu_regs2", O_RDONLY);
  // mmap doesn't work :(
  /*int* gpu = (int *)mmap(0, 0x1000, PROT_READ, MAP_SHARED, fd, GC_BASE_ADDR*4);
  if (gpu == MAP_FAILED) {
    printf("MAP FAILED\n");
    return -1;
  }*/
  int dump;
  for (int i = 0; i < DUMP_COUNT; i++) {
    pread(fd, &dump, 4, (GC_BASE_ADDR + regCP_MEC_RS64_INSTR_PNTR)*4);
    //if (dumps[i] != 0x9123) i++;
    histogram[dump]++;
  }

  for (int i = 0; i < MAX_ADDR; i++) {
    if (histogram[i] != 0) printf("%8x : %d\n", i, histogram[i]);
  }

  //for (int i = 0; i < DUMP_COUNT; i++) { printf("0x%8X\n", dumps[i]); }
  return 0;
}
