class BloomFilter:

    def __init__(self, f_len):
        self.filter_len = f_len
        # создаём битовый массив длиной f_len ...
        self.bits = 0
        
    def hash1(self, str1):
        # 17
        ans = 0
        for c in str1:
            code = ord(c)
            ans = (17 * ans + code) % self.filter_len
        return ans        
        
    def hash2(self, str1):
        # 223 
        ans = 0
        for c in str1:
            code = ord(c)
            ans = (223 * ans + code) % self.filter_len
        return ans        
    
    def bit_mask(self, str1):
        return (1 << self.hash1(str1)) | (1 << self.hash2(str1))
    
    def add(self, str1):
        self.bits = self.bits | self.bit_mask(str1)

    def is_value(self, str1):
        mask = self.bit_mask(str1)
        return self.bits & mask == mask
    
