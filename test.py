#!/usr/bin/env python3
import os
from tqdm import trange
import numpy as np
import time
import sys
sys.path.append(os.environ["HOME"] + "/tinygrad")

#os.environ["HSAKMT_DEBUG_LEVEL"] = "7"
from extra.hip_gpu_driver import hip_ioctl

import ctypes
import tinygrad.runtime.autogen.hsa as hsa
from tinygrad.helpers import init_c_var, from_mv
from tinygrad.runtime.driver import hsa as hsa_driver

from tinygrad.runtime.ops_hsa import HSAProgram, HSACompiler
from hexdump import hexdump
#lib = HSACompiler("gfx1100").compile("void test() {}")

def check(status):
  if status != 0:
    hsa.hsa_status_string(status, ctypes.byref(status_str := ctypes.POINTER(ctypes.c_char)()))
    raise RuntimeError(f"HSA Error {status}: {ctypes.string_at(status_str).decode()}")

check(hsa.hsa_init())
#time.sleep(1)
agents = hsa_driver.scan_agents()
agent = agents[hsa.HSA_DEVICE_TYPE_GPU][0]

check(hsa.hsa_agent_get_info(agent, hsa.HSA_AGENT_INFO_QUEUE_MAX_SIZE, ctypes.byref(max_queue_size := ctypes.c_uint32())))
queue_size = max_queue_size.value

null_func = ctypes.CFUNCTYPE(None, hsa.hsa_status_t, ctypes.POINTER(hsa.struct_hsa_queue_s), ctypes.c_void_p)()
hw_queue = init_c_var(ctypes.POINTER(hsa.hsa_queue_t)(), lambda x: check(
  hsa.hsa_queue_create(agent, queue_size, hsa.HSA_QUEUE_TYPE_SINGLE, null_func, None, (1<<32)-1, (1<<32)-1, ctypes.byref(x))))

print(hw_queue)

next_doorbell_index = 0
queue_base = hw_queue.contents.base_address
write_addr = queue_base
#for i in trange(10000):
  # random crap in the queue
  #dat = np.random.randint(0, 255, size=0x100)
  #ctypes.memmove(queue_base, from_mv(dat.data), 0x100)

global_size, local_size = [0x10,0x10,0x10], [0x10, 0x10, 0x10]

private_segment_size = 0x1000
group_segment_size = 0x1000
handle = 12312
kernargs = 0

packet = hsa.hsa_kernel_dispatch_packet_t.from_address(write_addr)
packet.workgroup_size_x = local_size[0]
packet.workgroup_size_y = local_size[1]
packet.workgroup_size_z = local_size[2]
packet.reserved0 = 0
packet.grid_size_x = global_size[0] * local_size[0]
packet.grid_size_y = global_size[1] * local_size[1]
packet.grid_size_z = global_size[2] * local_size[2]
packet.private_segment_size = private_segment_size
packet.group_segment_size = group_segment_size
packet.kernel_object = handle
packet.kernarg_address = kernargs
packet.reserved2 = 0
packet.completion_signal = hsa_driver.EMPTY_SIGNAL
packet.setup = hsa_driver.DISPATCH_KERNEL_SETUP
packet.header = hsa_driver.DISPATCH_KERNEL_HEADER

# corrupt
#dat = np.random.randint(0, 255, size=0x100)
#ctypes.memmove(write_addr, from_mv(dat.data), 0x100)

# ring doorbell
print("DING DONG")
next_doorbell_index += 1
hsa.hsa_queue_store_write_index_relaxed(hw_queue, next_doorbell_index)
hsa.hsa_signal_store_screlease(hw_queue.contents.doorbell_signal, next_doorbell_index-1)

time.sleep(5)


check(hsa.hsa_queue_destroy(hw_queue))

#import tinygrad.runtime.autogen.hsakmt as hsakmt
#check(hsakmt.hsaKmtOpenKFD())

#hsakmt.hsaKmtAllocMemory()