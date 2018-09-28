#!/bin/sh

for row in 10 20 40 80 160 320 640 1280 2560
do
    # 
    col=${row}
    density=0.2
    #
    python spm_gen.py ${row} ${col} ${density}

    riscv64-unknown-elf-gcc -I../../env -I../common -I./ -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -ffast-math -fno-common -fno-builtin-printf -o spmv-${row}-${col}-${density}.riscv riscv_spmv.c ../common/syscalls.c ../common/crt.S -static -nostdlib -nostartfiles -lm -lgcc -T ../common/test.ld -O1

#    riscv64-unknown-elf-objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.data spmv-${row}-${col}-${density}.riscv > spmv-${row}-${col}-${density}.riscv.dump

    spike --dc=64:4:64:1 spmv-${row}-${col}-${density}.riscv > log
    spike --dc=64:4:64:0 spmv-${row}-${col}-${density}.riscv > log_simple

    #
    python analysis_log.py ${row} ${col} ${density}

done

