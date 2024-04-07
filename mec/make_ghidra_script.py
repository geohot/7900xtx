regs = [x.split(" ") for x in open("gc_11_0_0.reg").read().strip().split("\n") if x.startswith("reg")]
regs_dict = {}
base_addrs = [0x00001260, 0x0000A000, 0x0001C000, 0x02402C00]
for x in regs:
  #print(int(x[5]))
  addr, name = base_addrs[int(x[5])] + int(x[2],16), x[0]
  if addr not in regs_dict:
    regs_dict[addr] = name
  else:
    #print(f"OVERLAP {addr:X}", regs_dict[addr], name)
    pass
#assert len(regs_dict) == len(regs)
for addr,name in regs_dict.items():
  gaddr = 0x1080800000000 + addr*4
  print(f"{name} 0x{gaddr:X}")
  gaddr = 0x1000800000000 + addr*4
  print(f"{name.replace('reg', 'alt8')} 0x{gaddr:X}")
  gaddr = 0x1000200000000 + addr*4
  print(f"{name.replace('reg', 'alt2')} 0x{gaddr:X}")
  gaddr = 0x1000100000000 + addr*4
  print(f"{name.replace('reg', 'alt1')} 0x{gaddr:X}")

# regCP_HQD_PERSISTENT_STATE 0 0x1fad 18 0 0 +0x1260
# regSDMA0_QUEUE1_RB_BASE 0 0xd9 1 0 0
# regCP_PIPEID 0 0xd9 1 0 1

# OVERLAP D9 regCP_PIPEID regSDMA0_QUEUE1_RB_BASE
