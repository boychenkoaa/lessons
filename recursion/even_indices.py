def print_even_indices_LR(li: list, left_index: int, right_index: int):
	if right_index - left_index <= 1:
		print(li[left_index], end = ' ')
	else:
		print_even_indices_LR(li, left_index+2, right_index)

def print_even_indices(li: list):
	print_even_indices_LR(li, 0, len(li)-1)
	
