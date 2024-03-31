# SDMA

The SDMA you normally use is part of the GFX block. How do you control with one your queue is on?

## LSDMA (fake SDMA)

Has 2 hw queues you can see in the register dump.

```bash
sudo umr -s amd744c.lsdma600
```

NOTE: this is not the SDMA you normally use

## SDMA (real SDMA)

```bash
watch -n 0.001 'sudo umr -s amd744c.gfx1100 | grep SDMA0_QUEUE2'
```

There's two of them with 8 queues each. It's set up by the driver then handed off to the MES. Default is SDMA0 on QUEUE2

```
[86163.338010] [drm:sdma_v6_0_ring_set_wptr [amdgpu]] Setting write pointer
[86163.338188] [drm:sdma_v6_0_ring_set_wptr [amdgpu]] Using doorbell -- wptr_offs == 0x000001a8 lower_32_bits(ring->wptr) << 2 == 0x000004c0 upper_32_bits(ring->wptr) << 2 == 0x00000000
[86163.338362] [drm:sdma_v6_0_ring_set_wptr [amdgpu]] calling WDOORBELL64(0x00000214, 0x00000000000004c0)
[86163.339459] [drm:amdgpu_ih_process [amdgpu]] amdgpu_ih_process: rptr 2016, wptr 2080
[86163.339684] [drm:sdma_v6_0_process_trap_irq [amdgpu]] IH: SDMA trap
[86163.339862] [drm:amdgpu_irq_dispatch [amdgpu]] Unregistered interrupt src_id: 51 of client_id:10
[86163.340603] [drm:amdgpu_ttm_tt_get_user_pages_done [amdgpu]] user_pages_done 0x72a570300000 pages 0x100
[86163.341086] MES_MISC_OP_WRM_REG_WR_WAIT: 291c 292e
[86163.341090] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] MES msg=14 was emitted
[86163.341259] MES_MISC_OP_WRM_REG_WR_WAIT: 1a774 1a786
[86163.341261] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] MES msg=14 was emitted
[86163.341916] [drm:mes_v11_0_submit_pkt_and_poll_completion.constprop.0 [amdgpu]] MES msg=2 was emitted
[86163.342367] [drm:amdgpu_ttm_tt_get_user_pages_done [amdgpu]] user_pages_done 0x72a5cbc3d000 pages 0x1
[86163.342573] [drm:amdgpu_ih_process [amdgpu]] amdgpu_ih_process: rptr 2080, wptr 2112
[86163.342756] [drm:amdgpu_irq_dispatch [amdgpu]] Unregistered interrupt src_id: 51 of client_id:10
[86163.442951] [drm:amdgpu_ih_process [amdgpu]] amdgpu_ih_process: rptr 2112, wptr 2144
[86163.443177] [drm:amdgpu_irq_dispatch [amdgpu]] Unregistered interrupt src_id: 51 of client_id:10
[86163.543334] [drm:amdgpu_ih_process [amdgpu]] amdgpu_ih_process: rptr 2144, wptr 2176
[86163.543560] [drm:amdgpu_irq_dispatch [amdgpu]] Unregistered interrupt src_id: 51 of client_id:10
```

```
kafka@q:/lib/firmware/amdgpu$ sudo umr -sdma
[WARNING]: Unknown ASIC [amd744c] should be added to pci.did to get proper name

SDMA 0  RLC 0
  RB BASE 0x45f000  RPTR 0x2afc0  WPTR 0x2afc0  RPTR_ADDR 0x4015e0  CNTL 0x841817

SDMA 0  RLC 2
  RB BASE 0x790260600000  RPTR 0x493c  WPTR 0x493c  RPTR_ADDR 0x7902c1482010  CNTL 0x8061825

SDMA 0  RLC 3
  RB BASE 0x790260800000  RPTR 0x3550  WPTR 0x3550  RPTR_ADDR 0x7902c1480010  CNTL 0x8061825

SDMA 1  RLC 0
  RB BASE 0x461000  RPTR 0x340  WPTR 0x340  RPTR_ADDR 0x401680  CNTL 0x841817
```
