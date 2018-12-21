# parse log file for cache and dram trace

import sys

def locate_para(addr, para_dir):
    """

    :param addr:
    :param para_dir:
    :return:
    """
    for elem in para_dir:
        if type(para_dir[elem]) is tuple:
            if (addr >= para_dir[elem][0]) & (addr < para_dir[elem][1]):
                return elem

if __name__ == '__main__':

    argv = sys.argv

    log_file = open('log', 'r')
    log_simple_file = open('log_simple', 'r')
    
    # DRAM trace file
    dram_trace = open('dram.trace', 'w')

    para_dir = {}
    access_cnt = {}
    miss_cnt = {}

    # # general parse
    # for line in log_simple_file:
    #     if ('ADDR' in line):
    #         para_list = line[5:].strip().split(',')
    #         for elem in para_list:
    #             elem_split = elem.split('=')
    #             para_dir[elem_split[0]] = int(elem_split[1], 16)
    #             access_cnt[elem_split[0]] = [0, 0]
    #             miss_cnt[elem_split[0]] = [0, 0]

    #     if ('cycle' in line):
    #         cycle = int(line[6:].strip())

    # manually cal para dram range
    para_dir['MAT'] = (int('800de000', 16), int('800de000', 16) + int(sys.argv[1])*64)
    access_cnt['MAT'] = [0,0]
    miss_cnt['MAT'] = [0, 0]

    # general parse memory read trace
    for line in log_file:

        if (line[0:3] == 'RD@'):
            # TODO: exclude the ValueError
            try:
                addr = int(line[3:11], 16)
            except ValueError:
                # print("ErrorLine: " + line)
                continue
            else:
                addr = int(line[3:11], 16)
                elem = locate_para(addr, para_dir)
                if elem:
                    access_cnt[elem][0] = access_cnt[elem][0] + 1
                continue


        if (line[0:3] == 'WR@'):
            # TODO: exclude the ValueError
            try:
                addr = int(line[3:11], 16)
            except ValueError:
                # print("ErrorLine: " + line)
                continue
            else:
                addr = int(line[3:11], 16)
                elem = locate_para(addr, para_dir)
                if elem:
                    access_cnt[elem][1] = access_cnt[elem][1] + 1
                continue


        if ('-------------------' in line):
            if ('WRMISS' in line):
                addr = int(line[26:34], 16)
                elem = locate_para(addr, para_dir)
                if elem:
                    miss_cnt[elem][1] = miss_cnt[elem][1] + 1
                    miss_line_head = int(line[38:46], 16)
                    for ii in range (0, 8):
                        dram_trace.write(str(0)+',WR,'+ hex(miss_line_head+8*ii)+'\n')
                continue
            if ('RDMISS' in line):
                addr = int(line[26:34], 16)
                elem = locate_para(addr, para_dir)
                if elem:
                    miss_cnt[elem][0] = miss_cnt[elem][0] + 1
                    miss_line_head = int(line[38:46], 16)
                    for ii in range (0, 8):
                        dram_trace.write(str(0)+',RD,'+ hex(miss_line_head+8*ii)+'\n')
                continue

    log_file.close()
    log_simple_file.close()
    dram_trace.close()


    res_file_name = 'cache' + '.log'
    res_file = open(res_file_name, 'a')

    # res_file.write(argv[1] + '\t')
    # res_file.write(argv[2] + '\t')
    # res_file.write(argv[3] + '\t')
    for elem in access_cnt:
        if type(para_dir[elem]) is tuple:
            res_file.write(str(access_cnt[elem][0])+'\t')
            res_file.write(str(miss_cnt[elem][0])+'\t')
            res_file.write(str(access_cnt[elem][1])+'\t')
            res_file.write(str(miss_cnt[elem][1])+'\t')
    res_file.write('\n')
    res_file.close()

    print_log = '[DONE] Analysis Cache file of word ' + sys.argv[1] + ' ...'
    print(print_log)
