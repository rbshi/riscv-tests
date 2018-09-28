# Generate sparse matrix and the corresponding CSR, CSC, COO representation.

from scipy import sparse
import numpy as np

import sys

def frac2fix(nd_array, dtype):
    dt_bit_len = np.dtype(dtype).itemsize*8
    # mult_factor = np.array(2**dt_bit_len).repeat(nd_array.shape)
    nd_array = nd_array * (2**dt_bit_len)
    nd_array_int = nd_array.astype(np.dtype(dtype))
    return nd_array_int

def print_data(file, array_name, array_data):
    file.write('const' + ' int ' + array_name + '[' + str(array_data.size) + ']' + ' = { ')
    file.write(str(array_data[0]))
    for ii in range(1, array_data.size):
        file.write(', ' + str(array_data[ii]))
    file.write(' };\n\n')

def print_def(file, ROW, COL, NNZ):
    file.write('#define R ' + str(ROW) + '\n')
    file.write('#define C ' + str(COL) + '\n')
    file.write('#define NNZ ' + str(NNZ) + '\n\n')


if __name__ == '__main__':

    argv = sys.argv

    ROW = int(argv[1])
    COL = int(argv[2])
    DENSITY = float(argv[3])

    mat_coo = sparse.rand(ROW, COL, density=DENSITY, format='coo', random_state=None)
    # trans float to fixed point, sparse.rand only support float random
    mat_coo.data = frac2fix(mat_coo.data, 'int16')
    mat_csr = mat_coo.tocsr()
    mat_csc = mat_coo.tocsc()
    mat_array = mat_coo.toarray()
    # Dense vector
    vec_float = np.random.rand(COL)
    vec_int = frac2fix(vec_float, 'int16')
    res = np.dot(mat_array.astype(np.dtype('int32')), vec_int.astype(np.dtype('int32')))
    # res = mat_array.dot(vec_int)

    data_hf = open('data_head.h', 'w')

    print_def(data_hf, ROW, COL, mat_coo.data.size)
    print_data(data_hf, 'coo_row', mat_coo.row)
    print_data(data_hf, 'coo_col', mat_coo.col)
    print_data(data_hf, 'coo_val', mat_coo.data)

    print_data(data_hf, 'csr_idx', mat_csr.indices)
    print_data(data_hf, 'csr_ptr', mat_csr.indptr)
    print_data(data_hf, 'csr_val', mat_csr.data)

    print_data(data_hf, 'csc_idx', mat_csc.indices)
    print_data(data_hf, 'csc_ptr', mat_csc.indptr)
    print_data(data_hf, 'csc_val', mat_csc.data)

    print_data(data_hf, 'x0', vec_int)
    print_data(data_hf, 'x1', vec_int)

    print_data(data_hf, 'verify_data', res)

    data_hf.close()

    print("[DONE] Generate test data ...")