extern int printf(const char* fmt, ...);

#include "util.h"

//--------------------------------------------------------------------------
// Input/Reference Data

#include "data_head.h"

void spmv(int r, const int* val, const int* idx, const int* x,
          const int* ptr, int* y)
{
  for (int i = 0; i < r; i++)
  {
    int k;
    int k_min = ptr[i];
    int k_max = ptr[i+1];
    int tmp = 0;
    for (k = k_min; k < k_max; k++){
      tmp = tmp + val[k] * x[idx[k]];
    }
    y[i] = tmp;
  }
}

//--------------------------------------------------------------------------
// Main

int main( int argc, char* argv[] )
{
  int y0[R], y1[R];
  int cycle;

  // printf("\n\nbegin.\n\n");

  cycle = -read_csr(mcycle);
  spmv(R, csr_val, csr_idx, x0, csr_ptr, y0);
  spmv(R, csr_val, csr_idx, x1, csr_ptr, y1);
  // for (int i=0; i<R; i++){
  //   printf("y[%d]=%d\n", i, y[i]);
  // }
  cycle += read_csr(mcycle);

  printf("\n\ncycle=%d\n\n", cycle);
  // printf("\n\nend.\n\n");
  printf("\n\nADDR:VAL=%lx,IDX=%lx,PTR=%lx,x0=%lx,x1=%lx,y0=%lx,y1=%lx,R=%lx,C=%lx,NNZ=%lx\n\n", &csr_val, &csr_idx, &csr_ptr, &x0, &x1, &y0, &y1, R, C, NNZ);

  return 0;
  // return verify(R, y0, verify_data);
}
