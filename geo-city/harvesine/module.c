#include <stdio.h>
#include <math.h>


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


int main(){
//    printf("%hu", EARTH_RADIUS);
    float r = harvesine_distance_impl(82.725872, 52.473092, 82.747944, 52.409325);
    printf("%f \n", r);
    return 0;
}