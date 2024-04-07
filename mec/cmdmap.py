#!/usr/bin/env python3
import struct
from hexdump import hexdump
# bd501466f507fd1c8da17b77d278e1af03f80845  gc_11_0_0_mec.bin
# switched to c55ab5e8ba327ef3b219234291b7c4fc2f91248c  gc_11_0_0_mec.bin

# 0x15 PACKET3_DISPATCH_DIRECT 0xfff060e8
# 0x285e8

dat = open("gc_11_0_0_mec.bin", "rb").read()[0x200:].strip(b"\x00")

#offset = dat.find(b"\x24\x50\xf0\xff")
#cmdtable = dat[offset:] #offset+300*4+0x1000]
#offset = struct.unpack("H"*(len(cmdtable)//2), cmdtable)

# this is correct (just useless for PM4?)
offset = dat.find(b"\x3c\x50\xf0\xff")
cmdtable = dat[offset:offset+300*4]
offset = struct.unpack("i"*(len(cmdtable)//4), cmdtable)
offsets = [(42,0x100148), (72,0x1001f0), (8,0x100310), (16,0x100330),
           (16,0x100370), (23,0x1003b0), (15,0x10040c), (18,0x100448),
           (7,0x100490), (7,0x1004ac), (34,0x1004c8), (21,0x100550),
           (7,0x1005a4), (7,0x1005c0), (7,0x1005dc)]
exoffsets = []
for cnt,num in offsets:
  exoffsets += [num]*cnt
assert len(exoffsets) == len(offset)
for i,o in enumerate(offset):
  print(i, hex(exoffsets[i]), hex(exoffsets[i]+o), hex(0x100000000+o))
exit(0)

for o1 in offset:
  if o1 == 0:
    continue
  for o2 in offset:
    if o2*4-o1*4 == found[0]-found[2]:
      print("HIT", hex(found[1]-o2*4), hex(o1), hex(o2))



"""
for o1 in offset:
  for o2 in offset:
    if o2-o1 == found[2]-found[1]:
      print("HIT", hex(found[1]-o2), hex(o1), hex(o2))
"""
exit(0)


"""
for b in range(0x100000, 0x110000, 4):
  ff = [b+o for o in offset]
  if found[0] in ff and found[1] in ff:
    print(hex(b))
exit(0)
"""


"""
for o in offset:
  tb = o+found[1]
  for o2 in offset:
    #print(hex(tb), hex(o2-found[1]))
    if o2+found[2] == tb:
      print(hex(tb))
exit(0)
"""


"""
idx = -1
while 1:
  idx = dat.find(b"\x9b\x96\x26\x00", idx+1)
  if idx == -1:
    break
  print(hex(idx))
"""

# 0x5490
# 0x55a4
# 0x5688
# 0xffee97e8
#BASE = 0xfff57b18

#BASE = 0x1005dc
BASE = 0x1011f8
#BASE = 0x100aa8

for i,o in enumerate(offset):
  print(hex(i), hex(o+BASE))
