#include <stdio.h>
#include <limits.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>


#define deg_to_rad(deg_angle) ((deg_angle) * M_PI / 180.0)
const short EARTH_RADIUS = 6371;


int harvesine_distance_impl(double lon_1, double lat_1, double lon_2, double lat_2){
    lon_1 = deg_to_rad(lon_1);
    lat_1 = deg_to_rad(lat_1);
    lon_2 = deg_to_rad(lon_2);
    lat_2 = deg_to_rad(lat_2);

    double dlon = lon_2 - lon_1;
    double dlat = lat_2 - lat_1;
    long double angle = powl(sin(dlat/2), 2) + cos(lat_1) * cos(lat_2) * powl(sin(dlon/2), 2);
    angle = 2 * asin(sqrt(angle));
    return EARTH_RADIUS * angle;
}


int* allocate(int n){
    int* ptr = (int*)malloc(sizeof(int) * n);
    if (!ptr){
        for (int i = 0; i < n; i++){
            ptr[i] = 0;
        }
    }

    return ptr;
}

int* generate(int n){
    int* ptr = allocate(n);
    if (!ptr){
        for (int i = 0; i < n; i++){
            ptr[i] = i;
        }
    }
    return ptr;
}


int* combinations_impl(double lon_1, double lat_1, double *values, int values_size){
    int arr_size = ceil(values_size / 2);
    int* arr = generate(arr_size);
    int distance;
    int p = 0;
    for (int i = 0; i < arr_size; i++) {
        distance = harvesine_distance_impl(
            lon_1, lat_1, values[p], values[p+1]
        );
        arr[i] = distance;
        p = p + 2;
    }
    return arr;
}

int main(){
    return 0;
}
