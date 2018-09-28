#!/bin/sh
riscv64-unknown-elf-gcc -I../../env -I../common -I./ -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -ffast-math -fno-common -fno-builtin-printf -o spmv.riscv riscv_spmv.c ../common/syscalls.c ../common/crt.S -static -nostdlib -nostartfiles -lm -lgcc -T ../common/test.ld -O1

riscv64-unknown-elf-objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.data spmv.riscv > spmv.riscv.dump

spike --dc=64:2:64:1 spmv.riscv > log
spike --dc=64:2:64:0 spmv.riscv > log_simple