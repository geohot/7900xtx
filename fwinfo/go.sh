#!/bin/bash
FW=/lib/firmware/amdgpu
gcc main.c
./a.out $FW/psp_13_0_0_sos.bin $FW/psp_13_0_0_ta.bin $FW/smu_13_0_0.bin  \
  $FW/gc_11_0_0_pfp.bin $FW/gc_11_0_0_me.bin $FW/gc_11_0_0_rlc.bin $FW/gc_11_0_0_mec.bin \
  $FW/gc_11_0_0_mes_2.bin $FW/gc_11_0_0_mes1.bin $FW/gc_11_0_0_imu.bin \
  $FW/dcn_3_2_0_dmcub.bin $FW/vcn_4_0_0.bin $FW/sdma_6_0_0.bin


