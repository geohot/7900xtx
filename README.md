# Documentation for the 7900XTX
aka Navi31 aka Plum Bonito aka amd744c

- PSP = Platform Security Processor (ARM)
  - SOS = Secure Operating System (psp_13_0_0_sos.bin)
  - TA = Trusted Application (psp_13_0_0_ta.bin)
  - KDB
  - TMR = Trusted Memory Region
- SMU = System Management Unit (smuio1306) (amdgpu/smu_13_0_0.bin)
- DCN = Display Core Next (dcn320) (amdgpu/dcn_3_2_0_dmcub.bin)
- GC = Graphics and Compute (gfx1100)
  - CP (Command Processor) = PFP,ME,CE,MEC (PFP+ME = Drawing Engine)
  - PFP = Pre-Fetch Parser (gc_11_0_0_pfp.bin)
  - ME = Micro Engine (gc_11_0_0_me.bin)
  - RLC = RunList Controller (gc_11_0_0_rlc.bin)
  - MEC = Micro Engine Compute (gc_11_0_0_mec.bin)
  - [MES](/docs/MES.md) = Micro Engine Scheduler (gc_11_0_0_mes1.bin) (gc_11_0_0_mes_2.bin)
  - IMU = Integrated Memory Controller Utility (gc_11_0_0_imu.bin)
  - CE = Constant Engine
- VCN = Video Core Next (encoder/decoder) (vcn400) (vcn_4_0_0.bin)
- SDMA = System DMA (lsdma600) (sdma_6_0_0.bin)

More info on each piece:
https://mjmwired.net/kernel/Documentation/gpu/amdgpu/driver-core.rst

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
- https://martty.github.io/posts/radbg_part_4/
- https://www.phoronix.com/news/AMDGPU-LSDMA-Light-SDMA
- https://gpuopen.com/presentations/2023/RDNA3_Beyond-the-current-gen-v4.pdf
- https://bu-icsg.github.io/publications/2022/navisim_pact_2022.pdf
- https://gpuopen.com/rdna/

## More Acronyms

- MQD: Memory Queue Descriptor
- GMC: Graphic Memory Controller

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
