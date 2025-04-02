# you may use pandas only for IO reason
# Using it to do sort will impact your grade
# import pandas as pd
import random
import timeit
import csv


def timeFunc(method):
    """
    Define the main body of the decorator that decorates a method.

    Returns
    -------
    Callable
        A wrapper that defines the behavior of the decorated method
    """
    def wrapper(*args, **kwargs):
        """
        Define the behavior of the decorated method
        Parameters:
            Same as the parameters used in the methods to be decorated

        Returns:
            Same as the objects returned by the methods to be decorated
        """
        start = timeit.default_timer()
        result = method(*args, **kwargs)
        # record the time consumption of executing the method
        time = timeit.default_timer() - start

        # send metadata to standard output
        print(f"Method: {method.__name__}")
        print(f"Result: {result}")
        print(f"Elapsed time of 10000 times: {time*10000} seconds")
        return result
    return wrapper


class MusicLibrary:
    def __init__(self):
        """
        Initialize the MusicLibrary object with default values.
        self.data the collect of music library
        self.rows: the row number
        self.cols: the col number
        self.nameIndex: the number represent the index of name in each element of self.data
        self.albumIndex: the number represent the index of album in each element of self.data
        self.trackIndex: the number represent the index of track in each element of self.data
        """
        self.data = []
        self.rows = 0
        self.cols = 0
        self.nameIndex = 0
        self.albumIndex = 1
        self.trackIndex = 1

    def readFile(self, fileName):
        """
        Read music data from a CSV file and store it in the self.data attribute.
        The self.rows and self.cols should be updated accordingly.
        The self.data should be [[name, albums count, track count],...]
        You could assume the file is in the same directory with your code.
        Please research about the correct encoding for the given data set,
        as it is not UTF-8.
        You are allowed to use pandas or csv reader,
        but self.data should be in the described form above.

        Parameters
        ----------
        fileName : str
            The file name of the CSV file to be read.
        """
        # Open the file with the correct encoding (e.g., 'ISO-8859-1' for non-UTF-8 files)
        with open(fileName, mode='r', encoding='ISO-8859-1') as file:
            reader = csv.reader(file)
            self.data = []  # Clear any existing data

            for row in reader:
                # Convert the row into the required format: [name, albums count, track count]
                self.data.append([str(row[0]), int(row[1]), int(row[2])])

            # Update rows and cols based on the data
            self.rows = len(self.data)
            self.cols = len(self.data[0]) if self.rows > 0 else 0

    def printData(self):
        """
        Print the data attribute stored in the library instance in a formatted manner.
        """
        print(f"{'Artist Name':<30} {'Number of Albums':<15} {'Number of Tracks':<15}")
        print("-" * 60)
        for row in self.data:
            print(f"{row[0]:<30} {row[1]:<15} {row[2]:<15}")

    def shuffleData(self):
        """
        Shuffle the data stored in the library.
        refer to the random package
        """
        random.shuffle(self.data)

    @timeFunc
    def binarySearch(self, key, keyIndex):
        """
        Perform a binary search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        # Shuffle the data before sorting
        #self.shuffleData()

        # Sort the data by the target index in ascending order
        #self.data.sort(key=lambda row: row[keyIndex])

        # Helper function for binary search
        def _binarySearch(data, key, keyIndex):
            low, high = 0, len(data) - 1
            while low <= high:
                mid = (low + high) // 2
                if data[mid][keyIndex] == key:
                    return mid
                elif data[mid][keyIndex] < key:
                    low = mid + 1
                else:
                    high = mid - 1
            return -1

        # Perform binary search
        return _binarySearch(self.data, key, keyIndex)

    @timeFunc
    def seqSearch(self, key, keyIndex):
        """
        Perform a sequential search on the data.

        Parameters
        ----------
        key : int or str
            The key to search for.
        keyIndex : int
            The column index to search in.

        Returns
        -------
        int
            The index of the row where the key is found, or -1 if not found.
        """
        # Shuffle the data before sorting
        #self.shuffleData()

        # Sort the data by the target index in ascending order
        #self.data.sort(key=lambda row: row[keyIndex])

        # Perform sequential search
        for i, row in enumerate(self.data):
            if row[keyIndex] == key:
                return i
        return -1

    @timeFunc
    def bubbleSort(self, keyIndex):
        """
        Sort the data using the bubble sort algorithm based on a specific column index.
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        # Shuffle the data before sorting
        #self.shuffleData()

        # Perform bubble sort
        n = len(self.data)
        for i in range(n):
            # Flag to check if any swapping happened in this pass
            swapped = False
            for j in range(0, n - i - 1):
                if self.data[j][keyIndex] > self.data[j + 1][keyIndex]:
                    # Swap the rows if they are in the wrong order
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    swapped = True
            # If no swapping happened, the list is already sorted
            if not swapped:
                break

    def merge(self, L, R, keyIndex):
        """
        Merge two sorted sublists into a single sorted list.
        This is the helper function for merge sort.
        You may change the name of this function or even not have it.


        Parameters
        ----------
        L, R : list
            The left and right sublists to merge.
        keyIndex : int
            The column index to sort by.

        Returns
        -------
        list
            The merged and sorted list.
        """
        merged = []
        i = j = 0

        # Merge the two sublists while maintaining sorted order
        while i < len(L) and j < len(R):
            if L[i][keyIndex] <= R[j][keyIndex]:
                merged.append(L[i])
                i += 1
            else:
                merged.append(R[j])
                j += 1

        # Append any remaining elements from L or R
        while i < len(L):
            merged.append(L[i])
            i += 1

        while j < len(R):
            merged.append(R[j])
            j += 1

        return merged

    @timeFunc
    def mergeSort(self, keyIndex):
        """
        Sort the data using the merge sort algorithm.
        This is the main mergeSort function
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        def _mergeSort(arr, keyIndex):
            # Base case: if the list has 1 or no elements, it's already sorted
            if len(arr) <= 1:
                return arr

            # Split the list into two halves
            mid = len(arr) // 2
            left = arr[:mid]
            right = arr[mid:]

            # Recursively sort both halves
            sortedLeft = _mergeSort(left, keyIndex)
            sortedRight = _mergeSort(right, keyIndex)

            # Merge the sorted halves
            return self.merge(sortedLeft, sortedRight, keyIndex)

        # Call the helper function and update self.data
        self.data = _mergeSort(self.data, keyIndex)

    @timeFunc
    def quickSort(self, keyIndex):
        """
        Sort the data using the quick sort algorithm.
        This is the main quickSort function.
        self.data will have to be in sorted order after calling this function.

        Parameters
        ----------
        keyIndex : int
            The column index to sort by.
        """
        def _quickSort(arr, keyIndex):
            # Base case: if the list has 1 or no elements, it's already sorted
            if len(arr) <= 1:
                return arr

            # Choose the pivot (using the last element in the list)
            pivot = arr[-1]

            # Partition the list into three parts: less, equal, and greater
            less = [row for row in arr[:-1] if row[keyIndex] <= pivot[keyIndex]]
            greater = [row for row in arr[:-1] if row[keyIndex] > pivot[keyIndex]]

            # Recursively sort the less and greater parts, and combine them with the pivot
            return _quickSort(less, keyIndex) + [pivot] + _quickSort(greater, keyIndex)

        # Call the helper function and update self.data
        self.data = _quickSort(self.data, keyIndex)

    def comment(self):
        '''
        Based on the result you find about the run time of calling different function,
        Write a small paragraph (more than 50 words) about time complexity, and print it.
        '''
        print("""
        The run time of calling different functions varies significantly.
        The binary search function has the lowest time complexity of O(log n),
        which is the most efficient among the four functions. The sequential search
        function has a time complexity of O(n). A binary search is most efficient than a sequential search.
        The bubble sort function has a time complexity of O(n^2), which is less efficient
        than both search functions. The merge and quick sort functions have a time complexity of O(n log n),
        which is also less efficient. The bubble sort function took the longest time so was the least efficient.
        """)



# create instance and call the following instance method
# using decroator to decroate each instance method
def main():
    random.seed(42)
    myLibrary = MusicLibrary()
    filePath = 'music.csv'
    myLibrary.readFile(filePath)

    idx = 0
    myLibrary.shuffleData()
    myLibrary.data.sort(key = lambda data: data[idx])
    myLibrary.seqSearch(key="30 Seconds To Mars", keyIndex=idx)
    myLibrary.binarySearch(key="30 Seconds To Mars", keyIndex=idx)

    idx = 2
    myLibrary.shuffleData()
    myLibrary.bubbleSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.quickSort(keyIndex=idx)
    myLibrary.shuffleData()
    myLibrary.mergeSort(keyIndex=idx)
    myLibrary.printData()

if __name__ == "__main__":
    main()

