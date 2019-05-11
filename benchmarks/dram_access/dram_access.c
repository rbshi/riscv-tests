/*

Compilation:
Note: MUST use -O1 and higher optimization, otherwise reduntant DRAM access will be generated.
riscv64-unknown-elf-gcc -I./../env -I./common -I./lstm -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -ffast-math -fno-common -fno-builtin-printf -o dram_test.riscv ./dram_access/test.c ./common/syscalls.c ./common/crt.S -static -nostdlib -nostartfiles -lm -lgcc -T ./common/test.ld -O1

Run:
spike --dc=64:4:64:1 dram_test.riscv > ./dram_access/log

*/



// Declaration of using the printf for baremetal run.
// it's included in ../common/syscalls.c
extern int printf(const char* fmt, ...);

#define TEST_SIZE 1000000

int main( int argc, char* argv[] )
{
  int x=0; 
  printf("Program Start\n");
  printf("initial x=%d\n",x);

  // use the following if adopt the direct physical memory write,
  // currently, RISC-V tool has no virtual memory protection.
  // int *data = (volatile unsigned int *)0x800de000;

  // Note: DONOT use dynamic allocation.
  int data[100];

  // write data in to memory 
  for (int ii=0; ii<TEST_SIZE; ii++){
    *(data+ii) = ii;
  }

  // read data and do accumulation
  for (int jj=0; jj<TEST_SIZE; jj++){
    x = x + *(data+jj);
  }

  // re-load the data, TEST_SIZE will affect cache-hit rate
  for (int jj=0; jj<TEST_SIZE; jj++){
    x = x + *(data+jj)*2;
  }

  printf("x=%d\n",x);
  return x;
}
