class HashTable:
    def __init__(self):
        self.size = 41
        self.table = [None] * self.size

    def _hash(self, key):
        return key % self.size

    def insert(self, key, item):
        hash_index = self._hash(key)
        if not self.table[hash_index]:
            self.table[hash_index] = [(key, item)]
        else:
            for pair in self.table[hash_index]:
                if pair[0] == key:
                    # If key already exists, update value
                    pair[1] = item  
                    break
            else:
                # If key not found, append new pair
                self.table[hash_index].append((key, item))  

    def lookup(self, key):
        hash_index = self._hash(key)
        if self.table[hash_index] is not None:
            for pair in self.table[hash_index]:
                if pair[0] == key:
                    # Return the Package object if key found
                    return pair[1] 
        # Return None if key not found         
        return None  
