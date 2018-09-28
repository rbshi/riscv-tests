#!/bin/sh

for row in 10 20 40 80 160 320 640 1280 2560
do
    col=${row}
    density=0.2
    ./fesvr-zynq spmv-${row}-${col}-${density}.riscv >> log_run
done

