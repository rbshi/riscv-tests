#!/bin/sh


# rm dram.riscv* log* *.trace

for cacheword in 66216 9330 9464
do
    echo "#define TEST_SIZE ${cacheword}" > size.h

    riscv64-unknown-elf-gcc -I../../env -I../common -I./ -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -ffast-math -fno-common -fno-builtin-printf -o dram.riscv dram.c ../common/syscalls.c ../common/crt.S -static -nostdlib -nostartfiles -lm -lgcc -T ../common/test.ld -O1

#    riscv64-unknown-elf-objdump --disassemble-all --disassemble-zeroes --section=.text --section=.text.startup --section=.data spmv-${row}-${col}-${density}.riscv > spmv-${row}-${col}-${density}.riscv.dump

    spike --dc=64:4:64:1 dram.riscv > log
    spike --dc=64:4:64:0 dram.riscv > log_simple

    #
    python analysis_log.py ${cacheword}
    # dram 
    drampower -m $DRAMPOWER/memspecs/MICRON_2GB_DDR3-1600_64bit_G_UDIMM.xml -t dram.trace > logdram
    python analysis_dram.py ${cacheword}

done

