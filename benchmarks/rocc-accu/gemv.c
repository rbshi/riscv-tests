#include "stdio.h"
#include "rocc.h"

static inline void gemv_set_size(int mat_w, int mat_h)
{
	ROCC_INSTRUCTION_SS(0, mat_w, mat_h, 0);
}

static inline void gemv_set_addr(void *mat_addr, void *vec_addr)
{
	ROCC_INSTRUCTION_SS(0, (uintptr_t) mat_addr, (uintptr_t) vec_addr, 1);
}

static inline void gemv_set_start_res(void *res_addr)
{
	ROCC_INSTRUCTION_S(0, (uintptr_t) res_addr, 2);
	asm volatile ("fence");
}


int main(void)
{
	

	int mat_w, mat_h;

	// define the size of matrix
	mat_w = 3; mat_h = 3;
	
	uint64_t mat[mat_w*mat_h];
	uint64_t vec[mat_w];
	uint64_t res[mat_h];
	// initialize the mat and vec
	for (int ii=0; ii<mat_w*mat_h; ii++){
		mat[ii] = ii+1000;
	}
	for (int ii=0; ii<mat_w; ii++){
		vec[ii] = ii+25;
	}
	memset(res, 0, sizeof(res));

	gemv_set_size(mat_w, mat_h);
	gemv_set_addr(&mat, &vec);
	gemv_set_start_res(&res);


	// verify
    for (int ii=0; ii<mat_h; ii++){
    	int tmp = 0;
    	for (int jj=0; jj<mat_w; jj++){
        	tmp = tmp + mat[ii*mat_w+jj]*vec[jj];
    	}

    	if (tmp != res[ii]){
    		printf("Verify faliure.\n");
    		printf("%d\n", res[ii]);
    		return -1;
    		break;
    	}
    }

   	printf("Passed!\n");
    return 0;

}
