#ifndef LIBSIM_H
#define LIBSIM_H
#include <stdlib.h>
void sim_flex(double* production, double* consumption, double* dates, size_t count, double delta_dates, double flex_ratio);
void sort_indices(size_t* indices, double* diff, int length);

#endif