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
    i = 2
    key_temp = key
    while key in list_temp:
        key = key_temp
        key = key + "_%.2d" % i
        i += 1

    list_temp.append(key)
    return key
'''
def list_rename(key, list_temp):
    i = 2
    key_temp = key
    while key in list_temp:
        key = key_temp
        key = key + "_%s" % i
        if k==2:
            list_temp[-1] = list_temp[-1] + '_1'
        i += 1
    list_temp.append(key)
    return key
'''
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
                func_key.append(para_name + '=' + elem_cmd[3 + i])
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


def file_generate(dict_para, txt_name):
    txt_name = txt_name.strip('.txt').replace(' ', '_')
    name_temp = txt_name + '(Robot)' + '.txt'
    if os.path.exists(name_temp):
        print "Warning:'%s' already exists" % txt_name
        os.remove(name_temp)
    # return
    try:
        file_obj = open(name_temp, 'w')
    except IOError as err:
        print('file open error: {0}'.format(err))

    file_obj.writelines('*** Settings ***\n')
    file_obj.writelines('Resource          ../../../tool_ext/tool_UESIM/command_struct.txt\n')
    file_obj.writelines('Resource          ../../../tool_ext/tool_UESIM/generate_tm500_command.txt\n')
    file_obj.writelines('Library           ../../../tool_ext/tool_UESIM/tm500_control.py\n\n')
    
    file_obj.writelines('*** Variables ***\n')
    for key in list_order:
        if key[:4] == 'WAIT':
            continue
        file_obj.writelines('&{%s}' % key)
        file_obj.writelines('    %s' % (x) for x in dict_para[key])
        file_obj.writelines('\n')
    file_obj.writelines('&{%s}' % txt_name)
    for key in list_order:
        file_obj.writelines('    %s=${%s}' % (key, key))  # (filter(str.isalpha,key)
    file_obj.writelines('\n')

    file_obj.writelines('\n*** Keywords ***\n')
    file_obj.writelines('%s\n' % txt_name)
    file_obj.writelines(
        '    [Arguments]    ${%s}    ${host}=${CFG_TM500_ControlPC_IP}    ${port}=${CFG_TM500_MDL_Port}\n' % txt_name)
    file_obj.writelines('    ${commands}    Create List\n')
    for key in list_order:
        if key[:4] == 'WAIT':
            file_obj.writelines('    ${command}    WAIT FOR    %s\n' % (dict_para[key][1]))
            file_obj.writelines('    Append To List    ${commands}    ${command}\n')
            continue
        file_obj.writelines('    ${command}    %s    ${%s}\n' % (key, txt_name))
        file_obj.writelines('    Append To List    ${commands}    ${command}\n')
    file_obj.writelines('    log    ${commands}\n')
    file_obj.writelines('    SendCommandLines2Tm500    ${commands}    ${host}    ${port}\n')
    file_obj.writelines('    [Return]    ${commands}\n')
    file_obj.close()


if __name__ == '__main__':
    dict_generate(file_name)
    for key in list_order:
        print key, dict_data[key]
    file_generate(dict_data, file_name)
    del list_order[:]
