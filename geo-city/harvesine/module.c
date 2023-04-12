#include <stdio.h>
#include <limits.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>


#define deg_to_rad(deg_angle) ((deg_angle) * M_PI / 180.0)
const short EARTH_RADIUS = 6371;


double harvesine_distance_impl(double lon_1, double lat_1, double lon_2, double lat_2){
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


double* allocate(int n){
    double* ptr = (double*)malloc(sizeof(double) * n);
    if (!ptr){
        for (int i = 0; i < n; i++){
            ptr[i] = 0;
        }
    }

    return ptr;
}

double* generate(int n){
    double* ptr = allocate(n);
    if (!ptr){
        for (int i = 0; i < n; i++){
            ptr[i] = (double)i;
        }
    }
    return ptr;
}

//void show_array (double array[], int number_of_elements)
//{
//   for (int i = 0; i < number_of_elements; i++) {
//       printf("%f10\t", array[i]);
//   }
//   printf("\n");
//}

const int queue_size = 2;

double* combinations_impl(float *queue_values, float *elemts_values, int elemts_size){
    int arr_size = ceil(elemts_size / 2);
    double* arr = generate(arr_size);
    double distance;
    int p = 0;
    for (int i = 0; i < arr_size; i++) {
        distance = harvesine_distance_impl(
            queue_values[0], queue_values[1], elemts_values[p], elemts_values[p+1]
        );
        arr[i] = distance;
        p = p + 2;
    }
    return arr;
}


int main(){
//    queue_item = ["str", "float", "float"] -> "str", ["float", "float"]
//    char queue_key[100] = "п Алейский";
//    float queue_values[2] = {82.725872, 52.473092};
//
////    elemts = {"str": ["float", "float"] ...}
//    char elemts_keys[][30] = {"с Малахово", "п Мамонтовский", "п Октябрьский"};
//    float elemts_values[6] = {
//        82.747944, 52.409325, 84.753586, 51.747974, 82.762632, 52.343874
//    };
//    double *arr = combinations_impl(queue_values, elemts_values, 6);
//    show_array(arr, 3);
//    int n = sizeof elemts_keys[0] / sizeof *elemts_keys[0];
//    strcat(queue_key, elemts_keys[0]);
//    printf("%s\n", queue_key);

    return 0;
}


//    char items[][10] = {"10", "11"};
//    show_array(item, 10);


//   int little_numbers[5] = {1, 2, 3, 4, 5};
//   int big_numbers[3] = {1000, 2000, 3000};
//   show_array(little_numbers, 5);
//   int n = sizeof little_numbers / sizeof *little_numbers;
//   printf("%d", n);
//    printf("%hu", EARTH_RADIUS);
//    float r = harvesine_distance_impl(82.725872, 52.473092, 82.747944, 52.409325);
//    printf("%f \n", r);
