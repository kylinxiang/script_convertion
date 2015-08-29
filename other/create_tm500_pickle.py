# -*- coding: UTF-8 -*-
import pickle
import re
import collections

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


def get_raw_para_list_with_start_line_and_cmd(start_line_index, cmd):
    if start_line_index == None:
        return ['error']
    para_list = []
    state = "begin"
    temp_list = list_text_lines[start_line_index:]
    for index, line in enumerate(temp_list):
        #print line
        if state == "begin" and re.search(r"[ ]{4,}%s" % cmd.lower(), line.lower()):    # Match: CMD
            #print line
            state = "matched_cmd"
            continue
        if state == "matched_cmd" and re.search(r"Request [p|P]arameters", line):  # Match: Request parameters
            state = "matched_request_para"
            continue
        if state == "matched_request_para":
            #print line
            if re.search(r"Confirm parameters", line):  # Match: Confirm parameters
                return para_list
            if re.search(r"Returns", line):  # Match: Returns
                return para_list
            if re.search(r"Return [p|P]arameters", line):  # Match: Return Parameters
                return para_list
            if re.search(r"Appendix A", line):
                return para_list
            if re.match(r"\d(.\d+){1,}[ ]{4,}[A-Za-z_\-]{1,}", line):  # Match: Next cmd
                return para_list
            if re.search(r"[ ]{12}", line.strip()):    # Twelve Spaces
                para = line.strip().split("        ")[0].strip()
                if para != "Parameter name" and para != "Parameter Name" and para != "Parameter":
                    para_list.append(para)  # Match: para
                    continue
    print "Can't get para of %s!" % cmd


def create_dict_cmd_page(start_index):
    dict_cmd_page = collections.OrderedDict()
    for index, line in enumerate(list_text_lines[start_index:]):
        line = line.strip()
        if re.search(r"( \.){8,}", line):  # Match: AddTF  . . . . . . . . . . . .59
            #print line
            temp_list = re.split(r'( \.){8,}', line)
            #print temp_list
            if temp_list[0].split(" .")[0].strip() in dict_cmd_page.keys():
                continue
            dict_cmd_page[temp_list[0].split(" .")[0].strip()] = temp_list[-1].strip()
    return dict_cmd_page


def create_tm500_pickle():
    dict_cmd_paralist = collections.OrderedDict()
    fill_line_list_with_txt_file(r'TM500_R10_HSPA_SUE_CRM.txt')
    start_index = get_line_index_from_page_info(495)  # Appendix G: Alphabetical List of Commands
    dict_cmd_page = create_dict_cmd_page(start_index)
    for key_cmd, value_page in dict_cmd_page.items():
        #print key_cmd,": ",value_page
        start_line_index = get_line_index_from_page_info(value_page)
        raw_list = get_raw_para_list_with_start_line_and_cmd(start_line_index, key_cmd)
        if key_cmd == "CPDCP_CONFIG_REQ":
            raw_list = ['User Radio Bearer ID','Lossless SRNS support','Is PDCP header ABSENT',
                        'Number of Algos','Algo choice','rfc2507 bitmask','rfc2507 Max Period',
                        'rfc2507 Max Time','rfc2507 Max Header','rfc2507 TCP Space','rfc2507 Non-TCP Space',
                        'Expect re-ordering','RLC Mode','In sequence delivery','SN sync required','Header compression re-init']
        if key_cmd == "AddDLPhCH":
            raw_list =['DL PhCH index','DL PhCH leg index','DL PhCH On/Off','DL PCP Slot format index',
                        'Transmit Diversity Mode','DL PhCH Scrambling code','DL PhCH Spreading code index',
                        'CPICH Scrambling code','CPICH Spreading code index','Td Over Null','Alternate Scrambling Code Request',
                        'TPC Combination Index','Phase Reference Type','Multicode Index','Is channel a PDSCH']
        dict_cmd_paralist[key_cmd] = raw_list
    with open('tm500_cmd_para.pkl', 'wb') as tm500_pkl_file:
        pickle.dump(dict_cmd_paralist, tm500_pkl_file)
    print "--------------------Success create_tm500_pickle!--------------------"




if __name__ == '__main__':
    
    create_tm500_pickle()
    with open('tm500_cmd_para.pkl', 'rb') as it:
        read_dict = pickle.load(it)

    for key_cmd, value_page in read_dict.items():
        print key_cmd,": ",value_page
    '''
    
    fill_line_list_with_txt_file(r'TM500_R10_HSPA_SUE_CRM.txt')
    start_line_index = get_line_index_from_page_info(251)
    raw_list = get_raw_para_list_with_start_line_and_cmd(start_line_index, "sethsdschcategory")
    print raw_list
    '''