# -*- coding: UTF-8 -*-
import pickle
import re
import collections

def read_tm500_pickle():
    with open('tm500_cmd_para.pkl', 'rb') as it:
        dict_tm500 = pickle.load(it)
    return dict_tm500

def expand_cmd_with_duplicated_element(original_list, element, num):
    #['forw', 'L1TT', 'AddULTFC', '0', '2', '0', '5', '15', '0', '3']
    #['UL_TFC_ROW_INDEX', 'NUM_TF_IN_UL_TFC', 'TFCI', 'CTRL_GAIN', 'DATA_GAIN', 'UL_TF_INDEX_LIST', 'PREAMBLE_MESSAGE_POWER_OFFSET', 'REFERENCE_TFC_INDEX']
    #['UL_TFC_ROW_INDEX', 'NUM_TF_IN_UL_TFC', 'TFCI', 'CTRL_GAIN', 'DATA_GAIN', 'UL_TF_INDEX_LIST_1', 'UL_TF_INDEX_LIST_2']
    if int(num) > 1:
        temp_list = []
        for value in original_list:
            if re.search(r"%s" % element, value):
                for i in range(1, int(num) + 1):
                    temp_list.append(value + '_' + str(i))
            else:
                temp_list.append(value)
        return temp_list
    else:
        return original_list

def expand_cmd_for_each(original_list, start_index, end_index, num):
    # [AA, BB, CC, DD, EE]      (2, 3, 3)
    # [AA, BB, CC_1, DD_1, CC_2, DD_2, CC_3, DD_3, EE]
    if int(num) > 1:
        temp_list = original_list
        sub_list = temp_list[start_index:end_index+1]
        del temp_list[start_index:end_index+1]
        for i in range(int(num), 0, -1):
            for j in range(end_index-start_index, -1, -1):
                temp_list.insert(start_index, sub_list[j]+'_'+str(i))
        return temp_list
    else:
        return original_list

def get_para_list(cmd_represent_as_list):
    dict_cmd_paralist = read_tm500_pickle()
    number_of_parameters = len(cmd_represent_as_list) - 3
    cmd = cmd_represent_as_list[2]
    if cmd == 'sethsdschcategory':
        cmd = 'SetHsDschCategory'
    if cmd == 'sethsdschparameters':
        cmd = 'SetHsDschParameters'
    raw_para_list = dict_cmd_paralist[cmd]
    #print "PDF list: ",raw_para_list
    # ----These need expand list para----
    if cmd == "AddDLTFC":  # NUM_TF_IN_DL_TFC: DL_TF_INDEX_LIST
        return expand_cmd_with_duplicated_element(raw_para_list, "DL_TF_INDEX_LIST", cmd_represent_as_list[4])
    elif cmd == "AddULTFC":  # Optional,,    NUM_TF_IN_UL_TFC: UL_TF_INDEX_LIST
        return expand_cmd_with_duplicated_element(raw_para_list, "UL_TF_INDEX_LIST", cmd_represent_as_list[4])[0:number_of_parameters]
    elif cmd == "CfgDLCCTrCH":  # NUM_DL_PHYS_CH: DL_PHYS_CH_LIST
        temp_list = expand_cmd_with_duplicated_element(raw_para_list, "DL_PHYS_CH_LIST", cmd_represent_as_list[18])
        # NUM_TRCH: DATA_PORT_LIST
        return expand_cmd_with_duplicated_element(temp_list, "DATA_PORT_LIST", cmd_represent_as_list[13])
    elif cmd == "CfgULCCTrCH":  # NUM_TRCH: DATA_PORT_LIST
        return expand_cmd_with_duplicated_element(raw_para_list, "DATA_PORT_LIST", cmd_represent_as_list[14])
    elif cmd == "CfgPRACH":
        temp_list = ['UL_PHCH_INDEX', 'DL_PHCH_INDEX', 'LEG_INDEX', 'PREAMBLE_SCRAM_CODE', 'AICH_TIMING', 'POWER_RAMP_STEP_SIZE', 'PREAMBLE_TX_LIMIT', 'PREAMBLE_INIT_POWER', 'DL_SCRAM_CODE', 'SPREADING_CODE_INDEX', 'AICH_REL_TX_POWER', 'PREAMBLE_MESSAGE_POWER_OFFSET', 'NUM_ASC', 'AVAILABLE_ASC_SIG_LIST', 'SUB_CHANNELS_PER_ASC_LIST']
        temp_list = expand_cmd_with_duplicated_element(temp_list, 'AVAILABLE_ASC_SIG_LIST', 8)
        return expand_cmd_with_duplicated_element(temp_list, 'SUB_CHANNELS_PER_ASC_LIST', 8)


    # ----These have "for each"----
    elif cmd == "AddDDITableEntry":
        return expand_cmd_for_each(raw_para_list, 3, 4, cmd_represent_as_list[4])[0:number_of_parameters]
    elif cmd == "AddLchTableEntry":
        pass
    elif cmd == "CfgEDCHTestMode":
        temp_list = expand_cmd_for_each(raw_para_list, 7, 8, cmd_represent_as_list[23])
        return expand_cmd_for_each(temp_list, 4, 5, 8)
    elif cmd == "CfgHsScchLess":
        pass
    elif cmd == "ConfigMacHsQueues": #########

        pass
    elif cmd == "ModifyHSDPA":
        pass
    elif cmd == "ConfigMacEhs":
        pass
    elif cmd == "SetGSMMeasurement":
        pass
    elif cmd == "SetOuterLoopPowerControl":
        pass
    elif cmd == "SetSearcherMeasurement":
        pass
    elif cmd == "SetupCommonEDCH":
        pass
    elif cmd == "SetupHSDPA":# NUM_HS-SCCH: HS-SCCH_SPREAD_CODE_INDEX   #@@#
        temp_list = expand_cmd_with_duplicated_element(raw_para_list, "HS-SCCH_SPREAD_CODE_INDEX", cmd_represent_as_list[9])
        if cmd_represent_as_list[19]=='0':
            temp_list.remove("PROC_MEM_SIZE_LIST")
        return temp_list[0:number_of_parameters]
    elif cmd == "SetSIRCQIMapping":
        pass
    elif cmd == "CRABM_RAB_ESTABLISH_IND":
        return expand_cmd_for_each(raw_para_list, 1, 1, 11)
        #['RAB_COUNT', '>NSAPI_1', '>NSAPI_2', '>NSAPI_3', '>NSAPI_4', '>NSAPI_5', '>NSAPI_6', '>NSAPI_7', '>NSAPI_8', '>NSAPI_9', '>NSAPI_10', '>NSAPI_11']
    elif cmd == "CRABM_RAB_RELEASE_IND":
        return expand_cmd_for_each(raw_para_list, 1, 1, 11)
    elif cmd == "NBRABM_ACTIVATE_REQ":
        return expand_cmd_for_each(raw_para_list, 1, 5, 11)
    elif cmd == "NBRABM_DEACTIVATE_REQ":
        return expand_cmd_for_each(raw_para_list, 1, 1, 11)
    elif cmd == "CRLC_CONFIG_RAB_REQ":
        return expand_cmd_for_each(raw_para_list, 2, 2, 3)
    elif cmd == "CMAC_CONFIG_RACH_REQ":
        pass
    elif cmd == "CMAC_CONFIG_E_DCH_REQ":################################   #@@#
        temp_list = raw_para_list[:36]
        temp_list = expand_cmd_for_each(temp_list, 29, 35, 8)
        temp_list = expand_cmd_for_each(temp_list, 27, 27, 32)
        temp_list = expand_cmd_for_each(temp_list, 21, 58, 15)
        return expand_cmd_for_each(temp_list, 10, 11, 8)
    elif cmd == "CMAC_CONFIG_RX_CCTRCH_REQ":
        temp_list = expand_cmd_for_each(raw_para_list, 12, 13, 32)
        temp_list = expand_cmd_for_each(temp_list, 9, len(temp_list)-1, 8)
        return expand_cmd_for_each(temp_list, 3, 7, 36)
    elif cmd == "CMAC_CONFIG_RX_ENH_HS_DSCH_REQ":
        pass
    elif cmd == "CMAC_CONFIG_RX_HS_DSCH_REQ":#
        temp_list = expand_cmd_for_each(raw_para_list, 12, 13, 8)
        temp_list = expand_cmd_for_each(temp_list, 7, len(temp_list)-1, 8)
        return expand_cmd_for_each(temp_list, 2, 5, 36)
    elif cmd == "CMAC_CONFIG_TX_CCTRCH_REQ":
        pass
    elif cmd == "UTEST_CLOSE_LOOP_M1_REQ":
        pass
    elif cmd == "RRCSetRfFrequency":
        pass
    elif cmd == "Set Band Combinations":
        pass
    elif cmd == "SetHsScchOrder":
        pass
    else:  # ordinary cmd
        while len(raw_para_list) > number_of_parameters:
            raw_para_list.pop()  # remove optional parameter
        if len(raw_para_list) < number_of_parameters:   # Maybe have other variable parameter
            return ['error']
        return raw_para_list


if __name__ == '__main__':
    path_of_txt = r'TM500_R10_HSPA_SUE_CRM.txt'
    #test_str = "forw L1TT AddDLTFC 0 2 0 0 0 0 0 4 1"
    #test_str = "forw L1TT AddULTFC 0 2 0 5 15 0 3"
    #test_str = "forw L1TT AddULTFC 0 1 0 0 0 0 0 1"
    #test_str = "forw L1TT CfgDLCCTrCH 0 0 1 0 0 1 0 0 2 0 1 0 0 2 1 1 0 0 0 1 1 1"
    #test_str = "forw L1TT CfgULCCTrCH 2 0 1 4 1 0 0 1 0 0 0 2 0 12 0 18 127 0 1"
    #test_str = "forw L1TT CfgPRACH 0 2 12 256 0 1 1 -30 256 14 -9 -5 1 16 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0"
    
    #test_str = "forw l1tt SetupEDCH 0 0 1 1 0 0 0xFFFF 0xFFFFFFFF 2 0 0 6 11 0 0 0 1 0 0 0"
    #test_str = "forw l1tt AddDLPhCH 4 13 1 58 0 0 1 0 0 0 0 -1 0 0 0"

    #for each
    #test_str = "forw l1tt CfgEDCHTestMode 0 0 0 2 15 0 15 0 15 0 15 0 15 0 15 0 15 0 15 0 3 0 0 1 0 2 0"
    #test_str = "forw pte CRLC_CONFIG_RAB_REQ 15 1 15 0 0"
    #test_str = "forw PTE NBRABM_DEACTIVATE_REQ 2 10 11 0 0 0 0 0 0 0 0 0"
    #test_str = "forw PTE NBRABM_ACTIVATE_REQ 1 5 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    #test_str = "forw pte CRABM_RAB_RELEASE_IND 1 6 0 0 0 0 0 0 0 0 0 0"
    #test_str = "forw PTE CRABM_RAB_ESTABLISH_IND 1 5 0 0 0 0 0 0 0 0 0 0"
    #test_str = "forw L1TT AddDDITableEntry 0 0 -1"
    #test_str = "forw L1TT AddDDITableEntry 0 1 1 4 1"
    test_str = "forw PTE CMAC_CONFIG_E_DCH_REQ -1 0 10 0 50 1 8 13 -1 6 4 10 7 12 8 12 11 13 12 13 49 18 0 0 0 0 255 500 10 7 0 0 0 0 1 5 3 5 4 0 1 42 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 5 1 0 100 255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    #test_str = "forw PTE CMAC_CONFIG_RX_CCTRCH_REQ -1 0 1 0 1 5 1 255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 246 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    #test_str = "forw PTE CMAC_CONFIG_RX_HS_DSCH_REQ -1 1 4 6 0 255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 100 32 1 336 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0"
    #test_str = "forw L1TT SetupHSDPA 1 1 2 8 0 0x0457 3 3 4 5 22 8 1 1 1 1 1 5 0 0 9 0 0 0"
    #test_str = "forw L1TT SetupHSDPA 0 1 0 19 16 0x0001 1 3 0 2 1 0 0 0 1 6 0 2 0 0 1 1"

    #test_str = "forw L1 sethsdschcategory 6"
    test_str = "forw L1TT Reset"
    #test_str = "forw L1TT InitCellSearch"
    in_list = test_str.strip().split(" ")
    #in_list = ['forw', 'pte', 'USERPTE ADD PATTERNEVAL', '0', '0', '15', '0', '0']
    print "in_list: ",in_list, "len: %s" % len(in_list)
    out_list = get_para_list(in_list)
    print "out_list: ",out_list, "len: " #% len(out_list)

