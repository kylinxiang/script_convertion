# -*- coding: UTF-8 -*-
import re

def tm500_commands_list_gernerator(paras_dict):
    """
    @paras_dict : Parameters of tm500 scripts as a python dictionary,it like this
        paras_dict = {
                        'CfgDEPNG': {'DATA_PORT': '0', 'INSTANCE_NUMBER': '0', 
                                    'PN_IS_FIXED_LENGTH': '0', 'PN_OPTION': '2', 
                                    'layer_info': 'forw L1TT', 
                                    'order': "['INSTANCE_NUMBER', 'DATA_PORT',
                                                'PN_OPTION', 'PN_IS_FIXED_LENGTH']"},
                        'CfgDEPNG_02': {'DATA_PORT': '1', 'INSTANCE_NUMBER': '1',
                                        'PN_IS_FIXED_LENGTH': '0', 'PN_OPTION': '2', 
                                        'layer_info': 'forw L1TT', 
                                        'order': "['INSTANCE_NUMBER', 'DATA_PORT', 
                                                    'PN_OPTION', 'PN_IS_FIXED_LENGTH']"},
                        'order': ['CfgDEPNG', 'CfgDEPNG_02']
    }
    """
    cmds_list = map(
        lambda x:assembling_single_command_str(paras_dict,x), 
        paras_dict['order'])
    return cmds_list


def assembling_single_command_str(paras_dict,cmd_name):
    cmd_info_dict = paras_dict[cmd_name]
    cmd_name = _handle_cmd_name(cmd_name)
    return _assembling_command_str(cmd_info_dict, cmd_name).strip()


def _assembling_command_str(cmd_info_dict,cmd_name):
    if cmd_name.startswith('WAIT'):
        return ' '.join(cmd_info_dict.items()[0])
    else:
        para_list = [cmd_info_dict[i] for i in eval(cmd_info_dict['order'])]
        para_str = ' '.join(para_list)
        cmd_str = cmd_info_dict['layer_info'] + \
            ' ' + cmd_name + ' ' + para_str
        return cmd_str


def _handle_cmd_name(cmd_name):
    if re.search(r'_\d{2}', cmd_name):
        return '_'.join(cmd_name.split('_')[:-1])
    else:
        return cmd_name




if __name__ == '__main__':
    # forw L1TT CfgDEPNG 0 0 2 0
    test_dict = {
   'CfgDEPNG': {'DATA_PORT': '0', 'INSTANCE_NUMBER': '0', 'PN_IS_FIXED_LENGTH': '0', 'PN_OPTION': '2', 'layer_info': 'forw L1TT', 'order': "['INSTANCE_NUMBER', 'DATA_PORT', 'PN_OPTION', 'PN_IS_FIXED_LENGTH']"},
 'CfgDEPNG_02': {'DATA_PORT': '1', 'INSTANCE_NUMBER': '1', 'PN_IS_FIXED_LENGTH': '0', 'PN_OPTION': '2', 'layer_info': 'forw L1TT', 'order': "['INSTANCE_NUMBER', 'DATA_PORT', 'PN_OPTION', 'PN_IS_FIXED_LENGTH']"},
 'CfgDEPNG_03': {'DATA_PORT': '2', 'INSTANCE_NUMBER': '2', 'PN_IS_FIXED_LENGTH': '0', 'PN_OPTION': '2', 'layer_info': 'forw L1TT', 'order': "['INSTANCE_NUMBER', 'DATA_PORT', 'PN_OPTION', 'PN_IS_FIXED_LENGTH']"},
 'CfgDEPNG_04': {'DATA_PORT': '3', 'INSTANCE_NUMBER': '3', 'PN_IS_FIXED_LENGTH': '0', 'PN_OPTION': '2', 'layer_info': 'forw L1TT', 'order': "['INSTANCE_NUMBER', 'DATA_PORT', 'PN_OPTION', 'PN_IS_FIXED_LENGTH']"},
 'CfgDEPNG_05': {'DATA_PORT': '4', 'INSTANCE_NUMBER': '4', 'PN_IS_FIXED_LENGTH': '0', 'PN_OPTION': '2', 'layer_info': 'forw L1TT', 'order': "['INSTANCE_NUMBER', 'DATA_PORT', 'PN_OPTION', 'PN_IS_FIXED_LENGTH']"},
 'order': ['CfgDEPNG', 'CfgDEPNG_02','CfgDEPNG_03', 'CfgDEPNG_04','CfgDEPNG_05']
    }
    for i in tm500_commands_list_gernerator(test_dict):
        print i
