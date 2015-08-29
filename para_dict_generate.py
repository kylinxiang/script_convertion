import sys, string, os,re
import collections
from get_para_list import *
from tm500_commands_list_gernerator import *

file_name = r'Reset_Hard.txt'
dict_data = os.path.splitext(file_name)[0]
temp_dict_name = dict_data
dict_data = collections.OrderedDict()
order_list_file = []

def list_rename(key, list_temp):
    i = 2
    key_temp = key
    while key in list_temp:
        key = key_temp
        key = key + "_%.2d" % i
        i += 1

    list_temp.append(key)
    return key


def dict_generate(file_name):
    cmds_in_script = []
    list_name = []
    file_read = open(file_name)
    file_data = file_read.read()
    print "Start to generate dict '%s'" % temp_dict_name

    cmds_in_script = re.findall(r'forw L\d.+ .+|forw PTE .+|WAIT FOR .+|WAIT \d+|\nRBOT\n', file_data)

    for cmd in cmds_in_script:
    	order_list_cmd = []
        layer_info = []
        elem_cmd = cmd.split()
        if elem_cmd[0] == 'forw' or elem_cmd[0] == 'RBOT':
            if elem_cmd[0] == 'RBOT':
                elem_cmd.insert(0,"")
                elem_cmd.insert(0,"")
            #for special commands.eg:USERPTE ADD RAB,USERPTE RMV...
            if elem_cmd[2] =='USERPTE':
                if elem_cmd[3] == 'ADD':
                    elem_cmd[2] = elem_cmd[2]+' '+elem_cmd[3]+' '+elem_cmd[4]
                    del elem_cmd[3]
                    del elem_cmd[3]
                else:
                    elem_cmd[2] = elem_cmd[2]+' '+elem_cmd[3]
                    del elem_cmd[3]
            func_key = list_rename(elem_cmd[2], list_name)
            order_list_file.append(func_key)
            dict_name = func_key
            func_key = collections.OrderedDict()
            #print elem_cmd
            para_name_list = get_para_list(elem_cmd)
            i = 0
            for para_name in para_name_list:
                func_key.update({para_name:elem_cmd[3 + i]})
                order_list_cmd.append(para_name)
                i += 1
            func_key.update({'order':order_list_cmd})
            func_key.update({'layer_info':' '.join(elem_cmd[:2])})
            dict_data.update({dict_name:func_key})

        elif elem_cmd[0] == 'WAIT':
            wait_key = list_rename('WAIT', list_name)
            order_list_file.append(wait_key)
            dict_name = wait_key
            wait_key = collections.OrderedDict()
            if len(elem_cmd) == 2:
            	#for special commands.eg:WAIT 1
                wait_key.update({'WAIT':elem_cmd[1]})
            else:
                wait_key.update({'WAIT FOR':cmd.strip('WAIT FOR ')})
            dict_data.update({dict_name:wait_key})

    dict_data.update({'order':order_list_file})
    del cmds_in_script[:]


def file_generate(dict_para, txt_name):
    txt_name = os.path.splitext(txt_name)[0]
    name_temp = (txt_name +'(Robot)' +'.txt').replace(' ', '_')

    if os.path.exists(name_temp):
        print "Warning:'%s' already exists" % name_temp
        os.remove(name_temp)
    try:
        file_obj = open(name_temp, 'w')
    except IOError as err:
        print('file open error: {0}'.format(err))

    print "Start to generate file '%s'" % name_temp
    file_obj.writelines('*** Settings ***\n')
    file_obj.writelines('Library           ../lrc3g_robot/tool_ext/tool_UESIM/tm500_commands_list_gernerator.py\n\n\n')
    
    file_obj.writelines('*** Variables ***')
    for key in dict_para.keys()[:-1]:
        file_obj.writelines('\n&{%s}' % key)
        file_obj.writelines('    %s=%s' % (x,dict_para[key][x]) for x in dict_para[key])
    file_obj.writelines('\n@{%s}    %s' % ('order','    '.join(dict_para['order'])))
    file_obj.writelines('\n&{%s}' % txt_name)
    for key in dict_para:
        file_obj.writelines('    %s=${%s}' % (key, key))  # (filter(str.isalpha,key)
    file_obj.writelines('\n')

    file_obj.writelines('\n*** Keywords ***\n')
    file_obj.writelines('%s\n' % txt_name)
    file_obj.writelines('    [Arguments]    ${%s}    ${host}=${CFG_TM500_ControlPC_IP}    ${port}=${CFG_TM500_MDL_Port}\n' % txt_name)
    file_obj.writelines('    ${commands}    tm500_commands_list_gernerator    ${%s}\n'% txt_name)
    file_obj.writelines('    log    ${commands}\n')
    file_obj.writelines('    SendCommandLines2Tm500    ${commands}    ${host}    ${port}\n')
    file_obj.writelines('    [Return]    ${commands}\n')
    file_obj.close()
    print 'Completed'


if __name__ == '__main__':
    dict_generate(file_name)
    file_generate(dict_data,file_name)
    #for key in dict_data:
    #    print key, dict_data[key]
