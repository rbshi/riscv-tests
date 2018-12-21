import sys

if __name__ == '__main__':
    log_file = open('logdram', 'r')
    res_file = open('dram.log', 'a')

    for line in log_file:
        if ('Total Trace Length (clock cycles): ' in line):
            total_cycle = line[35:].strip()
        if ('Total Trace Energy: ' in line):
            total_energy = line[20:-3].strip()

    res_file.write(total_cycle + '\t' + total_energy + '\n')



