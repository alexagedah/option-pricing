import numpy as np

def Quicksort(arr):
	if len(arr) <= 1:
		return arr
	else:
		pivot = arr[0]
		sub_arr1 = []
		sub_arr2 = []
		for i in arr[1:]:
			if i < pivot:
				sub_arr1.append(i)
			else:
				sub_arr2.append(i)
		return Quicksort(sub_arr1) + [pivot] + Quicksort(sub_arr2)

print(Quicksort(np.random.permutation(50)))