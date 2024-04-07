import struct
from hexdump import hexdump
mec_f32 = open("/lib/firmware/amdgpu/gc_11_0_1_mec.bin", "rb").read()
mec_rs64 = open("/lib/firmware/amdgpu/gc_11_0_0_mec.bin", "rb").read()

# ./a.out /lib/firmware/amdgpu/gc_11_0_0_mec.bin /lib/firmware/amdgpu/gc_11_0_1_mec.bin
# /lib/firmware/amdgpu/gc_11_0_0_mec.bin   size_bytes:0x63620 ucode_size_bytes:0x63520
# /lib/firmware/amdgpu/gc_11_0_1_mec.bin   size_bytes:0x41960 ucode_size_bytes:0x41860

# both have 0x100 headers, skipped in f32dis.py
# the next 0x100 isn't really code, some other kind of header
# real code starts at 0x200 in f32 (numbers are after 0x100 header)
# real code starts at 0x1200 in rs64 (or maybe 0x3200)
# 0x100     ldw r9, [r0, #0xb]
# 0x104     b _PKT_0x0_10
# 0x108     stw #0x0, [r0, #0x8b]
# 0x10c     cbz r2, _jmptab_0x44

S = 0x100
c1 = mec_f32[S:]
print("***")

#S = 0x100  # 000091DC   00470713
S = 0x200  # 000091DC   1C058C63
#S = 0x3200
c2 = mec_rs64[S:]

with open("/tmp/mec.bin", "wb") as f: f.write(c2)

"""
# kernel wait loop
kafka@q:~/7900xtx/fwinfo$ clang -O2 dump_ip.c && sudo ./a.out
    91bc : 46830 <-- 8367020D
    91bd : 23319 <-- skip 9B870700
    91bf : 23358
    91c0 : 46045
    91c1 : 256994
    91c2 : 46645
    91c3 : 23166 <-- skip
    91c5 : 22995
    91c6 : 23021
    91c7 : 70026
    91c8 : 46407 <-- skip 9B870700
    91ca : 23063
    91cb : 23252
    91cc : 139591 <- 630E0702
    91cd : 93818 <-- branch 63960514
    91db : 46689 <-- E38207F8
    91dc : 93357 <-- branch 638C051C
"""

from capstone import *
md = Cs(CS_ARCH_RISCV, CS_MODE_RISCV64)

# 73 = unconditional absolute branch ???

# oooooo11 ssss ???

# 01101111 ssss 0000 iiiiiiiiiiii = mov 16-bit immediate into s (6f) ???

# python rosetta.py | sort | uniq -c | less
def disasm(addr):
  out = md.disasm(c2[addr*4:addr*4+4], addr)
  ins = [o for o in out]
  i2 = struct.unpack(">I", c2[addr*4:addr*4+4])[0]
  print(f"{addr*4:08X}   {i2:08X} {bin(i2 | (1 << 32))[3:]:s}", ins)
  #print(f"{bin(i2 | (1 << 32))[3:]:s} {i2:08X}")

#for i in range(0x10): disasm(0x9120 + i)
#for i in range(0x10000): disasm(0xc00 + i)
#for i in range(0x100): disasm(0x400 + i)
for i in range(0x40): disasm(0x91bc + i)

exit(0)

i = 0
while 1:
  addr = i*4

  for s in range(20):
    vals = [(k>>s)&0xFFFF for k in struct.unpack(">IIIII", c2[addr:addr+0x14])]
    if vals[0] == 0x2e01:
      print(hex(addr*4), f"{vals[0]:X} {vals[1]:X} {vals[2]:X} {vals[3]:X} {vals[4]:X}")
    vals = [(k>>s)&0xFFFF for k in struct.unpack("<IIIII", c2[addr:addr+0x14])]
    if vals[0] == 0x2e01:
      print(hex(addr*4), f"{vals[0]:X} {vals[1]:X} {vals[2]:X} {vals[3]:X} {vals[4]:X}")

  i += 1

"""
for i in range(0, 0x100, 4):
  i1 = struct.unpack("<I", c1[i:i+4])[0]
  i2 = struct.unpack(">I", c2[i:i+4])[0]
  print(f"{i:08X}  {i1:08X} {i2:08X}")
"""

# sudo umr -s amd744c.gfx1100 | grep regCP_MEC_RS64_INSTR_PNTR

# idle
# amd744c.gfx1100.regCP_MEC_RS64_INSTR_PNTR == 0x00009123

# running AQL queues
# amd744c.gfx1100.regCP_MEC_RS64_INSTR_PNTR == 0x000091bc
# amd744c.gfx1100.regCP_MEC_RS64_INSTR_PNTR == 0x000091c1
# amd744c.gfx1100.regCP_MEC_RS64_INSTR_PNTR == 0x000091dc


# xxd -c 36 -e -g4 /lib/firmware/amdgpu/gc_11_0_0_mec.bin  |more
# xxd -c 32 -e -g4 /lib/firmware/amdgpu/gc_11_0_1_mec.bin  |more