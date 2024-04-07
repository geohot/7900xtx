#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>

// clang -O2 dump_ip.c && sudo ./a.out

#define GC_BASE_ADDR 0xA000
#define regCP_MEC_RS64_INSTR_PNTR  0x2908
#define regCP_MEC_RS64_CNTL 0x2904

#define MEC_HALT 1<<30
#define MEC_STEP 1<<31

#define DUMP_COUNT 0x100000
//int dumps[DUMP_COUNT];

#define MAX_ADDR 0x100000
int histogram[MAX_ADDR] = {0};

int main() {
  int fd = open("/sys/kernel/debug/dri/0/amdgpu_regs2", O_RDWR);

  // halting crashes the GPU

  int val;

  /*val = MEC_HALT;
  pwrite(fd, &val, 4, (GC_BASE_ADDR + regCP_MEC_RS64_CNTL)*4);

  // 10 steps
  for (int i = 0; i < 10; i++) {
    pread(fd, &val, 4, (GC_BASE_ADDR + regCP_MEC_RS64_INSTR_PNTR)*4);
    //printf("regCP_MEC_RS64_INSTR_PNTR : %x\n", val);
  }

  // unhalt
  val = 0;
  pwrite(fd, &val, 4, (GC_BASE_ADDR + regCP_MEC_RS64_CNTL)*4);

  pread(fd, &val, 4, (GC_BASE_ADDR + regCP_MEC_RS64_CNTL)*4);
  printf("regCP_MEC_RS64_CNTL : %x\n", val);

  exit(0);*/


  // mmap doesn't work :(
  /*int* gpu = (int *)mmap(0, 0x1000, PROT_READ, MAP_SHARED, fd, GC_BASE_ADDR*4);
  if (gpu == MAP_FAILED) {
    printf("MAP FAILED\n");
    return -1;
  }*/
  int dump;
  for (int i = 0; i < DUMP_COUNT; i++) {
    pread(fd, &dump, 4, (GC_BASE_ADDR + regCP_MEC_RS64_INSTR_PNTR)*4);
    //pread(fd, &dump, 4, (GC_BASE_ADDR + tmp)*4);
    //if (dumps[i] != 0x9123) i++;
    //dumps[i] = dump;
    histogram[dump]++;
  }

  for (int i = 0; i < MAX_ADDR; i++) {
    if (histogram[i] != 0) printf("%8x : %d\n", i*4, histogram[i]);
  }

  //for (int i = 0; i < DUMP_COUNT; i++) { printf("%5d: 0x%8X\n", i, dumps[i]); }
  return 0;
}
