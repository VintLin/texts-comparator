import difflib
import string

from textscomparator._utils_for_char import CharInfo

class StringUtils:
    @staticmethod
    def get_match_texts(a_info: CharInfo, a_line_index, b_info: CharInfo, b_line_index):
        is_match = False
        a_text = a_info.lines[a_line_index]
        b_text = b_info.lines[b_line_index]
        a_match_indexs, b_match_indexs = StringUtils.unchanged_indices(a_text, b_text)
        filter_a_indexs, filter_b_indexs = [], []
        # filter is used
        for i in range(len(a_match_indexs)):
            if not a_info.is_used(a_line_index, a_match_indexs[i]) and \
                not b_info.is_used(b_line_index, b_match_indexs[i]):
                filter_a_indexs.append(a_match_indexs[i])
                filter_b_indexs.append(b_match_indexs[i])
        # filter condition
        match_indexs = StringUtils.filter_indices(a_text, filter_a_indexs, b_text, filter_b_indexs)
        match_count = len(match_indexs)
        total_count = b_info.get_char_count(b_line_index)
        if match_count / total_count  > 0.1 or match_count == total_count:
            for min_char_index, max_char_index in match_indexs:
                a_info.set_char_match(a_line_index, min_char_index, CharInfo.STATE_SAME)
                b_info.set_char_match(b_line_index, max_char_index, CharInfo.STATE_SAME)
                is_match = True
        return is_match        
        
    @staticmethod
    def find_strs_matches(a_texts, b_texts):
        result = []
        for a_index, a_text in enumerate(a_texts):
            matches = StringUtils.find_matches(a_text, b_texts)
            for b_index, b_text, ratio  in matches:
                if ratio >= 0.1 or StringUtils.is_pinyin(b_text):
                    result.append([ratio, a_index, b_index])
        return sorted(result, key=lambda x: x[0], reverse=True)
        
    @staticmethod
    def find_matches(a_text, b_texts):
        matches = []
        for b_index, b_text in enumerate(b_texts):
            ratio = StringUtils.similarity_ratio(a_text, b_text, use_contains=True)
            matches.append([b_index, b_text, ratio])
        
        sorted_matches = sorted(matches, key=lambda x: x[2], reverse=True)
        
        return sorted_matches

    @staticmethod
    def get_split_texts(char_index, line, include=6):
        texts = set()
        for left_index in range(include, -1, -1):
            for right_index in range(include, -1, -1):
                start_index = char_index - left_index
                start_index = 0 if start_index < 0 else start_index
                
                end_index = char_index + right_index
                end_index = len(line) - 1 if end_index >= len(line) else end_index

                text = line[start_index: end_index + 1]
                
                if len(text) > 4 or len(line) == len(text):
                    texts.add((char_index - start_index, text))
        
        texts = sorted(texts, key=lambda x: len(x[1]), reverse=True)
        return texts
    
    @staticmethod
    def unchanged_indices(a, b):
        diffs = StringUtils.diff_list(a, b)
        unchanged_a = []
        unchanged_b = []

        for diff in diffs:
            tag, i1, i2, j1, j2 = diff
            if tag == 'equal':
                unchanged_a.extend(range(i1, i2))
                unchanged_b.extend(range(j1, j2))
        
        return unchanged_a, unchanged_b
    
    @staticmethod
    def filter_indices(a, unchanged_a, b, unchanged_b):
        min_length = 3
        is_span = True
        
        filtered_indices_a = StringUtils.filter_consecutive(unchanged_a, min_length=min_length, is_span=is_span)
        filtered_indices_b = StringUtils.filter_consecutive(unchanged_b, min_length=min_length, is_span=is_span)
        
        filtered_pairs = []
        for index in range(len(unchanged_a)):
            if index in filtered_indices_a and index in filtered_indices_b:
                filtered_pairs.append((unchanged_a[index], unchanged_b[index]))
        
        return filtered_pairs
    
    @staticmethod
    def filter_consecutive(indices, min_length=2, is_span=False):
        result_indices = []
        current_sequence = []

        for i, index in enumerate(indices):
            if not current_sequence:
                current_sequence.append(i)
            else:
                if index == indices[current_sequence[-1]] + 1 or (is_span and index == indices[current_sequence[-1]] + 2):
                    current_sequence.append(i)
                else:
                    if len(current_sequence) >= min_length:
                        result_indices.extend(current_sequence)
                    current_sequence = [i]

        if len(current_sequence) >= min_length:
            result_indices.extend(current_sequence)

        return result_indices
    
    @staticmethod
    def similarity_ratio(a, b, remove_punctuation=True, use_contains=False):
        if remove_punctuation:
            a = StringUtils.remove_punctuation(a)
            b = StringUtils.remove_punctuation(b)
            
        ratio = difflib.SequenceMatcher(None, a, b).ratio()
        if use_contains and ratio < 0.1 and StringUtils.contains_four_consecutive(a, b):
            return 0.1
        else:
            return ratio
    
    @staticmethod
    def contains_four_consecutive(a, b):
        """
        Checks whether two strings contain four consecutive contiguous characters.
        """
        for i in range(len(a) - 3):  # -3 is because there must be at least four consecutive characters
            sub_a = a[i:i+4]
            if sub_a in b:
                return True
        return False
    
    @staticmethod
    def remove_punctuation(text):
        # Chinese punctuation marks
        chinese_punctuation = " 。？！，、；：“”‘’（）《》【】——…"
        all_punctuation = string.punctuation + chinese_punctuation
        translator = str.maketrans('', '', all_punctuation)
        return text.translate(translator)
    
    @staticmethod
    def diff_list(a, b):
        # Use difflib to get the difference between two strings
        s = difflib.SequenceMatcher(None, a, b)
        diffs = []
        for tag, i1, i2, j1, j2 in s.get_opcodes():
            diffs.append((tag, i1, i2, j1, j2))
        return diffs
