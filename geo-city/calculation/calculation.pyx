# cython: boundscheck=False
import cython
from libc.stdlib cimport free
from libc.string cimport memset
from cpython cimport array
import array


cdef extern from "module.c" nogil:
    int* combinations_impl(double lon_1, double lat_1, double *values, int values_size);

cdef int* harvesine_array(double lon_1, double lat_1, double *elemts_values, int elemts_size):
    return combinations_impl(lon_1, lat_1, elemts_values, elemts_size);

cdef pythonize(int *ptr, int values_size, array.array result_array):
    cdef int i
    for i in range(values_size):
        result_array[i] = ptr[i]
    return result_array

def combinations(
    lon_1: cython.double,
    lat_1: cython.double,
    values: array.array,
    values_size: cython.int,
    result_array: array.array
) -> array.array:
    cdef int* result;
    result = harvesine_array(lon_1, lat_1, values.data.as_doubles, values_size);
    result_array = pythonize(result, values_size, result_array)
    free(result)
    return result_array
