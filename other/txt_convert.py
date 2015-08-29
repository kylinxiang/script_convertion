import sys,string

def list_rename(key,list_temp):
	i = 1
	key_temp = key
	while key in list_temp:
		key = key_temp
		key = key + "%s" % i
		i += 1
	list_temp.append(key)
	return key

def txt_convert(file_data):
	list_temp = []
	list_backup = []
	list_name = []
	while True:
		line = file_data.readline()
		if line.split():
			line = line.strip()
			line_temp = line.split()
			if line_temp[0] == '#' and '.' in line_temp[1]:
				num = line_temp[1].strip('.')
				if num.isdigit():
					list_temp.append(line[7:]) 
			elif line[0] != '#':
				dict_name = ''
				if line_temp[0] == 'WAIT':
					wait_key = list_rename('WAIT',list_name)
					dict_name = wait_key
					wait_key = {}
					wait_key['WAIT FOR'] = line.strip('WAIT FOR ')
					dict_data[dict_name] = wait_key

				else:
					if not any(list_temp):
						list_temp = list_backup[:]
						del list_backup[:]
					func_key = list_rename(line_temp[2],list_name)
					dict_name = func_key
					func_key = {}
					i=0
					for elem in list_temp:			
						func_key[elem] = string.atoi(line_temp[3+i])
						i = i+1
					list_backup = list_temp[:]
					del list_temp[:]
					dict_data[dict_name] = func_key
			else:
				pass
		elif line == b"":
			break

file_name = r'ReleaseDCCHandHSDPA.txt'
file_read = open(file_name)
dict_data = file_name.strip('.txt')
print dict_data
dict_data = {}

txt_convert(file_read)

for key in dict_data:
	print key,dict_data[key]
file_read.close()
