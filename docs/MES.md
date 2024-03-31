# MES stands for Micro Engine Scheduler

All queues created with AMDKFD_IOC_CREATE_QUEUE go on the MES, which then dispatches to the hardware queues of the respective hardware blocks.

(actually, it appears like the SDMA queue is directly on the SDMA engine on GFX)

See `mes_v11_0_set_hw_resources` for info on the resources the MES manages.

```C
enum MES_SCH_API_OPCODE {
	MES_SCH_API_SET_HW_RSRC			= 0,
	MES_SCH_API_SET_SCHEDULING_CONFIG	= 1, /* agreegated db, quantums, etc */
	MES_SCH_API_ADD_QUEUE			= 2,
	MES_SCH_API_REMOVE_QUEUE		= 3,
	MES_SCH_API_PERFORM_YIELD		= 4,
	MES_SCH_API_SET_GANG_PRIORITY_LEVEL	= 5,
	MES_SCH_API_SUSPEND			= 6,
	MES_SCH_API_RESUME			= 7,
	MES_SCH_API_RESET			= 8,
	MES_SCH_API_SET_LOG_BUFFER		= 9,
	MES_SCH_API_CHANGE_GANG_PRORITY		= 10,
	MES_SCH_API_QUERY_SCHEDULER_STATUS	= 11,
	MES_SCH_API_PROGRAM_GDS			= 12,
	MES_SCH_API_SET_DEBUG_VMID		= 13,
	MES_SCH_API_MISC			= 14,
	MES_SCH_API_UPDATE_ROOT_PAGE_TABLE      = 15,
	MES_SCH_API_AMD_LOG                     = 16,
	MES_SCH_API_MAX				= 0xFF
};
```

## Adding a queue to the MES

```C
union MESAPI__ADD_QUEUE {
	struct {
		union MES_API_HEADER		header;
		uint32_t			process_id;
		uint64_t			page_table_base_addr;
		uint64_t			process_va_start;
		uint64_t			process_va_end;
		uint64_t			process_quantum;
		uint64_t			process_context_addr;
		uint64_t			gang_quantum;
		uint64_t			gang_context_addr;
		uint32_t			inprocess_gang_priority;
		enum MES_AMD_PRIORITY_LEVEL	gang_global_priority_level;
		uint32_t			doorbell_offset;
		uint64_t			mqd_addr;
		uint64_t			wptr_addr;
		uint64_t                        h_context;
		uint64_t                        h_queue;
		enum MES_QUEUE_TYPE		queue_type;
		uint32_t			gds_base;
		uint32_t			gds_size;
		uint32_t			gws_base;
		uint32_t			gws_size;
		uint32_t			oa_mask;
		uint64_t                        trap_handler_addr;
		uint32_t                        vm_context_cntl;
		struct {
			uint32_t paging			: 1;
			uint32_t debug_vmid		: 4;
			uint32_t program_gds		: 1;
			uint32_t is_gang_suspended	: 1;
			uint32_t is_tmz_queue		: 1;
			uint32_t map_kiq_utility_queue  : 1;
			uint32_t reserved		: 23;
		};
		struct MES_API_STATUS		api_status;
	};
	uint32_t	max_dwords_in_api[API_FRAME_SIZE_IN_DWORDS];
};
```
## SDMA (fake)

Has 2 hw queues you can see in the register dump.

```bash
sudo umr -s amd744c.lsdma600
```

NOTE: this is not the SDMA you normally use

## SDMA

The SDMA you normally use is part of the GFX block. How do you control with one your queue is on?

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
