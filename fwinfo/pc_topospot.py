graph = {0:set(), -1:set()}
pods = open("/tmp/trace2").read().strip().split(")\n")[1:]

from collections import defaultdict
addrs = defaultdict(list)
for p in pods:
  addr = [int(l.replace(" ", ""), 16) for l in p.split("(")[0].strip().split("\n")]
  if len(addr) == 1: continue
  for i,a in enumerate(addr): addrs[a].append(i/(len(addr)-1))

  """
  addr = [0] + addr + [-1]
  for i,e in enumerate(addr[1:]):
    b = addr[i]
    if b not in graph: graph[b] = set()
    if (b != 92992 and e != 81440) and b != e and (b != 81328 and e != 93476) and (b != 81976 and e != 81968):
      graph[b].add(e)
  """

for a in sorted(addrs):
  print(f"{a:X} {sum(addrs[a])/len(addrs[a]):.2f}", len(addrs[a])) # {len(addrs[a]):d}", addrs[a])


exit(0)


#cnt = sorted([(sum(pp)/len(pp),a) for a,pp in addrs.items()])
#for _,x in cnt: print(hex(x))
from graphlib import TopologicalSorter
ts = TopologicalSorter(graph)
for x in tuple(ts.static_order()):
  print(hex(x), len(graph[x]))