# Documentation for the 7900XTX
aka Navi31 aka gfx1100 aka Plum Bonito aka amd744c

- [PSP](/docs/PSP.md) = Platform Security Processor (ARM)
  - SOS = Secure Operating System (psp_13_0_0_sos.bin)
  - TA = Trusted Application (psp_13_0_0_ta.bin)
  - KDB = Key DataBase
  - TMR = Trusted Memory Region
- SMU = System Management Unit (smuio1306) (amdgpu/smu_13_0_0.bin) (RS64?)
- GC = Graphics and Compute (gfx1100)
  - [CP](/docs/CP.md) (Command Processor) = an umbrella term for the PFP,ME,MEC,MES
  - Drawing Engine (idle during compute)
    - PFP = Pre-Fetch Parser (gc_11_0_0_pfp.bin)
    - ME = Micro Engine (gc_11_0_0_me.bin)
  - RLC = RunList Controller (gc_11_0_0_rlc.bin) (F32)
  - [MEC](/docs/MEC.md) = Micro Engine Compute (gc_11_0_0_mec.bin) (RS64)
  - [MES](/docs/MES.md) = Micro Engine Scheduler (gc_11_0_0_mes1.bin) (gc_11_0_0_mes_2.bin) (RS64)
  - IMU = Integrated Memory Controller Utility (gc_11_0_0_imu.bin)
- DCN = Display Core Next (dcn320) (amdgpu/dcn_3_2_0_dmcub.bin)
- VCN = Video Core Next (encoder/decoder) (vcn400) (vcn_4_0_0.bin)
- [SDMA](/docs/SDMA.md) = System DMA (lsdma600) (sdma_6_0_0.bin) (F32)

More info on each piece:
https://mjmwired.net/kernel/Documentation/gpu/amdgpu/driver-core.rst

RS64 = RISCV/RV64I + a few custom instructions! Load (at least MEC) with offset 0x200

## Documenting Flows

- [Launching a kernel](/docs/launching.md)
- Device/Firmware bringup

## Architechture Diagram

![](/docs/arch1.jpg)

- 1x 5nm GCD (graphics compute die)
- 6x 6nm MCD (memory cache die)
- More about the [Compute Unit](/docs/CU.md)

## Dumping registers

```bash
# list regs with bits
sudo umr -lr amd744c.gfx1100 -O bits

# dump regs
sudo umr -s amd744c.gfx1100
```

## umr --top

```
GRBM (Graphics Register Backbone Manager) Bits:
                 TA =>    95.0 % |                GDS =>     0.0 %
                 SX =>     0.0 % |                SPI =>    96.0 %
                BCI =>     0.0 % |                 SC =>     0.0 %
                 PA =>     0.0 % |                 DB =>     0.0 %
       CP_COHERENCY =>     0.0 % |                 CP =>    97.0 %
                 CB =>     0.0 % |                GUI =>    97.0 %
                 GE =>     0.0 % |                RLC =>    96.0 %
                CPF =>    97.0 % |                CPC =>    97.0 %
                CPG =>     0.0 % |

TA (Texture Addresser) Bits:
                 IN =>    33.0 % |                 FG =>     0.0 %
                 LA =>     0.0 % |                 FL =>     0.0 %
                 TA =>     0.0 % |                 FA =>    44.0 %
                 AL =>    70.0 % |
```

## Installing AMDGPU

```bash
sudo apt-get install linux-generic-hwe-22.04
# add user to render+video groups
```

## Rebuilding amdgpu kernel module

https://imil.net/blog/posts/2022/build-a-single-in-tree-linux-kernel-module-debian--clones/

```bash
sudo rmmod amdgpu && make -C . M=drivers/gpu/drm/amd/amdgpu && sudo insmod drivers/gpu/drm/amd/amdgpu/amdgpu.ko
# gpu_recovery doesn't seem to work
#sudo modprobe amdgpu gpu_recovery=0
```

Enable debug prints in dmesg

```bash
sudo su -c "echo 'file drivers/gpu/drm/amd/* +p' > /sys/kernel/debug/dynamic_debug/control"
echo 0x19F | sudo tee /sys/module/drm/parameters/debug # Enable verbose DRM logging
HSAKMT_DEBUG_LEVEL=7  # user space debugging
```

## Links

- https://www.amd.com/content/dam/amd/en/documents/radeon-tech-docs/instruction-set-architectures/rdna3-shader-instruction-set-architecture-feb-2023_0.pdf
- https://lists.freedesktop.org/archives/amd-gfx/2022-April/078410.html
- https://docs.kernel.org/gpu/amdgpu/driver-core.html
- https://wiki.gentoo.org/wiki/AMDGPU
- https://mjmwired.net/kernel/Documentation/gpu/amdgpu/driver-core.rst
- https://www.kernel.org/doc/html/v6.8/gpu/amdgpu/amdgpu-glossary.html
- https://github.com/amezin/amdgpu-pptable
- https://themaister.net/blog/2023/08/20/hardcore-vulkan-debugging-digging-deep-on-linux-amdgpu/
- https://martty.github.io/posts/radbg_part_3/
- https://martty.github.io/posts/radbg_part_4/
- https://www.phoronix.com/news/AMDGPU-LSDMA-Light-SDMA
- https://gpuopen.com/presentations/2023/RDNA3_Beyond-the-current-gen-v4.pdf
- https://bu-icsg.github.io/publications/2022/navisim_pact_2022.pdf
- https://gpuopen.com/rdna/
- https://github.com/fail0verflow/radeon-tools
- https://github.com/gnif/vendor-reset
- https://sourceware.org/gdb/current/onlinedocs/gdb.html/AMD-GPU.html
- https://www.x.org/docs/AMD/old/R5xx_Acceleration_v1.2.pdf
- https://www.amd.com/content/dam/amd/en/documents/radeon-tech-docs/programmer-references/si_programming_guide_v2.pdf
- https://old.gem5.org/wiki/images/1/19/AMD_gem5_APU_simulator_isca_2018_gem5_wiki.pdf

## More Acronyms

- MQD: Memory Queue Descriptor
- GMC: Graphic Memory Controller
- BACO: Bus Active, Chip Off
- VMID: Virtual Memory Identifiers (Each VMID is associated with its own page table.)
  - 0 - GFX hub
  - 1 - MM hub
  - 2 - VC0 hub
  - 3 - VC1 hub
  - 8 and 9 - User programs?
- HQD: Hardware Queue Descriptor
- PQ: Packet Queue
- HWS: HardWare Scheduling
- EOP: End Of Pipe/Pipeline
- SRBM: System Register Bus Manager
- GRBM: Graphics Register Bus Manager
- HDP: Host Data Port
- gfxhub (see APU simulator docs)
  - TCP: Texture Cache per Pipe (private L1 data)
  - SQC (inst): Sequencer Cache (shared L1 instruction)
  - SQC (data): Sequencer Cache (shared L1 data)
- TCC: Texture Cache per Channel (shared L2)
- CWSR: Compute Wave Store and Resume [code](https://lists.freedesktop.org/archives/amd-gfx/2017-November/016069.html)

## Listing IP blocks

```
kafka@q:/sys/class/drm/card0/device/fw_version$ sudo umr -lb
[WARNING]: Unknown ASIC [amd744c] should be added to pci.did to get proper name
        amd744c.df421{5} (4.2.1)
        amd744c.df421{3} (4.2.1)
        amd744c.df421{1} (4.2.1)
        amd744c.df421{6} (4.2.1)
        amd744c.df421{4} (4.2.1)
        amd744c.df421{2} (4.2.1)
        amd744c.df420 (4.2.0)
        amd744c.mp11300 (13.0.0)
        amd744c.lsdma600 (6.0.0)
        amd744c.mmhub300 (3.0.0)
        amd744c.osssys600 (6.0.0)
        amd744c.vcn401{1} (4.0.1)
        amd744c.vcn400 (4.0.0)
        amd744c.hdp600 (6.0.0)
        amd744c.smuio1306 (13.0.6)
        amd744c.nbio430 (4.3.0)
        amd744c.athub300 (3.0.0)
        amd744c.dcn320 (3.2.0)
        amd744c.thm1305{5} (13.0.5)
        amd744c.thm1305{3} (13.0.5)
        amd744c.thm1305{1} (13.0.5)
        amd744c.thm1305{6} (13.0.5)
        amd744c.thm1305{4} (13.0.5)
        amd744c.thm1305{2} (13.0.5)
        amd744c.thm1303 (13.0.3)
        amd744c.mp01300 (13.0.0)
        amd744c.umc8100{5} (8.10.0)
        amd744c.umc8100{3} (8.10.0)
        amd744c.umc8100{1} (8.10.0)
        amd744c.umc8100{4} (8.10.0)
        amd744c.umc8100{2} (8.10.0)
        amd744c.umc8100{0} (8.10.0)
        amd744c.gfx1100 (11.0.0)
```

```
[46444.513680] [drm] amdgpu kernel modesetting enabled.
[46444.513978] amdgpu: CRAT table disabled by module option
[46444.513986] amdgpu: Virtual CRAT table created for CPU
[46444.514013] amdgpu: Topology: Add CPU node
[46444.514595] [drm] initializing kernel modesetting (IP DISCOVERY 0x1002:0x744C 0x1002:0x0E3B 0xC8).
[46444.514638] [drm] register mmio base: 0xFB300000
[46444.514641] [drm] register mmio size: 1048576
[46444.520723] [drm] add ip block number 0 <soc21_common>
[46444.520729] [drm] add ip block number 1 <gmc_v11_0>
[46444.520733] [drm] add ip block number 2 <ih_v6_0>
[46444.520735] [drm] add ip block number 3 <psp>
[46444.520737] [drm] add ip block number 4 <smu>
[46444.520740] [drm] add ip block number 5 <dm>
[46444.520742] [drm] add ip block number 6 <gfx_v11_0>
[46444.520745] [drm] add ip block number 7 <sdma_v6_0>
[46444.520747] [drm] add ip block number 8 <vcn_v4_0>
[46444.520749] [drm] add ip block number 9 <jpeg_v4_0>
[46444.520752] [drm] add ip block number 10 <mes_v11_0>
```

```
root@q:/sys/kernel/debug/dri/0# cat amdgpu_firmware_info
VCE feature version: 0, firmware version: 0x00000000
UVD feature version: 0, firmware version: 0x00000000
MC feature version: 0, firmware version: 0x00000000
ME feature version: 29, firmware version: 0x000005da
PFP feature version: 29, firmware version: 0x00000605
CE feature version: 0, firmware version: 0x00000000
RLC feature version: 1, firmware version: 0x00000074
RLC SRLC feature version: 0, firmware version: 0x00000000
RLC SRLG feature version: 0, firmware version: 0x00000000
RLC SRLS feature version: 0, firmware version: 0x00000000
RLCP feature version: 1, firmware version: 0x00000019
RLCV feature version: 1, firmware version: 0x00000022
MEC feature version: 29, firmware version: 0x000001fe
IMU feature version: 0, firmware version: 0x0b1f3600
SOS feature version: 3211301, firmware version: 0x00310025
ASD feature version: 553648282, firmware version: 0x2100009a
TA XGMI feature version: 0x00000000, firmware version: 0x00000000
TA RAS feature version: 0x00000000, firmware version: 0x1b000201
TA HDCP feature version: 0x00000000, firmware version: 0x17000031
TA DTM feature version: 0x00000000, firmware version: 0x12000013
TA RAP feature version: 0x00000000, firmware version: 0x00000000
TA SECUREDISPLAY feature version: 0x00000000, firmware version: 0x00000000
SMC feature version: 0, program: 0, firmware version: 0x004e5500 (78.85.0)
SDMA0 feature version: 60, firmware version: 0x00000013
SDMA1 feature version: 60, firmware version: 0x00000013
VCN feature version: 0, firmware version: 0x0510b023
DMCU feature version: 0, firmware version: 0x00000000
DMCUB feature version: 0, firmware version: 0x07000a01
TOC feature version: 12, firmware version: 0x0000000c
MES_KIQ feature version: 6, firmware version: 0x0000006a
MES feature version: 1, firmware version: 0x00000034
VBIOS version: 113-D7020100-102
```

```
[80568.560601] amdgpu_ucode_request amdgpu/psp_13_0_0_sos.bin
[80568.560737] amdgpu_ucode_request amdgpu/psp_13_0_0_ta.bin
[80568.560917] amdgpu_ucode_request amdgpu/smu_13_0_0.bin
[80568.561082] amdgpu_ucode_request amdgpu/dcn_3_2_0_dmcub.bin
[80568.561225] amdgpu_ucode_request amdgpu/gc_11_0_0_pfp.bin
[80568.561362] amdgpu_ucode_request amdgpu/gc_11_0_0_me.bin
[80568.561491] amdgpu_ucode_request amdgpu/gc_11_0_0_rlc.bin
[80568.561765] amdgpu_ucode_request amdgpu/gc_11_0_0_mec.bin
[80568.562034] amdgpu_ucode_request amdgpu/vcn_4_0_0.bin
[80568.562398] amdgpu_ucode_request amdgpu/gc_11_0_0_mes_2.bin
[80568.562537] amdgpu_ucode_request amdgpu/gc_11_0_0_mes1.bin
[80569.088855] amdgpu_ucode_request amdgpu/gc_11_0_0_imu.bin
[80569.089068] amdgpu_ucode_request amdgpu/sdma_6_0_0.bin
```

```
kafka@q:~/7900xtx/fwinfo$ ./go.sh
/lib/firmware/amdgpu/psp_13_0_0_sos.bin  size_bytes:0x41810 ucode_size_bytes:0x41710
/lib/firmware/amdgpu/psp_13_0_0_ta.bin   size_bytes:0x39500 ucode_size_bytes:0x39400
/lib/firmware/amdgpu/smu_13_0_0.bin      size_bytes:0x47664 ucode_size_bytes:0x3fe00
/lib/firmware/amdgpu/gc_11_0_0_pfp.bin   size_bytes:0x32C70 ucode_size_bytes:0x32b70
/lib/firmware/amdgpu/gc_11_0_0_me.bin    size_bytes:0x2E450 ucode_size_bytes:0x2e350
/lib/firmware/amdgpu/gc_11_0_0_rlc.bin   size_bytes:0x2D2A0 ucode_size_bytes:0x6200
/lib/firmware/amdgpu/gc_11_0_0_mec.bin   size_bytes:0x63620 ucode_size_bytes:0x63520
/lib/firmware/amdgpu/gc_11_0_0_mes_2.bin size_bytes:0x46A00 ucode_size_bytes:0x46900
/lib/firmware/amdgpu/gc_11_0_0_mes1.bin  size_bytes:0x33AF0 ucode_size_bytes:0x339f0
/lib/firmware/amdgpu/gc_11_0_0_imu.bin   size_bytes:0x20500 ucode_size_bytes:0x20400
/lib/firmware/amdgpu/dcn_3_2_0_dmcub.bin size_bytes:0x41790 ucode_size_bytes:0x41690
/lib/firmware/amdgpu/vcn_4_0_0.bin       size_bytes:0x5DD50 ucode_size_bytes:0x5dc50
/lib/firmware/amdgpu/sdma_6_0_0.bin      size_bytes:0x 8700 ucode_size_bytes:0x8600
```

## Firmware loads

```
[ 1370.296802] psp_prep_load_ip_fw_cmd_buf: 0000000000C49000  type:18 sz:0x3fe00  # GFX_FW_TYPE_SMU
[ 1431.136232] psp_prep_load_ip_fw_cmd_buf: 0000000000C49000  type:18 sz:0x3fe00  # GFX_FW_TYPE_SMU
[ 1432.229979] psp_prep_load_ip_fw_cmd_buf: 0000000000A00000  type:71 sz:0x4400   # GFX_FW_TYPE_SDMA_UCODE_TH0
[ 1432.234035] psp_prep_load_ip_fw_cmd_buf: 0000000000A05000  type:72 sz:0x4200   # GFX_FW_TYPE_SDMA_UCODE_TH1
[ 1432.237930] psp_prep_load_ip_fw_cmd_buf: 0000000000A0A000  type:87 sz:0x10b70  # GFX_FW_TYPE_RS64_PFP
[ 1432.242088] psp_prep_load_ip_fw_cmd_buf: 0000000000A1B000  type:88 sz:0xc350   # GFX_FW_TYPE_RS64_ME
[ 1432.246220] psp_prep_load_ip_fw_cmd_buf: 0000000000A28000  type:89 sz:0x41520  # GFX_FW_TYPE_RS64_MEC
[ 1432.252719] psp_prep_load_ip_fw_cmd_buf: 0000000000A6A000  type:90 sz:0x22000  # GFX_FW_TYPE_RS64_PFP_P0_STACK
[ 1432.256295] psp_prep_load_ip_fw_cmd_buf: 0000000000A8C000  type:91 sz:0x22000  # GFX_FW_TYPE_RS64_PFP_P1_STACK
[ 1432.259908] psp_prep_load_ip_fw_cmd_buf: 0000000000AAE000  type:92 sz:0x22000  # GFX_FW_TYPE_RS64_ME_P0_STACK
[ 1432.263390] psp_prep_load_ip_fw_cmd_buf: 0000000000AD0000  type:93 sz:0x22000  # GFX_FW_TYPE_RS64_ME_P1_STACK
[ 1432.267162] psp_prep_load_ip_fw_cmd_buf: 0000000000AF2000  type:94 sz:0x22000  # GFX_FW_TYPE_RS64_MEC_P0_STACK
[ 1432.271029] psp_prep_load_ip_fw_cmd_buf: 0000000000B14000  type:95 sz:0x22000  # GFX_FW_TYPE_RS64_MEC_P1_STACK
[ 1432.274775] psp_prep_load_ip_fw_cmd_buf: 0000000000B36000  type:96 sz:0x22000  # GFX_FW_TYPE_RS64_MEC_P2_STACK
[ 1432.278344] psp_prep_load_ip_fw_cmd_buf: 0000000000B58000  type:97 sz:0x22000  # GFX_FW_TYPE_RS64_MEC_P3_STACK
[ 1432.281782] psp_prep_load_ip_fw_cmd_buf: 0000000000B7A000  type:33 sz:0x26900  # GFX_FW_TYPE_CP_MES
[ 1432.286907] psp_prep_load_ip_fw_cmd_buf: 0000000000BA1000  type:34 sz:0x20000  # GFX_FW_TYPE_MES_STACK
[ 1432.290773] psp_prep_load_ip_fw_cmd_buf: 0000000000BC1000  type:81 sz:0x139f0  # GFX_FW_TYPE_CP_MES_KIQ
[ 1432.295392] psp_prep_load_ip_fw_cmd_buf: 0000000000BD5000  type:82 sz:0x20000  # GFX_FW_TYPE_MES_KIQ_STACK
[ 1432.299012] psp_prep_load_ip_fw_cmd_buf: 0000000000BF5000  type:68 sz:0x10200  # GFX_FW_TYPE_IMU_I
[ 1432.303549] psp_prep_load_ip_fw_cmd_buf: 0000000000C06000  type:69 sz:0x10200  # GFX_FW_TYPE_IMU_D
[ 1432.307778] psp_prep_load_ip_fw_cmd_buf: 0000000000C17000  type:20 sz:0xa00    # GFX_FW_TYPE_RLC_RESTORE_LIST_GPM_MEM
[ 1432.311519] psp_prep_load_ip_fw_cmd_buf: 0000000000C18000  type:21 sz:0x8da0   # GFX_FW_TYPE_RLC_RESTORE_LIST_SRM_MEM
[ 1432.315520] psp_prep_load_ip_fw_cmd_buf: 0000000000C21000  type:26 sz:0x10200  # GFX_FW_TYPE_RLC_IRAM
[ 1432.319925] psp_prep_load_ip_fw_cmd_buf: 0000000000C32000  type:48 sz:0x8200   # GFX_FW_TYPE_RLC_DRAM_BOOT
[ 1432.323649] psp_prep_load_ip_fw_cmd_buf: 0000000000C3B000  type:25 sz:0x2200   # GFX_FW_TYPE_RLC_P
[ 1432.327185] psp_prep_load_ip_fw_cmd_buf: 0000000000C3E000  type:7 sz:0x3200    # GFX_FW_TYPE_RLC_V
[ 1432.331122] psp_prep_load_ip_fw_cmd_buf: 0000000000C42000  type:8 sz:0x6200    # GFX_FW_TYPE_RLC_G
[ 1432.335348] psp_prep_load_ip_fw_cmd_buf: 0000000000C89000  type:13 sz:0x5dc50  # GFX_FW_TYPE_VCN
[ 1432.343011] psp_prep_load_ip_fw_cmd_buf: 0000000000CE7000  type:58 sz:0x5dc50  # GFX_FW_TYPE_VCN1
[ 1432.350895] psp_prep_load_ip_fw_cmd_buf: 0000000000D45000  type:51 sz:0x41690  # GFX_FW_TYPE_DMUB
```

```C
/* FW types for GFX_CMD_ID_LOAD_IP_FW command. Limit 31. */
enum psp_gfx_fw_type {
	GFX_FW_TYPE_NONE        = 0,    /* */
	GFX_FW_TYPE_CP_ME       = 1,    /* CP-ME                    VG + RV */
	GFX_FW_TYPE_CP_PFP      = 2,    /* CP-PFP                   VG + RV */
	GFX_FW_TYPE_CP_CE       = 3,    /* CP-CE                    VG + RV */
	GFX_FW_TYPE_CP_MEC      = 4,    /* CP-MEC FW                VG + RV */
	GFX_FW_TYPE_CP_MEC_ME1  = 5,    /* CP-MEC Jump Table 1      VG + RV */
	GFX_FW_TYPE_CP_MEC_ME2  = 6,    /* CP-MEC Jump Table 2      VG      */
	GFX_FW_TYPE_RLC_V       = 7,    /* RLC-V                    VG      */
	GFX_FW_TYPE_RLC_G       = 8,    /* RLC-G                    VG + RV */
	GFX_FW_TYPE_SDMA0       = 9,    /* SDMA0                    VG + RV */
	GFX_FW_TYPE_SDMA1       = 10,   /* SDMA1                    VG      */
	GFX_FW_TYPE_DMCU_ERAM   = 11,   /* DMCU-ERAM                VG + RV */
	GFX_FW_TYPE_DMCU_ISR    = 12,   /* DMCU-ISR                 VG + RV */
	GFX_FW_TYPE_VCN         = 13,   /* VCN                           RV */
	GFX_FW_TYPE_UVD         = 14,   /* UVD                      VG      */
	GFX_FW_TYPE_VCE         = 15,   /* VCE                      VG      */
	GFX_FW_TYPE_ISP         = 16,   /* ISP                           RV */
	GFX_FW_TYPE_ACP         = 17,   /* ACP                           RV */
	GFX_FW_TYPE_SMU         = 18,   /* SMU                      VG      */
	GFX_FW_TYPE_MMSCH       = 19,   /* MMSCH                    VG      */
	GFX_FW_TYPE_RLC_RESTORE_LIST_GPM_MEM        = 20,   /* RLC GPM                  VG + RV */
	GFX_FW_TYPE_RLC_RESTORE_LIST_SRM_MEM        = 21,   /* RLC SRM                  VG + RV */
	GFX_FW_TYPE_RLC_RESTORE_LIST_SRM_CNTL       = 22,   /* RLC CNTL                 VG + RV */
	GFX_FW_TYPE_UVD1        = 23,   /* UVD1                     VG-20   */
	GFX_FW_TYPE_TOC         = 24,   /* TOC                      NV-10   */
	GFX_FW_TYPE_RLC_P                           = 25,   /* RLC P                    NV      */
	GFX_FW_TYPE_RLC_IRAM                        = 26,   /* RLC_IRAM                 NV      */
	GFX_FW_TYPE_GLOBAL_TAP_DELAYS               = 27,   /* GLOBAL TAP DELAYS        NV      */
	GFX_FW_TYPE_SE0_TAP_DELAYS                  = 28,   /* SE0 TAP DELAYS           NV      */
	GFX_FW_TYPE_SE1_TAP_DELAYS                  = 29,   /* SE1 TAP DELAYS           NV      */
	GFX_FW_TYPE_GLOBAL_SE0_SE1_SKEW_DELAYS      = 30,   /* GLOBAL SE0/1 SKEW DELAYS NV      */
	GFX_FW_TYPE_SDMA0_JT                        = 31,   /* SDMA0 JT                 NV      */
	GFX_FW_TYPE_SDMA1_JT                        = 32,   /* SDNA1 JT                 NV      */
	GFX_FW_TYPE_CP_MES                          = 33,   /* CP MES                   NV      */
	GFX_FW_TYPE_MES_STACK                       = 34,   /* MES STACK                NV      */
	GFX_FW_TYPE_RLC_SRM_DRAM_SR                 = 35,   /* RLC SRM DRAM             NV      */
	GFX_FW_TYPE_RLCG_SCRATCH_SR                 = 36,   /* RLCG SCRATCH             NV      */
	GFX_FW_TYPE_RLCP_SCRATCH_SR                 = 37,   /* RLCP SCRATCH             NV      */
	GFX_FW_TYPE_RLCV_SCRATCH_SR                 = 38,   /* RLCV SCRATCH             NV      */
	GFX_FW_TYPE_RLX6_DRAM_SR                    = 39,   /* RLX6 DRAM                NV      */
	GFX_FW_TYPE_SDMA0_PG_CONTEXT                = 40,   /* SDMA0 PG CONTEXT         NV      */
	GFX_FW_TYPE_SDMA1_PG_CONTEXT                = 41,   /* SDMA1 PG CONTEXT         NV      */
	GFX_FW_TYPE_GLOBAL_MUX_SELECT_RAM           = 42,   /* GLOBAL MUX SEL RAM       NV      */
	GFX_FW_TYPE_SE0_MUX_SELECT_RAM              = 43,   /* SE0 MUX SEL RAM          NV      */
	GFX_FW_TYPE_SE1_MUX_SELECT_RAM              = 44,   /* SE1 MUX SEL RAM          NV      */
	GFX_FW_TYPE_ACCUM_CTRL_RAM                  = 45,   /* ACCUM CTRL RAM           NV      */
	GFX_FW_TYPE_RLCP_CAM                        = 46,   /* RLCP CAM                 NV      */
	GFX_FW_TYPE_RLC_SPP_CAM_EXT                 = 47,   /* RLC SPP CAM EXT          NV      */
	GFX_FW_TYPE_RLC_DRAM_BOOT                   = 48,   /* RLC DRAM BOOT            NV      */
	GFX_FW_TYPE_VCN0_RAM                        = 49,   /* VCN_RAM                  NV + RN */
	GFX_FW_TYPE_VCN1_RAM                        = 50,   /* VCN_RAM                  NV + RN */
	GFX_FW_TYPE_DMUB                            = 51,   /* DMUB                          RN */
	GFX_FW_TYPE_SDMA2                           = 52,   /* SDMA2                    MI      */
	GFX_FW_TYPE_SDMA3                           = 53,   /* SDMA3                    MI      */
	GFX_FW_TYPE_SDMA4                           = 54,   /* SDMA4                    MI      */
	GFX_FW_TYPE_SDMA5                           = 55,   /* SDMA5                    MI      */
	GFX_FW_TYPE_SDMA6                           = 56,   /* SDMA6                    MI      */
	GFX_FW_TYPE_SDMA7                           = 57,   /* SDMA7                    MI      */
	GFX_FW_TYPE_VCN1                            = 58,   /* VCN1                     MI      */
	GFX_FW_TYPE_CAP                             = 62,   /* CAP_FW                           */
	GFX_FW_TYPE_SE2_TAP_DELAYS                  = 65,   /* SE2 TAP DELAYS           NV      */
	GFX_FW_TYPE_SE3_TAP_DELAYS                  = 66,   /* SE3 TAP DELAYS           NV      */
	GFX_FW_TYPE_REG_LIST                        = 67,   /* REG_LIST                 MI      */
	GFX_FW_TYPE_IMU_I                           = 68,   /* IMU Instruction FW       SOC21   */
	GFX_FW_TYPE_IMU_D                           = 69,   /* IMU Data FW              SOC21   */
	GFX_FW_TYPE_LSDMA                           = 70,   /* LSDMA FW                 SOC21   */
	GFX_FW_TYPE_SDMA_UCODE_TH0                  = 71,   /* SDMA Thread 0/CTX        SOC21   */
	GFX_FW_TYPE_SDMA_UCODE_TH1                  = 72,   /* SDMA Thread 1/CTL        SOC21   */
	GFX_FW_TYPE_PPTABLE                         = 73,   /* PPTABLE                  SOC21   */
	GFX_FW_TYPE_DISCRETE_USB4                   = 74,   /* dUSB4 FW                 SOC21   */
	GFX_FW_TYPE_TA                              = 75,   /* SRIOV TA FW UUID         SOC21   */
	GFX_FW_TYPE_RS64_MES                        = 76,   /* RS64 MES ucode           SOC21   */
	GFX_FW_TYPE_RS64_MES_STACK                  = 77,   /* RS64 MES stack ucode     SOC21   */
	GFX_FW_TYPE_RS64_KIQ                        = 78,   /* RS64 KIQ ucode           SOC21   */
	GFX_FW_TYPE_RS64_KIQ_STACK                  = 79,   /* RS64 KIQ Heap stack      SOC21   */
	GFX_FW_TYPE_ISP_DATA                        = 80,   /* ISP DATA                 SOC21   */
	GFX_FW_TYPE_CP_MES_KIQ                      = 81,   /* MES KIQ ucode            SOC21   */
	GFX_FW_TYPE_MES_KIQ_STACK                   = 82,   /* MES KIQ stack            SOC21   */
	GFX_FW_TYPE_UMSCH_DATA                      = 83,   /* User Mode Scheduler Data SOC21   */
	GFX_FW_TYPE_UMSCH_UCODE                     = 84,   /* User Mode Scheduler Ucode SOC21  */
	GFX_FW_TYPE_UMSCH_CMD_BUFFER                = 85,   /* User Mode Scheduler Command Buffer SOC21 */
	GFX_FW_TYPE_USB_DP_COMBO_PHY                = 86,   /* USB-Display port Combo   SOC21   */
	GFX_FW_TYPE_RS64_PFP                        = 87,   /* RS64 PFP                 SOC21   */
	GFX_FW_TYPE_RS64_ME                         = 88,   /* RS64 ME                  SOC21   */
	GFX_FW_TYPE_RS64_MEC                        = 89,   /* RS64 MEC                 SOC21   */
	GFX_FW_TYPE_RS64_PFP_P0_STACK               = 90,   /* RS64 PFP stack P0        SOC21   */
	GFX_FW_TYPE_RS64_PFP_P1_STACK               = 91,   /* RS64 PFP stack P1        SOC21   */
	GFX_FW_TYPE_RS64_ME_P0_STACK                = 92,   /* RS64 ME stack P0         SOC21   */
	GFX_FW_TYPE_RS64_ME_P1_STACK                = 93,   /* RS64 ME stack P1         SOC21   */
	GFX_FW_TYPE_RS64_MEC_P0_STACK               = 94,   /* RS64 MEC stack P0        SOC21   */
	GFX_FW_TYPE_RS64_MEC_P1_STACK               = 95,   /* RS64 MEC stack P1        SOC21   */
	GFX_FW_TYPE_RS64_MEC_P2_STACK               = 96,   /* RS64 MEC stack P2        SOC21   */
	GFX_FW_TYPE_RS64_MEC_P3_STACK               = 97,   /* RS64 MEC stack P3        SOC21   */
	GFX_FW_TYPE_MAX
};
```
