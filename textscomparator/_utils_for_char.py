


class CharInfo:
    STATE_DIFF = -1
    STATE_SAME = 1
    
    colors = {
        STATE_SAME: (0, 255, 0),  # 绿色
        STATE_DIFF: (0, 0, 255)  # 红色 完全不同
    }
    def __init__(self, lines) -> None:
        self.lines = lines
        self.match_lines = [[CharInfo.STATE_DIFF for _ in range(len(line))] for line in lines]
    
    def is_used(self, line_index, char_index):
        return self.match_lines[line_index][char_index] != CharInfo.STATE_DIFF
    
    def get_result(self):
        diff_chars = []
        same_chars = []
        for i, line in enumerate(self.match_lines):
            for j, char_state in enumerate(line):
                char = self.lines[i][j]
                if char_state == CharInfo.STATE_DIFF:
                    diff_chars.append(char)
                elif char_state == CharInfo.STATE_SAME:
                    same_chars.append(char)
                else:
                    diff_chars.append(char)
        return {
            CharInfo.STATE_DIFF: diff_chars, 
            CharInfo.STATE_SAME: same_chars
        }
    
    def set_char_match(self, line_index, char_index, state):
        self.match_lines[line_index][char_index] = state
    
    def set_line_match(self, line_index, state):
        for index in range(len(self.match_lines[line_index])):
            self.match_lines[line_index][index] = state
    
    def get_char_count(self, line_index):
        return len(self.match_lines[line_index])
    
    def get_match_count(self, line_index):
        same_indexs = [state for state in self.match_lines[line_index] if state == CharInfo.STATE_SAME]
        return len(same_indexs)
    
    def get_diff_indexs(self, line_index):
        return [index for index, char in enumerate(self.match_lines[line_index]) if char == CharInfo.STATE_DIFF]
