class InsertionSort:
    def __init__(self, numList):
        self.sorted = False
        self.pointer = 1
        self.numList = numList
        self.numOfElements = len(numList)

    def sort(self):
        for i in range(1, self.numOfElements):
            key = self.numList[i]
            j = i - 1    
            while key < self.numList[j] and j >= 0: #While larger values exist in the sublist and the pointer hasn't reached the end
                self.numList[j + 1] = self.numList[j]
                j -= 1
            self.numList[j + 1] = key
        return self.numList
 
if __name__ == "__main__":
    numList = [64, 11, 142, 99, 14, 49, 73, 381, 5, 6]
    sort = InsertionSort(numList)
    result = sort.sort()
    print(result)