#!/usr/bin/env python3
import struct
from hexdump import hexdump
# bd501466f507fd1c8da17b77d278e1af03f80845  gc_11_0_0_mec.bin
dat = open("gc_11_0_0_mec.bin", "rb").read()
offset = dat.find(b"\x24\x50\xf0\xff")
cmdtable = dat[offset:offset+300*4]
offset = struct.unpack("I"*(len(cmdtable)//4), cmdtable)

# 0x5490
# 0x55a4
# 0x5688

for i,o in enumerate(offset):
  print(hex(i), hex(o))
