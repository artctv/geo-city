# cython: boundscheck=False

cdef extern from "module.c" nogil:
    double harvesine_distance_impl(double lon_1, double lat_1, double lon_2, double lat_2);

cdef double harvesine_distance(double lon_1, double lat_1, double lon_2, double lat_2) nogil:
    return harvesine_distance_impl(lon_1, lat_1, lon_2, lat_2);

def calculate(double lon_1, double lat_1, double lon_2, double lat_2):
    cdef float result;
    with nogil:
        result = harvesine_distance(lon_1, lat_1, lon_2, lat_2);
    return result
