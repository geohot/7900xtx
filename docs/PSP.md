# Platform Security Processor

The PSP does bringup of the rest of the system. See `psp_cmd_submit_buf` for RPC.

```C
/* TEE Gfx Command IDs for the ring buffer interface. */
enum psp_gfx_cmd_id
{
    GFX_CMD_ID_LOAD_TA            = 0x00000001,   /* load TA */
    GFX_CMD_ID_UNLOAD_TA          = 0x00000002,   /* unload TA */
    GFX_CMD_ID_INVOKE_CMD         = 0x00000003,   /* send command to TA */
    GFX_CMD_ID_LOAD_ASD           = 0x00000004,   /* load ASD Driver */
    GFX_CMD_ID_SETUP_TMR          = 0x00000005,   /* setup TMR region */
    GFX_CMD_ID_LOAD_IP_FW         = 0x00000006,   /* load HW IP FW */
    GFX_CMD_ID_DESTROY_TMR        = 0x00000007,   /* destroy TMR region */
    GFX_CMD_ID_SAVE_RESTORE       = 0x00000008,   /* save/restore HW IP FW */
    GFX_CMD_ID_SETUP_VMR          = 0x00000009,   /* setup VMR region */
    GFX_CMD_ID_DESTROY_VMR        = 0x0000000A,   /* destroy VMR region */
    GFX_CMD_ID_PROG_REG           = 0x0000000B,   /* program regs */
    GFX_CMD_ID_GET_FW_ATTESTATION = 0x0000000F,   /* Query GPUVA of the Fw Attestation DB */
    /* IDs upto 0x1F are reserved for older programs (Raven, Vega 10/12/20) */
    GFX_CMD_ID_LOAD_TOC           = 0x00000020,   /* Load TOC and obtain TMR size */
    GFX_CMD_ID_AUTOLOAD_RLC       = 0x00000021,   /* Indicates all graphics fw loaded, start RLC autoload */
    GFX_CMD_ID_BOOT_CFG           = 0x00000022,   /* Boot Config */
    GFX_CMD_ID_SRIOV_SPATIAL_PART = 0x00000027,   /* Configure spatial partitioning mode */
};
```

## Secure Operating System

This is the main code for the PSP. It's an ARM binary, amdgpu/psp_13_0_0_sos.bin

It's loaded with `psp_v13_0_bootloader_load_sos`. The bootloader commands are here.

```C
enum psp_bootloader_cmd {
	PSP_BL__LOAD_SYSDRV		= 0x10000,
	PSP_BL__LOAD_SOSDRV		= 0x20000,
	PSP_BL__LOAD_KEY_DATABASE	= 0x80000,
	PSP_BL__LOAD_SOCDRV             = 0xB0000,
	PSP_BL__LOAD_DBGDRV             = 0xC0000,
	PSP_BL__LOAD_INTFDRV		= 0xD0000,
	PSP_BL__LOAD_RASDRV		    = 0xE0000,
	PSP_BL__DRAM_LONG_TRAIN		= 0x100000,
	PSP_BL__DRAM_SHORT_TRAIN	= 0x200000,
	PSP_BL__LOAD_TOS_SPL_TABLE	= 0x10000000,
};
```

TODO: how do we dump the bootloader and what arch is it?

