# -*- coding: UTF-8 -*-
import re

list_text_lines = []


def fill_line_list_with_txt_file(path_of_txt):
    with open(path_of_txt) as f:
        list_text_lines.extend(f.readlines())
        # print "lines of file:",len(list_text_lines)


def get_line_index_from_page_info(page_id):
    # ----------------------- Page 230-----------------------
    for idx, ele in enumerate(list_text_lines):
        if re.search(r"-{23} Page %s-{23}" % str(page_id), ele):  # Match: ---- Page xxx----
            # print "Page %s in line: %s" % (page_id, idx)
            return idx
    print "No Found This Page!    page: %s" % str(page_id)


def get_page_id_with_cmd_and_line_range(ending_line_index, cmd):
    if cmd == "CMAC_REMOVE_SEC_E_DCH_REQ":
        return "313"
    for idx, ele in enumerate(list_text_lines[:ending_line_index]):
        if re.search(r"[ ]{4}%s[ ]{1,4}" % cmd, ele):  # Match: "    CMD "
            cmd_page = ele.strip().split(' ')[-1]
            # print "Found CMD: %s!   cmd page: %s" % (cmd, cmd_page)
            return cmd_page
    print "No Found This CMD!    CMD: %s" % cmd


def get_raw_para_list_with_start_line_and_cmd(start_line_index, cmd):
    if start_line_index == None:
        return ['error']
    para_list = []
    state = "begin"
    temp_list = list_text_lines[start_line_index:]
    for index, line in enumerate(temp_list):
        if state == "begin" and re.search(r"%s" % cmd, line):    # Match: CMD
            state = "matched_cmd"
            continue
        if state == "matched_cmd" and re.search(r"Request parameters", line):  # Match: Request parameters
            state = "matched_request_para"
            continue
        if state == "matched_request_para":
            if re.search(r"[ ]{0,4}Confirm parameters", line):  # Match: Confirm parameters
                return para_list
            if re.search(r"[ ]{0,4}Returns", line):  # Match: Returns
                return para_list
            if re.search(r"[ ]{0,4}Return [p|P]arameters", line):  # Match: Return Parameters
                return para_list
            if re.search(r"\d[.\d]{0,}[ ]{4,}[A-Za-z_\-]{1,}", line):  # Match: Next cmd
                return para_list
            #if re.search(r"[ ]{0,8}[A-Z_\-][ ]{8}", line):  # Match: para
                #para_list.append( line.strip().split("    ")[0] )
            if re.search(r"[ ]{12}", line.strip()):    # Twelve Spaces
                para = line.strip().split("        ")[0]
                if para != "Parameter name":
                    para_list.append(para)  # Match: para
                    continue
    print "Can't get para of %s!" % cmd


def expand_cmd_with_duplicated_element(original_list, element, num):
    if num != '1':
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


def get_para_list(path_of_txt, cmd_represent_as_list):
    number_of_parameters = len(cmd_represent_as_list) - 3
    cmd = cmd_represent_as_list[2]
    fill_line_list_with_txt_file(path_of_txt)
    end_index = get_line_index_from_page_info(11)  # preface page is 11, end of contents
    cmd_page_idx = get_page_id_with_cmd_and_line_range(end_index, cmd)  # page num of cmd
    cmd_start_line_idx = get_line_index_from_page_info(cmd_page_idx)  # cmd start line
    raw_para_list = get_raw_para_list_with_start_line_and_cmd(cmd_start_line_idx, cmd)  # cmd para list
    #print "PDF list: ",raw_para_list

    if cmd == "AddDLTFC":  # NUM_TF_IN_DL_TFC: DL_TF_INDEX_LIST
        return expand_cmd_with_duplicated_element(raw_para_list, "DL_TF_INDEX_LIST", cmd_represent_as_list[4])

    elif cmd == "AddULTFC":  # Optional,,    NUM_TF_IN_UL_TFC: UL_TF_INDEX_LIST
        temp_list = expand_cmd_with_duplicated_element(raw_para_list, "UL_TF_INDEX_LIST", cmd_represent_as_list[4])
        while len(temp_list) > number_of_parameters:
            temp_list.pop()
        return temp_list

    elif cmd == "CfgDLCCTrCH":  # NUM_DL_PHYS_CH: DL_PHYS_CH_LIST
        temp_list = expand_cmd_with_duplicated_element(raw_para_list, "DL_PHYS_CH_LIST", cmd_represent_as_list[18])
        # NUM_TRCH: DATA_PORT_LIST
        return expand_cmd_with_duplicated_element(temp_list, "DATA_PORT_LIST", cmd_represent_as_list[13])
    elif cmd == "CfgULCCTrCH":  # NUM_TRCH: DATA_PORT_LIST
        return expand_cmd_with_duplicated_element(raw_para_list, "DATA_PORT_LIST", cmd_represent_as_list[14])
    elif cmd == "CfgPRACH":
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

    #test_str = "forw PTE CRLC_CONFIG_RAB_REQ 5 1 5 0 0"
    #test_str = "forw l1tt SetupEDCH 0 0 1 1 0 0 0xFFFF 0xFFFFFFFF 2 0 0 6 11 0 0 0 1 0 0 0"
    #test_str = "forw l1tt AddDLPhCH 4 13 1 58 0 0 1 0 0 0 0 -1 0 0 0"
    test_str = "forw pte USERPTE ADD PATTERNEVAL 0 0 15 0 0"
    #in_list = test_str.strip().split(" ")
    in_list = ['forw', 'pte', 'USERPTE ADD PATTERNEVAL', '0', '0', '15', '0', '0']
    print "in_list: ",in_list
    out_list = get_para_list(path_of_txt, in_list)
    print "out_list: ",out_list

