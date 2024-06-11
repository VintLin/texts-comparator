from textscomparator._utils_for_char import CharInfo
from textscomparator._utils_for_string import StringUtils
from textscomparator._utils_for_file import FileUtils

def compare_and_save(a_texts, b_texts, save_folder):
    data = compare_texts(a_texts, b_texts)
    FileUtils.save_to_json(data, save_folder)
    FileUtils.save_to_execel(data, save_folder)

def compare_texts(a_texts, b_texts):
    # 1. find matches
    a_info = CharInfo(a_texts)
    b_info = CharInfo(b_texts)
    
    # 2. first filter
    first_match_map = {}
    matches = StringUtils.find_strs_matches(a_texts, b_texts)
    for ratio, a_line_index, b_index in matches:
        
        if a_line_index not in first_match_map.keys():
            first_match_map[a_line_index] = set()
        
        if ratio == 1.0:
            a_info.set_line_match(a_line_index, CharInfo.STATE_SAME)
            b_info.set_line_match(b_index, CharInfo.STATE_SAME)
            
            first_match_map[a_line_index].add(b_index)
        else:
            if StringUtils.get_match_texts(a_info, a_line_index, b_info, b_index):
                first_match_map[a_line_index].add(b_index)
                
    first_match_map = {key: first_match_map[key] for key in sorted(first_match_map)}
    
    # 3. second filter
    second_match_map = {}
    result_map = {}
    for a_line_index, b_indices in first_match_map.items():
        # 3.1 init map
        if a_line_index not in second_match_map.keys():
            second_match_map[a_line_index] = set()
        
        # 3.2 find match str
        new_a_info = CharInfo(a_texts)
        new_b_info = CharInfo(b_texts)
        
        matches = StringUtils.find_strs_matches([a_texts[a_line_index]], [b_texts[i] for i in b_indices])
        for ratio, _, b_index in matches:
            b_line_index = list(b_indices)[b_index]
            
            if StringUtils.get_match_texts(new_a_info, a_line_index, new_b_info, b_line_index):
                second_match_map[a_line_index].add(b_line_index)
                
        second_match_map[a_line_index] = sorted(second_match_map[a_line_index])
        
        # 3.3 get font read to excel
        result_map[a_line_index] = {
            "left": {
                "text": new_a_info.lines[a_line_index], 
                "red_marks": new_a_info.get_diff_indexs(a_line_index), 
                "tag": f"Index {a_line_index + 1}"
            }, 
            "right": []
        }
        for b_line_index in list(second_match_map[a_line_index]):
            b_marks = {
                "text": new_b_info.lines[b_line_index], 
                "red_marks": new_b_info.get_diff_indexs(b_line_index),
                "tag": f"Index {b_line_index + 1}"
            }
            result_map[a_line_index]["right"].append(b_marks)
    return result_map

