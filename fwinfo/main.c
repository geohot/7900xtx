#include <stdio.h>
#include "amdgpu_ucode.h"

int main(int argc, char *argv[]) {
  for (int i = 1; i < argc; i++) {
    FILE *f = fopen(argv[i], "rb");
    if (!f) { printf("%s NOT FOUND\n", argv[i]); continue; }
    struct common_firmware_header header;
    fread(&header, 1, sizeof(header), f);

    /*printf("%s\n", argv[i]);
    printf("header_version_major: %d\n", header.header_version_major);
    printf("header_version_minor: %d\n", header.header_version_minor);
    printf("size_bytes: %d\n", header.size_bytes);
    printf("ucode_version: 0x%x\n", header.ucode_version);
    printf("ucode_size_bytes: %d\n", header.ucode_size_bytes);
    printf("ucode_array_offset_bytes: 0x%x\n", header.ucode_array_offset_bytes);
    printf("\n");*/
    printf("%-40s size_bytes:0x%5X ucode_size_bytes:0x%x\n", argv[i], header.size_bytes, header.ucode_size_bytes);
    fclose(f);
  }

  return 0;
}

// 00000100: e260 7124 688d 34fb 7573 3d4b f90e 9a9a

// /lib/firmware/amdgpu/gc_11_0_0_mes1.bin
// 00000100: cb31 524b 1a47 8b64 dcac 8fd0 462b cc15
