import os, struct
from hexdump import hexdump

OFFSET = 0x200
mec_rs64 = open("/lib/firmware/amdgpu/gc_11_0_0_mec.bin", "rb").read()[OFFSET:]

# cd /sys/devices/pci0000:00/0000:00:01.2/0000:02:00.0/0000:03:02.0/0000:05:00.0/0000:06:00.0/0000:07:00.0/ip_discovery/die/0/GC/0
#GC_BASE_ADDR = 0x00001260
#GC_BASE_ADDR = 0x0000A000
#GC_BASE_ADDR = 0x0001C000
#GC_BASE_ADDR = 0x02402C00

# sudo strace umr -r amd744c.gfx1100.regCP_MEC_RS64_INSTR_PNTR
GC_BASE_ADDR = 0x28000 # 0xA000*4
regCP_MEC_RS64_INSTR_PNTR = 0x2908

# 0x32420

def poll_tight(cnt):
  ret = []
  for _ in range(cnt):
    os.lseek(fd, GC_BASE_ADDR + regCP_MEC_RS64_INSTR_PNTR*4, os.SEEK_SET)
    ret.append(os.read(fd, 4))
  return ret

fd = os.open("/sys/kernel/debug/dri/0/amdgpu_regs2", os.O_RDONLY)
seen_addrs = set()
cnt = 0
while 1:
  os.lseek(fd, GC_BASE_ADDR + regCP_MEC_RS64_INSTR_PNTR*4, os.SEEK_SET)
  addr = struct.unpack("<I", os.read(fd, 4))[0]
  seen_addrs.add(addr)
  if (cnt%10000) == 0:
    print([hex(x) for x in sorted(list(seen_addrs))])
  cnt += 1


  #data = struct.unpack(">I", mec_rs64[addr*4:addr*4+4])[0]
  #print(f"{addr:X} {data:X}")




  #hexdump(val)
