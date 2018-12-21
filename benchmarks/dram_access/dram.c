#include "util.h"
#include "size.h"
/*

Compilation:
Note: MUST use -O1 and higher optimization, otherwise reduntant DRAM access will be generated.
riscv64-unknown-elf-gcc -I../../env -I../common -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -ffast-math -fno-common -fno-builtin-printf -o dram.riscv dram.c ../common/syscalls.c ../common/crt.S -static -nostdlib -nostartfiles -lm -lgcc -T ../common/test.ld -O1

Run:
spike --dc=64:4:64:1 dram.riscv > log

*/



// Declaration of using the printf for baremetal run.
// it's included in ../common/syscalls.c
extern int printf(const char* fmt, ...);

// #define TEST_SIZE 10000, defined in size.h

int main( int argc, char* argv[] )
{
  long int x=0; 

  // use the following if adopt the direct physical memory write,
  // currently, RISC-V tool has no virtual memory protection.
  long int *data = (volatile unsigned int *)0x800de000;

  int cycle;
  cycle = -read_csr(mcycle);

  // Note: DONOT use dynamic allocation in measurment.
  // read data and do accumulation
  for (int ii=0; ii<100; ii++){
    for (int jj=0; jj<TEST_SIZE; jj++){
      x = x + *(data+jj);
  }}
  
  cycle += read_csr(mcycle);  
  printf("\n\ncycle=%d\n\n", cycle);
  printf("x=%d\n",x);
  return x;
}
