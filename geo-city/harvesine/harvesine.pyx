# cython: boundscheck=False
from cpython cimport array
from libc.stdlib cimport free

cdef extern from "module.c" nogil:
    double harvesine_distance_impl(double lon_1, double lat_1, double lon_2, double lat_2);
    double* combinations_impl(float *queue_values, float *elemts_values, int elemts_size);

cdef double harvesine_distance(double lon_1, double lat_1, double lon_2, double lat_2) nogil:
    return harvesine_distance_impl(lon_1, lat_1, lon_2, lat_2);

def calculate(double lon_1, double lat_1, double lon_2, double lat_2):
    cdef double result;
    with nogil:
        result = harvesine_distance(lon_1, lat_1, lon_2, lat_2);
    return result

cdef convert_to_python(double *ptr, int n):
    cdef int i
    lst=[]
    for i in range(n):
        lst.append(ptr[i])
    return lst

cdef double* harvesine_array(float *queue_values, float *elemts_values, int elemts_size) nogil:
    return combinations_impl(queue_values, elemts_values, elemts_size);

def combinations(queue_values, elemts_values, elemts_size):
    cdef double* result;
    cdef array.array queue_values_arr = array.array('f', queue_values);
    cdef array.array elemts_values_arr = array.array('f', elemts_values);
    result = harvesine_array(queue_values_arr.data.as_floats, elemts_values_arr.data.as_floats, elemts_size);
    r = convert_to_python(result, elemts_size)
    free(result)
    return r