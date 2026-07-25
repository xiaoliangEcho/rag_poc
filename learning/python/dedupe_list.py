l = [1, 2, 3, 2, 1, 1, 4]
# dedup 
def unique_list(l=[]):
	dict_result = {}
	final_list= []
	for i in range(len(l)):
		element = l[i]
		if element not in dict_result:
			dict_result[i] = element
			final_list.append(element)
	for k in dict_result.keys():
		print(f"the unique index {k} and value {dict_result[k]}")
	print(f"The unique list is {final_list}")
		
unique_list(l)