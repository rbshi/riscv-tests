# parse log file for cache and dram trace

import sys

def locate_para(addr, para_dir):
    for elem in para_dir:
        if type(para_dir[elem]) is tuple:
            if (addr >= para_dir[elem][0]) & (addr < para_dir[elem][1]):
                return elem

if __name__ == '__main__':

    argv = sys.argv

    log_file = open('log', 'r')
    log_simple_file = open('log_simple', 'r')

    para_dir = {}
    access_cnt = {}
    miss_cnt = {}

    # general parse
    for line in log_simple_file:
        if ('ADDR' in line):
            para_list = line[5:].strip().split(',')
            for elem in para_list:
                elem_split = elem.split('=')
                para_dir[elem_split[0]] = int(elem_split[1], 16)
                access_cnt[elem_split[0]] = [0, 0]
                miss_cnt[elem_split[0]] = [0, 0]

        if ('cycle' in line):
            cycle = int(line[6:].strip())

    # manually cal para dram range
    para_dir['VAL'] = (para_dir['VAL'], para_dir['VAL'] + para_dir['NNZ']*4)
    para_dir['IDX'] = (para_dir['IDX'], para_dir['IDX'] + para_dir['NNZ']*4)
    para_dir['PTR'] = (para_dir['PTR'], para_dir['PTR'] + (para_dir['R'] + 1)*4)

    para_dir['x0'] = (para_dir['x0'], para_dir['x0'] + para_dir['C']*4)
    para_dir['x1'] = (para_dir['x1'], para_dir['x1'] + para_dir['C']*4)
    para_dir['y0'] = (para_dir['y0'], para_dir['y0'] + para_dir['R']*4)
    para_dir['y1'] = (para_dir['y1'], para_dir['y1'] + para_dir['R']*4)

    # general parse memory read trace
    for line in log_file:

        if (line[0:3] == 'RD@'):
            # TODO: exclude the ValueError
            try:
                addr = int(line[3:11], 16)
            except ValueError:
                print("ErrorLine: " + line)
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
                print("ErrorLine: " + line)
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
                continue
            if ('RDMISS' in line):
                addr = int(line[26:34], 16)
                elem = locate_para(addr, para_dir)
                if elem:
                    miss_cnt[elem][0] = miss_cnt[elem][0] + 1
                continue

    log_file.close()
    log_simple_file.close()


    res_file_name = 'res' + '.log'
    res_file = open(res_file_name, 'a')

    res_file.write(argv[1] + '\t')
    res_file.write(argv[2] + '\t')
    res_file.write(argv[3] + '\t')
    for elem in access_cnt:
        if type(para_dir[elem]) is tuple:
            res_file.write(str(access_cnt[elem][0])+'\t')
            res_file.write(str(miss_cnt[elem][0])+'\t')
            res_file.write(str(access_cnt[elem][1])+'\t')
            res_file.write(str(miss_cnt[elem][1])+'\t')
    res_file.write(str(cycle) + '\n')
    res_file.close()

    print("[DONE] Analysis log file ... ")
