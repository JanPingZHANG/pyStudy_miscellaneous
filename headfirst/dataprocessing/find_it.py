def find_closest (look_for,target_data):
	def whats_the_differents(first,second):
		if first==second:
			return (0)
		if first > second:
			return (first-second)
		else:
			return (second-first)
	max_diff=99999
	for each_thing in target_data:
		diff=whats_the_differents(each_thing,look_for)
		if 0 == diff:
			find = each_thing
			break
		if diff < max_diff:
			max_diff=diff
			find=each_thing
	return (find)
