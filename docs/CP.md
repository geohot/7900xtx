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

## umr --top

```
([amd744c]) (sample @ 1ms, report @ 100ms) -- Sat Apr  6 22:08:13 2024

GRBM Bits:
                 TA =>    25.0 % |                GDS =>     0.0 %
                 SX =>     0.0 % |                SPI =>   100.0 %
                BCI =>     0.0 % |                 SC =>     0.0 %
                 PA =>     0.0 % |                 DB =>     0.0 %
       CP_COHERENCY =>     0.0 % |                 CP =>   100.0 %
                 CB =>     0.0 % |                GUI =>   100.0 %
                 GE =>     0.0 % |                RLC =>   100.0 %
                CPF =>   100.0 % |                CPC =>   100.0 %
                CPG =>     0.0 % |

GFX PWR Bits:
          GFX_POWER =>   100.0 % |          GFX_CLOCK =>   100.0 %
             GFX_LS =>     0.0 % | GFX_PIPELINE_POWER =>   100.0 %

Sensors Bits:
           GFX_SCLK =>  3052 MHz |           GFX_MCLK =>    96 MHz
            VDD_GFX =>     1.127 |           GPU_LOAD =>   100 %
           MEM_LOAD =>     0 %   |           GPU_TEMP =>    56 C

TA Bits:
                 IN =>     0.0 % |                 FG =>     0.0 %
                 LA =>     0.0 % |                 FL =>     0.0 %
                 TA =>     0.0 % |                 FA =>     0.0 %
                 AL =>     0.0 % |

UVD Bits:
          UDEC_SCLK =>     0.0 % |         MPEG2_SCLK =>     0.0 %
          IDCT_SCLK =>     0.0 % |          MPRD_SCLK =>     0.0 %
           MPC_SCLK =>     0.0 % |

DRM Bits:
        BYTES_MOVED => 1484.190 g |         VRAM_USAGE => 726.734 m
          GTT_USAGE =>  16.602 m |           VIS_VRAM => 726.734 m
          EVICTIONS =>     2     |    FENCES_SIGNALED =>     0
     FENCES_EMITTED =>     0     |       FENCES_DELTA =>     0

VRAM: 0/413068234730 vis 105745439918023/24525 (MiB)
   python3:(52984)               :          0 KiB VRAM,          0 KiB vis VRAM,          0 KiB GTT
   umr:(52978)                   :          0 KiB VRAM,          0 KiB vis VRAM,          0 KiB GTT

(a)ll (w)ide (1)high_precision (2)high_frequency (W)rite (l)ogger
(v)ram d(r)m
(u)vd v(c)e (G)FX_PWR (s)GRBM (t)a v(g)t (m)emory_hub
s(d)ma se(n)sors
```

## All GFX register groups

```
amd744c.gfx1100.regCB
amd744c.gfx1100.regCC
amd744c.gfx1100.regCGTS
amd744c.gfx1100.regCGTT
amd744c.gfx1100.regCHA
amd744c.gfx1100.regCHCG
amd744c.gfx1100.regCHC
amd744c.gfx1100.regCHICKEN
amd744c.gfx1100.regCHI
amd744c.gfx1100.regCH
amd744c.gfx1100.regCOHER
amd744c.gfx1100.regCOMPUTE <- compute control here
amd744c.gfx1100.regCONFIG
amd744c.gfx1100.regCONTEXT
amd744c.gfx1100.regCPC
amd744c.gfx1100.regCPF
amd744c.gfx1100.regCPG
amd744c.gfx1100.regCP <- hardware queues here
amd744c.gfx1100.regDB
amd744c.gfx1100.regDIDT
amd744c.gfx1100.regEDC
amd744c.gfx1100.regGB
amd744c.gfx1100.regGCEA
amd744c.gfx1100.regGCMC
amd744c.gfx1100.regGCRD
amd744c.gfx1100.regGCR
amd744c.gfx1100.regGCUTCL2
amd744c.gfx1100.regGCUTC
amd744c.gfx1100.regGCVML2
amd744c.gfx1100.regGCVM
amd744c.gfx1100.regGC
amd744c.gfx1100.regGDS
amd744c.gfx1100.regGE1
amd744c.gfx1100.regGE2
amd744c.gfx1100.regGE
amd744c.gfx1100.regGFX
amd744c.gfx1100.regGL1A
amd744c.gfx1100.regGL1C
amd744c.gfx1100.regGL1H
amd744c.gfx1100.regGL1I
amd744c.gfx1100.regGL1
amd744c.gfx1100.regGL2A
amd744c.gfx1100.regGL2C
amd744c.gfx1100.regGL2
amd744c.gfx1100.regGRBM
amd744c.gfx1100.regGRTAVFS
amd744c.gfx1100.regGUS
amd744c.gfx1100.regIA
amd744c.gfx1100.regICG
amd744c.gfx1100.regLDS
amd744c.gfx1100.regPA
amd744c.gfx1100.regPCC
amd744c.gfx1100.regPC
amd744c.gfx1100.regPMM
amd744c.gfx1100.regPWRBRK
amd744c.gfx1100.regRLC <- RunList Controller
amd744c.gfx1100.regRMI
amd744c.gfx1100.regRTAVFS
amd744c.gfx1100.regSCRATCH
amd744c.gfx1100.regSDMA0
amd744c.gfx1100.regSDMA1
amd744c.gfx1100.regSE0
amd744c.gfx1100.regSE1
amd744c.gfx1100.regSE2
amd744c.gfx1100.regSE3
amd744c.gfx1100.regSE4
amd744c.gfx1100.regSE5
amd744c.gfx1100.regSEDC
amd744c.gfx1100.regSE
amd744c.gfx1100.regSH
amd744c.gfx1100.regSMU
amd744c.gfx1100.regSPI
amd744c.gfx1100.regSP
amd744c.gfx1100.regSQC
amd744c.gfx1100.regSQG
amd744c.gfx1100.regSQ <- information about waves
amd744c.gfx1100.regSX
amd744c.gfx1100.regTA <- Texture Addresser
amd744c.gfx1100.regTCP
amd744c.gfx1100.regTD
amd744c.gfx1100.regUCONFIG
amd744c.gfx1100.regUTCL1
amd744c.gfx1100.regVGT
amd744c.gfx1100.regVIOLATION
amd744c.gfx1100.regWD
```
