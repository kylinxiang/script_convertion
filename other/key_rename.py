list_date = ['ak:avalue','bk:bvalue','bk:cvalue','ck:cvalue','dk:evalue','ak:fvalue','ak:gvalue']

def key_rename(list_temp):
	dict_temp = {}
	for elem in list_temp:
		colon_index = elem.index(":")
		key_temp = elem[:colon_index]

		i = 1
		while key_temp in dict_temp.keys():
			key_temp = elem[:colon_index] + "%s" % i
			i += 1
		dict_temp[key_temp] = elem[colon_index+1:]
	return dict_temp

dict_date = key_rename(list_date)
for key in dict_date:
	print key
	print dict_date[key]