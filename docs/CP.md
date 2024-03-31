# Command Processor

PFP,ME,CE,MEC (PFP+ME = Drawing Engine)

## What arch is the firmware?

- The PSP is ARM
- SDMA+RLC are F32 -- see: https://github.com/fail0verflow/radeon-tools
- Others (like MEC) are RS64 -- no known docs on this ISA

## Random notes

`watch -n 0.1 'sudo umr -s amd744c.gfx1100 | grep INSTR_PNTR'`

```
amd744c.gfx1100.regCP_GFX_RS64_INSTR_PNTR0 == 0x00000f05
amd744c.gfx1100.regCP_GFX_RS64_INSTR_PNTR1 == 0x00000f5e
amd744c.gfx1100.regCP_MEC1_INSTR_PNTR == 0x00000000
amd744c.gfx1100.regCP_MEC2_INSTR_PNTR == 0x00000000
amd744c.gfx1100.regCP_MEC_RS64_INSTR_PNTR == 0x00009123
amd744c.gfx1100.regCP_MES_INSTR_PNTR == 0x000092b4
amd744c.gfx1100.regCP_ME_INSTR_PNTR == 0x00000c00
amd744c.gfx1100.regCP_PFP_INSTR_PNTR == 0x00000c00
```

Only regCP_MEC_RS64_INSTR_PNTR changes during operation

/lib/firmware/amdgpu/gc_11_0_0_mec.bin

`xxd -g4 /lib/firmware/amdgpu/gc_11_0_0_mec.bin | less`

0x00009123*4 -> 0x2448c

- MEC starts at 0x3000
- MES starts at 0x5000
