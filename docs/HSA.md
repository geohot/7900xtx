# HSA stands for Heterogeneous System Architecture

[HSA](https://en.wikipedia.org/wiki/Heterogeneous_System_Architecture) is a cross-vendor set of specifications that allow for the integration of central processing units and graphics processors on the same bus, with shared memory and tasks.

Idea of HSA is to reduce communication latency between CPUs, GPUs and to make it easier to offload calculations to the GPU
![](/docs/img/gpu_with_hsa.png)

HSA defines a unified virtual address space for compute.

Usually GPU and CPU have their own memory, HSA requires them to share page tables, to exchange data by sharing pointers. Needs to be supported by HSA specific [memory management units](https://web.archive.org/web/20140328140823/http://amd-dev.wpengine.netdna-cdn.com/wordpress/media/2012/10/hsa10.pdf)

HSA should support both GPUs and CPUs and high-level languages.

The CPU's [MMU](https://en.wikipedia.org/wiki/Memory_management_unit) and the GPU's [IOMMU](https://en.wikipedia.org/wiki/IOMMU) must both comply with HSA hardware specifications.
![](/docs/img/mmu_iommu.png)

Some of the HSA-specific features implemented in the hardware need to be supported by the operating system kernel and specific device drivers.

`amdkfd` supports heterogeneous queuing (HQ), which aims to simplify the distribution of computational jobs among multiple CPUs and GPUs from the programmer's perspective. Support for heterogeneous memory management (HMM), suited only for graphics hardware featuring version 2 of the AMD's IOMMU,


## Graphics Core Next (GCN)

HSA kernel driver resides in the directory `/drivers/gpu/hsa`, while the DRM graphics device drivers reside in `/drivers/gpu/drm`

Hardware schedulers are used to perform scheduling and offload the assignment of compute queues to the ACEs from the driver to hardware, by buffering these queues until there is at least one empty queue in at least one ACE. This causes the HWS to immediately assign buffered queues to the ACEs until all queues are full or there are no more queues to safely assign

Part of the scheduling work performed includes prioritized queues which allow critical tasks to run at a higher priority than other tasks without requiring the lower priority tasks to be preempted to run the high priority task, therefore allowing the tasks to run concurrently with the high priority tasks scheduled to hog the GPU as much as possible while letting other tasks use the resources that the high priority tasks are not using. These are essentially Asynchronous Compute Engines that lack dispatch controllers. They were first introduced in the fourth generation [GCN](https://en.wikipedia.org/wiki/Graphics_Core_Next) microarchitectur

## Kernel dispatch

[Dispatching a kernel](https://llvm.org/docs/AMDGPUUsage.html#kernel-dispatch) can be done from a CPU hosted program or from an HSA kernel executing on a GPU
* Get pointer to AQL queue
* Get pointer to the kernel [descriptor](https://llvm.org/docs/AMDGPUUsage.html#amdgpu-amdhsa-kernel-descriptor), kernel must be part of code loaded by an HSA runtime, where the AQL queue is associated
* Space is allocated, atleast 16-byte aligned, for the kernel arguments
* Kernel arguments values are asssigned to allocated memory, according to [HSA](https://llvm.org/docs/AMDGPUUsage.html#hsa). For AMDGPU kernel execution has direct access to kernel arguments memory
* An AQL kernel dispatch packet is created on the AQL queue. 64-bit atomic operationss is used to reserve space in the AQL queue
  - Final write must use an atomic store release to set the packet kind
  - AQL defines a doorbell signal mechanism, to notify kernel agent that AQL has been updated.[For more info](https://llvm.org/docs/AMDGPUUsage.html#hsa)
* A kernel dispatch contains information about the actual dispatch and information about the kernel. The HSA runtime can be used tofind values recorded in the [Code Object Metadata](https://llvm.org/docs/AMDGPUUsage.html#amdgpu-amdhsa-code-object-metadata)
* CP executes micro-code and is responsible for detecting and setting up the GPU to execute wavefronts of a kernel dispatch
* CP ensures SGRP and VGRP is setup as required by the machine code. See [Kernel Descriptor](https://llvm.org/docs/AMDGPUUsage.html#amdgpu-amdhsa-kernel-descriptor) and [Initial Kernel Execution State](https://llvm.org/docs/AMDGPUUsage.html#amdgpu-amdhsa-initial-kernel-execution-state)
  - SGRP = Scalar General Purpose Registers
  - VGRP = Vector General Purpose Registers
* [Kernel Prolog](https://llvm.org/docs/AMDGPUUsage.html#amdgpu-amdhsa-kernel-prolog) initialized by the compiler from instructions in the Initial Kernel Execution State via the Kernel descriptor
* When execution is complete, CP signals completion specified in the kernel dispatch packet, if not 0.

## HSA Signals

HSA Signal handles, are 64-bit addresses of a structure allocated in memory. Accessible both from CPU and GPU

## HSA AQL Queue

The HSA AQL queue structure, is defined by an HSA compatible runtime

## Example HSA kernel in assembler

GFX900 HSA kernel in [asm](https://llvm.org/docs/AMDGPUUsage.html#code-object-v3-and-above-example-source-code)

## HSA IB
```
bob@melee:~/dev/7900xtx/crash$ sudo umr -go 0 -di 0@0x7fff00b4ad00 0xc 6
[WARNING]: Unknown ASIC [amd744c] should be added to pci.did to get proper name
Decoding IB at 0@0x7fff00b4ad00 from 0@0x0 of 0 words (type 0)
[0@0x7fff00b4ad00 + 0x0000]     [        0x00000002]    Opcode 0x2 [HSA_KERNEL_DISPATCH] (32 words, type: 0, hdr: 0x2)
[0@0x7fff00b4ad00 + 0x0002]     [            0x0000]    |---> setup_dimensions=0
[0@0x7fff00b4ad00 + 0x0004]     [            0x1aa0]    |---> workgroup_size_x=6816
[0@0x7fff00b4ad00 + 0x0006]     [            0x0040]    |---> workgroup_size_y=64
[0@0x7fff00b4ad00 + 0x0008]     [            0x7fff]    |---> workgroup_size_z=32767
[0@0x7fff00b4ad00 + 0x000a]     [            0x0000]    |---> reserved0=0
[0@0x7fff00b4ad00 + 0x000c]     [        0x00000000]    |---> grid_size_x=0
[0@0x7fff00b4ad00 + 0x0010]     [        0xdeadbeef]    |---> grid_size_y=3735928559
[0@0x7fff00b4ad00 + 0x0014]     [        0x00000000]    |---> grid_size_z=0
[0@0x7fff00b4ad00 + 0x0018]     [        0x00000000]    |---> private_segment_size=0
[0@0x7fff00b4ad00 + 0x001c]     [        0x00000000]    |---> group_segment_size=0
[0@0x7fff00b4ad00 + 0x0020]     [0x0000000000000000]    |---> kernel_object=0x0
[0@0x7fff00b4ad00 + 0x0028]     [0x0000000000000000]    |---> kernarg_address=0x0
[0@0x7fff00b4ad00 + 0x0030]     [0x0000000000000000]    |---> reserved2=0x0
[0@0x7fff00b4ad00 + 0x0038]     [0x0000000000000000]    |---> completion_signal=0x0
[0@0x7fff00b4ad00 + 0x0040]     [        0x00000000]    Opcode 0x0 [HSA_VENDOR_SPECIFIC] (1 words, type: 0, hdr: 0x0)
[0@0x7fff00b4ad00 + 0x0042]     [        0x00000000]    Opcode 0x0 [HSA_VENDOR_SPECIFIC] (1 words, type: 0, hdr: 0x0)
[0@0x7fff00b4ad00 + 0x0044]     [        0x00000000]    Opcode 0x0 [HSA_VENDOR_SPECIFIC] (1 words, type: 0, hdr: 0x0)
[0@0x7fff00b4ad00 + 0x0046]     [        0x00000000]    Opcode 0x0 [HSA_VENDOR_SPECIFIC] (1 words, type: 0, hdr: 0x0)
Done decoding IB
```
