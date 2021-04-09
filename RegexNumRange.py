'''
RegexNumRange 
Author: Ram Varra
Ack: Python implementation of Java algorithm by bezmax: 
    https://ideone.com/3SCvZf  
    https://stackoverflow.com/a/33539325

Generate regular expression patterns for a range (end is inclusive) of two integers.

Examples (range)
    100, 199 = 1\d\d
    0, 500 = \d, [1-9]\d, [1-4]\d\d, 500
    124, 137 = 12[4-9], 13[0-7]
    29, 34 = 29, 3[0-4]
'''

class NumRange:
    def __init__(self, start, end):
        assert isinstance(start, int) and isinstance(end, int)
        assert start <= end
        assert start >= 0 and end >= 0
        self.start = start
        self.end = end
        
    @staticmethod
    def from_end(n):
        assert isinstance(n, int)
        ln = list(str(n))
        for i in range(len(ln)-1, -1, -1):
            p = ln[i]
            ln[i] = '0'
            if p != '9':
                break
        nn = ''.join(ln)
        return NumRange(int(nn), n)
    
    @staticmethod
    def from_start(n):
        assert isinstance(n, int)
        ln = list(str(n))
        for i in range(len(ln)-1, -1, -1):
            p = ln[i]
            ln[i] = '9'
            if p != '0':
                break
        nn = ''.join(ln)
        return NumRange(n, int(nn))
    
    @staticmethod
    def join(a, b):
        return NumRange(a.start, b.end)
    
    def overlaps(self, r):
        return self.end > r.start and r.end > self.start
    
    def __repr__(self):
        return f"NR({self.start},{self.end})" 
    
    def to_regex(self, anchor=False):
        result = []
        for a, b in zip(str(self.start), str(self.end)):
            if a == b:
                result.append(a)
            else:
                if a == '0' and b == '9':
                    result.append(r'\d')
                else:
                    result.append(f'[{a}-{b}]')
        r = ''.join(result)
        if anchor:
            r = "^" + r + "$"
        return r
    
def generate_regex(start: int, end: int, anchor=False) -> list:
    '''
    Generate list of regular expression patterns (strings) that cover numerical range start to end (inclusive)
    anchor: True -> prefix ^ and suffix $ to each regex
    '''
    def left_bounds(start, end):
        result = []
        while start < end:
            r = NumRange.from_start(start)
            result.append(r)
            start = r.end + 1 
        return result

    def right_bounds(start, end):
        result = []
        while start < end:
            r = NumRange.from_end(end)
            result.append(r)
            end = r.start - 1 

        return list(reversed(result))

    left = left_bounds(start, end)
    last_left = left.pop()
    right = right_bounds(last_left.start, end)
    first_right = right[0]
    right = right[1:]
    merged = []
    merged.extend(left)

    if not last_left.overlaps(first_right):
        merged.append(last_left)
        merged.append(first_right)
    else:
        merged.append(NumRange.join(last_left, first_right))
        
    merged.extend(right)

    return [r.to_regex(anchor) for r in merged]


#--------------------------------------------------------------------------------------
if __name__ == '__main__':
    test_list = [
        (100, 199, [r'1\d\d']),
        (0, 500, [r'\d', r'[1-9]\d', r'[1-4]\d\d', '500']),
        (124, 137, ['12[4-9]', '13[0-7]']),
        (29, 34, ['29', '3[0-4]']),
    ]

    for start, end, expected_result in test_list:
        result = generate_regex(start, end)
        sr = "[" + ', '.join(result) + "]"
        ser = "[" + ', '.join(expected_result) + "]"
        if result != expected_result:
            raise Exception(f"ERROR: ({start}, {end}) got {sr} expected {ser}")
        else:
            print(f"OK: ({start}, {end}) = {sr}")
        anchored_result = generate_regex(start, end, anchor=True)
        t = [ar == "^" + r + "$" for r, ar in zip(result, anchored_result)]
        assert all(t), f"anchored result test failure -  {t} {result} !== {anchored_result}"
        print('OK: anchor test')