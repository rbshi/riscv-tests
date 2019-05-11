#include <stdio.h>
#include "rocc.h"
#include "wiki_l2.h"

static inline void elstm_fun0(uint64_t size_x, uint64_t size_h)
{
    ROCC_INSTRUCTION_SS(0, size_x, size_h, 0);
}

static inline void elstm_fun1(uint h_th, uint size_ts)
{
    ROCC_INSTRUCTION_SS(0, h_th, size_ts, 1);
}

static inline void elstm_fun2(void *p_w, void *p_b)
{
    ROCC_INSTRUCTION_SS(0, (uintptr_t) p_w, (uintptr_t) p_b, 2);
}

static inline void elstm_fun3(void *p_ucolumn, uint ngrp)
{
    ROCC_INSTRUCTION_SS(0, (uintptr_t) p_ucolumn, ngrp, 3);
}

static inline void elstm_fun4(void *p_x, void* p_h)
{
    ROCC_INSTRUCTION_SS(0, (uintptr_t) p_x, (uintptr_t) p_h, 4);
}

static inline void elstm_fun5(void *p_u, uint dram_trace_flag)
{
    ROCC_INSTRUCTION_SS(0, (uintptr_t) p_u, dram_trace_flag, 5);
}


int main(void)
{

    // floating point -> uint 
    // mnist-l1: 0x3E99999A (0.3)
    // mnist-l2: 0x3F4CCCCD (0.8)
    // ptb-l1: 0x3DF5C28F (0.12)
    // ptb-l2: 0x3E6147AE (0.22)
    // wiki-l1: 0x3E8F5C29 (0.28)
    // wiki-l2: 0x3EDC28F6 (0.43)


    uint x_size = 1500;
    uint h_size = 1500;
    uint h_th = 0x3EDC28F6;
    uint ts_size = 35;
    uint ngrp = 7;

    // Note: 
    uint32_t h[h_size];

    for (int ii=0; ii<20; ii++){

        elstm_fun0(x_size, h_size);
        elstm_fun1(h_th, ts_size);
        elstm_fun2(w, bias);
        elstm_fun3(u_offset, ngrp);
        elstm_fun4(&(x[ii*x_size*ts_size]), h);
        elstm_fun5(u, 0);

    }

    // for (uint ii=0; ii<128; ii++){
    //     printf("h[%d]=%x\n", ii, h[ii]);
    // }

    return 0;

}
