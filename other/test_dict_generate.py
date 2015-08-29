import sys, string, os
import re
from TM500_read_cmd import *

file_name = r'Setup UL DCH for 384k(TTI20)_SF4.txt'
path_of_txt = r'TM500_R10_HSPA_SUE_CRM.txt'
dict_data = file_name.strip('.txt')
print dict_data
dict_data = {}
list_order = []


def list_rename(key, list_temp):
    i = 1
    key_temp = key
    while key in list_temp:
        key = key_temp
        key = key + "%s" % i
        i += 1
    list_temp.append(key)
    return key


def dict_generate(file_name):
    cmds_in_script = []
    list_name = []
    file_read = open(file_name)
    file_data = file_read.read()

    cmds_in_script = re.findall(r'forw L1TT .+|forw PTE .+|WAIT FOR .+', file_data)

    for cmd in cmds_in_script:
        elem_cmd = cmd.split()
        if elem_cmd[0] == 'forw':
            func_key = list_rename(elem_cmd[2], list_name)
            dict_name = func_key
            list_order.append(dict_name)
            func_key = []
            para_name_list = get_para_list(path_of_txt, elem_cmd)
            i = 0
            for para_name in para_name_list:
                func_key.append(para_name)# + '=' + elem_cmd[3 + i])
                i += 1

            dict_data[dict_name] = func_key
        elif elem_cmd[0] == 'WAIT':
            wait_key = list_rename('WAIT', list_name)
            dict_name = wait_key
            list_order.append(dict_name)
            wait_key = []
            wait_key.append('WAIT FOR')
            wait_key.append(cmd.strip('WAIT FOR '))
            dict_data[dict_name] = wait_key
    del cmds_in_script[:]


if __name__ == '__main__':
    dict_generate(file_name)
    for key in list_order:
        print key, dict_data[key]
    del list_order[:]
