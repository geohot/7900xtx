from hexdump import hexdump
#dat = open("/lib/firmware/amdgpu/gc_11_0_0_mec.bin", "rb").read()
dat = open("/lib/firmware/amdgpu/gc_11_0_0_pfp.bin", "rb").read()
headers, code = dat[:0x200], dat[0x200:]

# first 0x200 is headers
# code starts at 0x3000

hexdump(code[:0x4000])
