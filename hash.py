class hashTable:
    def __init__(self, size = 40):
        self.size = size
        self.table = [None] * size

    def hash(self, key):
        return hash(key) % self.size
        
    def insert(self, key, value):
        i = self.hash(key) # generate hash key
        if self.table[i] is None:
            # if new hash key, initialize list
            self.table[i] = [(key, value)]
        else:
            for j, (existing_key, _) in enumerate(self.table[i]):
                if existing_key == key:
                    # if key exists, update value
                    self.table[i][j] = (key, value)
                    break
                else:
                    # if new key, append to end
                    self.table[i].append((key, value))
    
    def search(self, key):
        i = self.hash(key) # generate hash key
        if self.table[i] is not None:
            for storedKey, value in self.table[i]:
                if storedKey == key:
                    return value
        else:
            print("No matching key was found.")
            return