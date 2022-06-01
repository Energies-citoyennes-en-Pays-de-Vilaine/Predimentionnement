#ifndef LIBSIM_H
#define LIBSIM_H
#include <stdlib.h>
#define TOLERATED_ERROR 0.00000001
#define MAX(X, Y) ((X > Y) ? X : Y)
#define MIN(X, Y) ((X < Y) ? X : Y)

void sim_flex(double* production, double* consumption, double* dates, size_t count, double delta_dates, double flex_ratio);
void sort_indices(size_t* indices, double* diff, int length);

#endif