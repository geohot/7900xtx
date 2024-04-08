# MEC stands for Micro Engine Compute

This is the microcontroller that controls the compute queues on the GFX/compute engine.

The MEC block has 4 independent threads, referred to as "pipes" in engineering and "ACEs" (Asynchronous Compute Engines) in marketing. One MEC => 4 ACEs, two MECs => 8 ACEs. Each pipe can manage 8 compute queues, or one of the pipes can run HW scheduler microcode which assigns "virtual" queues to queues on the other 3/7 pipes.

```
	GFX_FW_TYPE_RS64_MEC_P0_STACK               = 94,   /* RS64 MEC stack P0        SOC21   */
	GFX_FW_TYPE_RS64_MEC_P1_STACK               = 95,   /* RS64 MEC stack P1        SOC21   */
	GFX_FW_TYPE_RS64_MEC_P2_STACK               = 96,   /* RS64 MEC stack P2        SOC21   */
	GFX_FW_TYPE_RS64_MEC_P3_STACK               = 97,   /* RS64 MEC stack P3        SOC21   */
```

- https://www.phoronix.com/forums/forum/linux-graphics-x-org-drivers/open-source-amd-linux/856534-amdgpu-questions/page3#post857850
- https://dl.acm.org/doi/fullHtml/10.1145/3453417.3453432#sec-11
- https://www.cs.unc.edu/~otternes/papers/rtsj2022.pdf

What is VMID 9? All compute is on "Pipe 0  Queue 2  VMID 9"

Dump the ring with `sudo umr -RS gfx_0.0.0`

PM4 instead of AQL in ops_kfd.py?

The primary role of an ACE (MEC) is to dispatch blocks from the kernel at the head of an HSA queue to the SEs

The 7900XTX has 4 ACEs and 6 Shader Engines as seen in the main diagram.

## Understanding firmware

Based off c55ab5e8ba327ef3b219234291b7c4fc2f91248c  gc_11_0_0_mec_new.bin

Load with offset=0x200 length 0x41520
Load stack @ 0x100000 with offset 0x41720 length 0x21f00

- 0x7000000000000 = text
- 0x7000000001000 = irq handler
- 0x7000000003000 = start
- 0x7000000100000 = stack
- 0x13d80 = context_switch?
- 0x16800 = context_switch_alt?
- 0x24788 = wait_for_queue
- NOTE: the jumptable comes from regCP_MEC_ME1_UCODE_ADDR/regCP_MEC_ME1_UCODE_DATA
- PM4 commands, how do I find these? (used tracer)
  - 0x285e8 = PACKET3_DISPATCH_DIRECT
  - 0x2aa30 = PACKET3_NOP
  - 0x2b768 = PACKET3_SET_SH_REG
  - 0x2be70 = PACKET3_ACQUIRE_MEM
- 0x1080800000000 = MMIO (see make_ghidra_script.py to import MMIO regs, region is 0x40000)
- 0x1000800000000 = alt8 MMIO
- 0x1000200000000 = alt2 MMIO
- 0x1000100000000 = alt1 MMIO
- s11=0x100020000c000
- s10=0x1000100009124
- s9=0x10001000308c0

## Dumping queues

```
kafka@q:/lib/firmware/amdgpu$ sudo umr -cpc
[WARNING]: Unknown ASIC [amd744c] should be added to pci.did to get proper name
Pipe 0  Queue 0  VMID 0
  PQ BASE 0x44f000  RPTR 0x200  WPTR 0x200  RPTR_ADDR 0x4010e0  CNTL 0xc030890a
  EOP BASE 0x449000  RPTR 0x40000008  WPTR 0x1ff8008  WPTR_MEM 0x8
  MQD 0x85fe90f000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

Pipe 0  Queue 1  VMID 0
  PQ BASE 0x457000  RPTR 0x200  WPTR 0x200  RPTR_ADDR 0x401360  CNTL 0xc030890a
  EOP BASE 0x44b000  RPTR 0x40000008  WPTR 0x1ff8008  WPTR_MEM 0x8
  MQD 0x85feade000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

Pipe 0  Queue 2  VMID 9
  PQ BASE 0x7e9311a00000  RPTR 0x4f2e0  WPTR 0x4f730  RPTR_ADDR 0x7e936ba8a080  CNTL 0x8084514
  EOP BASE 0x7e936ba7c000  RPTR 0x400002a8  WPTR 0x3ff82a8  WPTR_MEM 0x2a8
  MQD 0xd88200  DEQ_REQ 0x0  IQ_TIMER 0x8100100  AQL_CONTROL 0x1
  SAVE BASE 0x7e91fe400000  SIZE 0x2bea000  STACK OFFSET 0xa000  SIZE 0xa000

Pipe 0  Queue 3  VMID 9
  PQ BASE 0x7e936baea000  RPTR 0xa0  WPTR 0x18a0  RPTR_ADDR 0x7e936c08f080  CNTL 0x808c509
  EOP BASE 0x7e936bae6000  RPTR 0x40000050  WPTR 0x3ff8050  WPTR_MEM 0x50
  MQD 0xd87200  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x1
  SAVE BASE 0x7e9201200000  SIZE 0x2bea000  STACK OFFSET 0xa000  SIZE 0xa000

ME 1 Pipe 0: INSTR_PTR 0x91cd (ASM 0x24734)
Pipe 1  Queue 0  VMID 0
  PQ BASE 0x451000  RPTR 0x200  WPTR 0x200  RPTR_ADDR 0x401180  CNTL 0xc030890a
  EOP BASE 0x449800  RPTR 0x40000008  WPTR 0x1ff8008  WPTR_MEM 0x8
  MQD 0x85feadb000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

Pipe 1  Queue 1  VMID 0
  PQ BASE 0x459000  RPTR 0x200  WPTR 0x200  RPTR_ADDR 0x401400  CNTL 0xc030890a
  EOP BASE 0x44b800  RPTR 0x40000008  WPTR 0x1ff8008  WPTR_MEM 0x8
  MQD 0x85feadd000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

ME 1 Pipe 1: INSTR_PTR 0x9123 (ASM 0x2448c)
Pipe 2  Queue 0  VMID 0
  PQ BASE 0x453000  RPTR 0x200  WPTR 0x200  RPTR_ADDR 0x401220  CNTL 0xc030890a
  EOP BASE 0x44a000  RPTR 0x40000008  WPTR 0x1ff8008  WPTR_MEM 0x8
  MQD 0x85feada000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

Pipe 2  Queue 1  VMID 0
  PQ BASE 0x45b000  RPTR 0x200  WPTR 0x200  RPTR_ADDR 0x4014a0  CNTL 0xc030890a
  EOP BASE 0x44c000  RPTR 0x40000008  WPTR 0x1ff8008  WPTR_MEM 0x8
  MQD 0x85feadc000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

ME 1 Pipe 2: INSTR_PTR 0x9123 (ASM 0x2448c)
Pipe 3  Queue 0  VMID 0
  PQ BASE 0x455000  RPTR 0x200  WPTR 0x200  RPTR_ADDR 0x4012c0  CNTL 0xc030890a
  EOP BASE 0x44a800  RPTR 0x40000008  WPTR 0x1ff8008  WPTR_MEM 0x8
  MQD 0x85feadf000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

Pipe 3  Queue 1  VMID 0
  PQ BASE 0x45d000  RPTR 0x200  WPTR 0x200  RPTR_ADDR 0x401540  CNTL 0xc030890a
  EOP BASE 0x44c800  RPTR 0x40000008  WPTR 0x1ff8008  WPTR_MEM 0x8
  MQD 0x85feaf7000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

ME 1 Pipe 3: INSTR_PTR 0x9123 (ASM 0x2448c)
Pipe 0  Queue 0  VMID 0
  PQ BASE 0x468000  RPTR 0x380  WPTR 0xab80  RPTR_ADDR 0x401a00  CNTL 0xd830800a
  EOP BASE 0x0  RPTR 0x40000000  WPTR 0x8000  WPTR_MEM 0x0
  MQD 0x85fe6a1000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

ME 3 Pipe 0: INSTR_PTR 0x92b4 (ASM 0x24ad0)
Pipe 1  Queue 0  VMID 0
  PQ BASE 0x600000  RPTR 0x2100  WPTR 0x2100  RPTR_ADDR 0x401960  CNTL 0xd8308011
  EOP BASE 0x0  RPTR 0x40000000  WPTR 0x8000  WPTR_MEM 0x0
  MQD 0x85feaf5000  DEQ_REQ 0x0  IQ_TIMER 0x0  AQL_CONTROL 0x0
  SAVE BASE 0x0  SIZE 0x0  STACK OFFSET 0x0  SIZE 0x0

ME 3 Pipe 1: INSTR_PTR 0x48dc (ASM 0x12370)
```

The SQ registers are on smc and should be readable with `sudo umr -s gfx1100 -O read_smc` but I can't get it to work.

They are in the reg files prefixed with `ix` instead of `reg`

```
kafka@q:~$ sudo umr --waves
[WARNING]: Unknown ASIC [amd744c] should be added to pci.did to get proper name
[WARNING]: Wave listing is unreliable if waves aren't halted; use -O halt_waves
[ERROR]: Could not open ring debugfs file '/sys/kernel/debug/dri/0/amdgpu_ring_gfx'
[WARNING]: On Navi and later ASICs the gfx ring name has changed, for instance: 'gfx_0.0.0'

------------------------------------------------------
se0.sa0.wgp3.simd1.wave0


Main Registers:
            ixSQ_WAVE_STATUS: 00010c20 |      ixSQ_WAVE_PC_LO: 13e5674c |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 20000d00 |     ixSQ_WAVE_HW_ID2: 091f0102 |  ixSQ_WAVE_GPR_ALLOC: 00027000 |
         ixSQ_WAVE_LDS_ALLOC: 000001fc |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00000c00 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: a36013fb |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se0.sa0.wgp3.simd1.wave1



Main Registers:
            ixSQ_WAVE_STATUS: 00010c20 |      ixSQ_WAVE_PC_LO: 13e563a0 |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 20000d01 |     ixSQ_WAVE_HW_ID2: 091f0102 |  ixSQ_WAVE_GPR_ALLOC: 0002702a |
         ixSQ_WAVE_LDS_ALLOC: 000001fc |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00001400 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: 94bb47d5 |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se0.sa0.wgp3.simd3.wave0



Main Registers:
            ixSQ_WAVE_STATUS: 00010c20 |      ixSQ_WAVE_PC_LO: 13e57020 |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 20000f00 |     ixSQ_WAVE_HW_ID2: 091f0102 |  ixSQ_WAVE_GPR_ALLOC: 00027000 |
         ixSQ_WAVE_LDS_ALLOC: 000001fc |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00005800 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: 30643b76 |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se0.sa0.wgp3.simd3.wave1



Main Registers:
            ixSQ_WAVE_STATUS: 00010c21 |      ixSQ_WAVE_PC_LO: 13e565a0 |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 20000f01 |     ixSQ_WAVE_HW_ID2: 091f0102 |  ixSQ_WAVE_GPR_ALLOC: 0002702a |
         ixSQ_WAVE_LDS_ALLOC: 000001fc |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00001000 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: 680cbcb8 |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se0.sa1.wgp0.simd1.wave0



Main Registers:
            ixSQ_WAVE_STATUS: 00010c20 |      ixSQ_WAVE_PC_LO: 13e56398 |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 20010100 |     ixSQ_WAVE_HW_ID2: 091f0102 |  ixSQ_WAVE_GPR_ALLOC: 00027000 |
         ixSQ_WAVE_LDS_ALLOC: 000001fc |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00006800 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: 050c77fb |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se0.sa1.wgp0.simd1.wave1



Main Registers:
            ixSQ_WAVE_STATUS: 00010c20 |      ixSQ_WAVE_PC_LO: 13e568b4 |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: b9c18be7 |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 20010101 |     ixSQ_WAVE_HW_ID2: 091f0102 |  ixSQ_WAVE_GPR_ALLOC: 0002702a |
         ixSQ_WAVE_LDS_ALLOC: 000001fc |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00000c00 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: e0b23766 |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se2.sa0.wgp0.simd0.wave1



Main Registers:
            ixSQ_WAVE_STATUS: 00018c20 |      ixSQ_WAVE_PC_LO: 13e562f8 |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 20080001 |     ixSQ_WAVE_HW_ID2: 09000102 |  ixSQ_WAVE_GPR_ALLOC: 0002702a |
         ixSQ_WAVE_LDS_ALLOC: 00000000 |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00000000 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: d0398c24 |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se3.sa0.wgp3.simd0.wave0



Main Registers:
            ixSQ_WAVE_STATUS: 00010c20 |      ixSQ_WAVE_PC_LO: 13e56648 |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 200c0c00 |     ixSQ_WAVE_HW_ID2: 09000102 |  ixSQ_WAVE_GPR_ALLOC: 00027000 |
         ixSQ_WAVE_LDS_ALLOC: 00000000 |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00003000 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: f0c26a7f |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se3.sa0.wgp3.simd0.wave1



Main Registers:
            ixSQ_WAVE_STATUS: 00010c20 |      ixSQ_WAVE_PC_LO: 13e56c68 |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 200c0c01 |     ixSQ_WAVE_HW_ID2: 09000102 |  ixSQ_WAVE_GPR_ALLOC: 0002702a |
         ixSQ_WAVE_LDS_ALLOC: 00000000 |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00001c00 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: 6a82dc24 |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se3.sa0.wgp3.simd2.wave1



Main Registers:
            ixSQ_WAVE_STATUS: 00010c20 |      ixSQ_WAVE_PC_LO: 13e5630c |      ixSQ_WAVE_PC_HI: 00007616 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 200c0e01 |     ixSQ_WAVE_HW_ID2: 09000102 |  ixSQ_WAVE_GPR_ALLOC: 0002702a |
         ixSQ_WAVE_LDS_ALLOC: 00000000 |    ixSQ_WAVE_TRAPSTS: 00000000 |     ixSQ_WAVE_IB_STS: 00006000 |    ixSQ_WAVE_IB_STS2: 00000203 |
           ixSQ_WAVE_IB_DBG1: 00000000 |         ixSQ_WAVE_M0: c4422177 |       ixSQ_WAVE_MODE: 000003f0 |
------------------------------------------------------
se3.sa0.wgp3.simd2.wave2



Main Registers:
            ixSQ_WAVE_STATUS: 20010c20 |      ixSQ_WAVE_PC_LO: febdd2e8 |      ixSQ_WAVE_PC_HI: 00007615 |    ixSQ_WAVE_EXEC_LO: b99caf90 |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 200c0e02 |     ixSQ_WAVE_HW_ID2: 09010102 |  ixSQ_WAVE_GPR_ALLOC: 00000000 |
         ixSQ_WAVE_LDS_ALLOC: bebebeef |    ixSQ_WAVE_TRAPSTS: 101ebcef |     ixSQ_WAVE_IB_STS: bc00bee7 |    ixSQ_WAVE_IB_STS2: bebebeef |
           ixSQ_WAVE_IB_DBG1: bebebeef |         ixSQ_WAVE_M0: bebebeef |       ixSQ_WAVE_MODE: bebebeef |
------------------------------------------------------
se3.sa0.wgp3.simd2.wave3



Main Registers:
            ixSQ_WAVE_STATUS: 20010c20 |      ixSQ_WAVE_PC_LO: febdd478 |      ixSQ_WAVE_PC_HI: 00007615 |    ixSQ_WAVE_EXEC_LO: ffffffff |
           ixSQ_WAVE_EXEC_HI: 00000000 |     ixSQ_WAVE_HW_ID1: 200c0e03 |     ixSQ_WAVE_HW_ID2: 09010102 |  ixSQ_WAVE_GPR_ALLOC: bebebeef |
         ixSQ_WAVE_LDS_ALLOC: bebebeef |    ixSQ_WAVE_TRAPSTS: 101ebcef |     ixSQ_WAVE_IB_STS: bc00bee7 |    ixSQ_WAVE_IB_STS2: bebebeef |
           ixSQ_WAVE_IB_DBG1: bebebeef |         ixSQ_WAVE_M0: bebebeef |       ixSQ_WAVE_MODE: bebebeef |
```

## Looking into the firmware

- polaris10_mec.bin <- f32dis works
- vega10_mec.bin <- f32dis doesn't work great, but it's still f32, and we still found DISPATCH_DIRECT
- gc_11_0_1_mec.bin <- f32?
- gc_11_0_0_mec.bin <- rs64

Multiply the register numbers by 4 to match with the rai file. From

0x00001260 = GC base address
+0x1ba1 = 0x2e01

```
# python3 f32dis.py /lib/firmware/amdgpu/polaris10_mec.bin | grep -A20 DISPATCH_DIRECT
DISPATCH_DIRECT:
    stw #0x1, [r0, #0x29]
    ldw r3, [r0, #0x5e]
    cbz r3, _PKT_0xa_14
    mov r6, r1
    mov r4, r1
    mov r5, r1
    mov r3, r1
    stw #0x2, [r0, #0x13]
    stw r6, reg[r0, #0x2e01]  # 0xb804 = COMPUTE_DIM_X
    stw r4, reg[r0, #0x2e02]
    stw r5, reg[r0, #0x2e03]
    stw r3, reg[r0, #0x2e00]  # 0xb800 = COMPUTE_DISPATCH_INITIATOR
    ...
```

```
# python3 f32dis.py /lib/firmware/amdgpu/gc_11_0_1_mec.bin | grep -A10 -B10 e01
    stw r1, reg[r0, #0x2e01]
    stw r1, reg[r0, #0x2e02]
    stw r1, reg[r0, #0x2e03]
    mov r3, r1
    stw r3, reg[r0, #0x2e00]
```

