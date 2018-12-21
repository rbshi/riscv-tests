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


def sell_construct(mat_in, mat_size):
    row = mat_size[0]
    col = mat_size[1]

    mat_show = np.zeros(mat_size, dtype='int16')
    # chunk size, note: val_c should be an integer multiple of 4, to avoid the padding overhead
    val_c = 1 * 4
    # chunk width
    val_cw = 1 * 4
    # sorting range size, note: sigma should be an integer multiple of chunk size
    val_sigma = 2 * val_c

    mat_permut = np.zeros([mat_size[0],int(mat_size[1]/val_cw)], dtype='int16')
    mat_col_idx = np.zeros([row, col], dtype='int16')

    #TODO: other info mat should be added

    # mat slicing and sorting
    for idx_sigma in range (0, int(row/val_sigma)):
        for idx_cw in range (0, int(col/val_cw)):
            mat_slice = mat_in[idx_sigma*val_sigma:(idx_sigma+1)*val_sigma, idx_cw*val_cw:(idx_cw+1)*val_cw]
            # count and sort nnz
            vec_nnz = np.zeros(val_sigma)
            for t_sigma in range(0, val_sigma):
                nnz = np.count_nonzero(mat_slice[t_sigma,:])
                vec_nnz[t_sigma]= nnz
                # fill in the col idx
                if (nnz!=0):
                    mat_col_idx[idx_sigma*val_sigma+t_sigma, idx_cw*val_cw:idx_cw*val_cw+nnz]=np.nonzero(mat_slice[t_sigma,:])[0]

            mat_col_idx[idx_sigma*val_sigma:(idx_sigma+1)*val_sigma, idx_cw*val_cw:(idx_cw+1)*val_cw] =  mat_col_idx[idx_sigma*val_sigma + np.argsort(-vec_nnz), idx_cw*val_cw:(idx_cw+1)*val_cw]
            mat_show[idx_sigma*val_sigma:(idx_sigma+1)*val_sigma, idx_cw*val_cw:(idx_cw+1)*val_cw]=mat_slice[np.argsort(-vec_nnz),:]
            mat_permut[idx_sigma*val_sigma:(idx_sigma+1)*val_sigma, idx_cw]=np.argsort(-vec_nnz)

    print("Finish SELL format construction.")

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

    # # SELL-C-\sigma construction
    # sell_construct(mat_array, [ROW, COL])




    res = mat_array.dot(vec_int)

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