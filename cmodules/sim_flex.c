#include "libsim.h"
#include <stdlib.h>
#include <stdio.h>

void copy_indices(){}
void merge_arrays(size_t* indices, double* diff, size_t left_base, size_t left_count, size_t right_base, size_t right_count)
{
	size_t left_index = 0;
	size_t right_index = 0;
	size_t* merging_array = malloc(sizeof(size_t) * (left_count + right_count));
	for (int i = 0; i < left_count + right_count; i++)
	{
		if (left_index < left_count && right_index < right_count)
		{
			if (diff[indices[left_index + left_base]] < diff[indices[right_index + right_base]])
			{
				merging_array[i] = indices[left_index + left_base];
				left_index ++;
			}
			else{
				merging_array[i] = indices[right_index + right_base];
				right_index ++;
			}
		}
		else
		{
			if (left_index < left_count)
			{
				merging_array[i] = indices[left_index + left_base];
				left_index ++;
			}
			else
			{
				merging_array[i] = indices[right_index + right_base];
				right_index ++;
			}
		}
	}
	for (int i = 0; i < left_count; i++)
	{
		indices[i + left_base] = merging_array[i];
	}
	for (int i = 0; i < right_count; i++)
	{
		indices[i + right_base] = merging_array[i + left_count];
	}
	free(merging_array);
}


void merge_sort_indices(size_t* indices, double* diff, size_t left_base, size_t left_count, size_t right_base, size_t right_count)
{
	if (left_count == 1 && right_count == 1){//two elements are easy to sort
		if (diff[indices[left_base]] > diff[indices[right_base]]){
			size_t temp = indices[right_base];
			indices[right_base] = indices[left_base];
			indices[left_base] = temp;
		}
		return;
	}
	if (right_count == 0 || left_count == 0)
		return;
	size_t new_left_base = left_base;
	size_t new_left_count = left_count / 2;
	size_t new_right_base =  left_base + left_count / 2;
	size_t new_right_count = left_count - left_count / 2;
	size_t* merge_array;
	//sorts the left part
	merge_sort_indices(indices, diff, new_left_base, new_left_count, new_right_base, new_right_count);
	merge_arrays(indices, diff, new_left_base, new_left_count, new_right_base, new_right_count);

	new_left_base = right_base;
	new_left_count = right_count / 2;
	new_right_base =  right_base + right_count / 2;
	new_right_count = right_count - right_count / 2;
	merge_sort_indices(indices, diff, right_base, right_count / 2, right_base + right_count / 2, right_count - right_count / 2);
	merge_arrays(indices, diff, new_left_base, new_left_count, new_right_base, new_right_count);
}
void sort_indices(size_t* indices, double* diff, int length)
{
	merge_sort_indices(indices, diff, 0, length / 2, length / 2, length - length / 2);
	merge_arrays(indices, diff, 0, length / 2, length / 2, length - length / 2);
}

double* caculate_diff(double* production, double* consumption, size_t count)
{
	double* diff = malloc(count * sizeof(double));
	for (int i = 0; i < count; i++)
	{
		diff[i] = consumption[i] - production[i]; 
	}
	return diff;
}

void sim_flex(double* production, double* consumption, double* dates, size_t count, double delta_dates, double flex_ratio)
{
	double* diff = caculate_diff(production, consumption, count);
	double last_date = dates[0];
	double total_power = 0;
	int j = 0;
	for (int i = 0; i < count; i++)
	{
		if (dates[i] - last_date > delta_dates || i == count - 1)
		{
			int width = i - j;
			size_t* day_indices = malloc(sizeof(size_t) * width);
			for (int k = 0; k < width; k++){
				day_indices[k] = k + j; 
			}
			sort_indices(day_indices, diff, width);

			double flex_up = total_power * flex_ratio;
			double flex_down = flex_up;
			int right_index = width - 1;
			double diff_with_last;
			while (flex_down > TOLERATED_ERROR)
			{
				diff_with_last = flex_down / (width - right_index);
				if (right_index > 0)
				{
					diff_with_last = diff[day_indices[right_index]] - diff[day_indices[right_index - 1]];
				}

				diff_with_last = MIN(diff_with_last, flex_down / (width - right_index));
				for (int i = right_index; i < width; i++)
				{
					diff[day_indices[i]] -= diff_with_last;
					consumption[day_indices[i]] -= diff_with_last;
					flex_down -= diff_with_last;
				}
				if (right_index > 0)
					right_index --;
			}
			
			int left_index = 0;
			while (flex_up > TOLERATED_ERROR)
			{
				diff_with_last = flex_up / (left_index + 1);
				if (left_index + 1 < width)
				{
					diff_with_last = diff[day_indices[left_index + 1]] - diff[day_indices[left_index]];
				}
				diff_with_last = MIN(diff_with_last, flex_up / (left_index + 1));
				for (int i = 0; i < left_index + 1; i++)
				{
					diff[day_indices[i]] += diff_with_last;
					consumption[day_indices[i]] += diff_with_last;
					flex_up -= diff_with_last;
				}
				if (left_index + 1 < width)
				left_index ++;
			}
			
			//going to next period
			last_date = dates[i];
			j = i;
			total_power = 0;
			free(day_indices);
		}
		total_power += consumption[i];
	}
	free(diff);
}