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
