# Name: Nathan Thompson
# OSU Email: thomnath@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 4/23/22
# Description: Creating methods to make Dynamic Array a functional class


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)
        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Changes the size of the array, and migrates all elements to a new array with a capacity double that of the
        existing array. If new_capacity < existing size (number of non-None elements), no action is taken.

        :param new_capacity: the integer size of the array the replaces the current array

        :returns: none (replaces existing array with new array of greater size)
        """
        # Check to see if the new capacity given is valid
        if self._size > new_capacity or new_capacity < 1:
            return
        # Change new value of the capacity, create a new array with that capacity, and transfer existing values
        self._capacity = new_capacity
        new_temp_arr = StaticArray(new_capacity)
        for num in range(self._size):
            new_temp_arr._data[num] = self._data[num]
        self._data = new_temp_arr._data

    def append(self, value: object) -> None:
        """
        Appends a value to the first empty index of a dynamic array. If the array does not have capacity to accept
        the new value, the resize method is invoked.

        :param value: value to be inserted at the end of the array

        :returns: none; modifies the array
        """
        if self._size == self._capacity:
            # this doubles the capacity
            self.resize(self._capacity*2)
        self._data[self._size] = value
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserts a given value at a given place in the array. Must be sequential; that is, there cannot be 'gaps'
        consisting of 'None' values between elements. Shifts all elements in the array.

        :param index: The index that will hold the value that is to be inserted

        :param value: The value that is to be inserted at the index

        :returns: none; modifies array
        """
        if index > self._size or index < 0:
            raise DynamicArrayException
        if index > self._capacity or self._size+1 > self._capacity:
            self.resize(self._capacity*2)
        # Find the last filled index in the array, and move 'right' if size > 0
        target_ind = self._size - 1
        if target_ind < index or self._size == 0:
            self._data[index] = value
            self._size += 1
        else:
            self.append(self._data[target_ind])
            while target_ind != index:
                self._data[target_ind] = self._data[target_ind - 1]
                target_ind -= 1
            self._data[index] = value

    def remove_at_index(self, index: int) -> None:
        """
        Replaces the value at the given index with the value of its neighbor, shifting all elements of the array and
        replacing the final element with 'None'

        :param index: The index of the array that holds the value to be replaced.

        :returns: none; modifies array
        """
        if index >= self._size or index < 0 or self._size == 0:
            raise DynamicArrayException
        # Resize array if needed
        if (self._size) < (self._capacity * .25):
            if (self._capacity / 2) > 10:
                self.resize(int(self._size * 2))
            elif self._capacity > 10:
                self.resize(10)
        self._size -= 1
        # Move all elements until we hit None or the end of the array, and replace the last element with 'None'
        while self._data[index] != None and index < self.length():
            self._data[index] = self._data[index + 1]
            index += 1
            if index == self._size:
                self._data[index] = None

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Returns a new array with selected elements of the starting array.

        :param start_index: the index at which the slice of the existing array begins

        :param size: the number of consecutive elements of the existing array, beginning with the start_index, to
        be included in the new array

        :returns: New Dynamic Array, size of 'size'
        """
        if start_index < 0 or start_index >= self._size or (start_index + size) > self._size or size < 0:
            raise DynamicArrayException
        new_arr = DynamicArray()
        if size > 4:
            new_arr.resize(int(self._capacity/2))
        for num in range(size):
            new_arr.append(self._data[start_index])
            start_index += 1
        # Return the new SA as a DA
        return new_arr

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Appends all elements of the given array to an existing array

        :param second_da: a given dynamic array, all elements of which are to be appended to the existing array

        :returns: Nothing; modifies existing array in place
        """
        # Resize existing array if the capacity is insufficient
        if self._size + second_da._size > self._capacity:
            self.resize(self._capacity * 2)
        for num in range(second_da._size):
            self.append(second_da[num])

    def map(self, map_func) -> "DynamicArray":
        """
        Returns a new array, each element of which is equal to the given function apply to the current array element

        :param map_func: a regular or Lambda function to be applied to each element of the array

        :returns: A new Dynamic Array, new_arr, that contains each element of the current array to which the function
        has been applied
        """
        # Create the new array, then change its capacity to that of the current array
        new_arr = DynamicArray()
        new_arr.resize(self._capacity)
        for num in range(self._size):
            new_arr.append(map_func(self._data[num]))
        return new_arr

    def filter(self, filter_func) -> "DynamicArray":
        """
        Creates a new Dynamic Array that contains only elements from the original array that meet filter criteria

        :param filter_func: A function that acts as a conditional for appending a given element to the new array

        :returns: new_arr, a Dynamic Array with only elements from current array that meet filter criteria
        """
        new_arr = DynamicArray()
        new_arr.resize(self._capacity)
        for num in range(self._size):
            if filter_func(self._data[num]) == True:
                new_arr.append(self._data[num])
        # If our new array uses less than half the capacity, resize it
        while new_arr._size <= new_arr._capacity/2 and new_arr._capacity > 4:
            new_arr.resize(int(new_arr._capacity/2))
        return new_arr

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Supplies the value of each element in the array to a given function, then returns the result of the function.
        The function is either initialized with a given value or with the first value of the array.

        :param reduce_func: The function to be supplied with array values

        :param initializer: if not None, the value intially supplied to the function along with an array value

        :returns: the final value of after supplying each array value to the function
        """
        if self._size == 0:
            return initializer
        # Keep track of the value that we start with
        if initializer != None:
            x = initializer
            for num in range(self._size):
                x = reduce_func(x, self._data[num])
        else:
            x = self._data[0]
        #x = reduce_func(x, self._data[0])
            for num in range(self._size-1):
                x = reduce_func(x, self._data[num+1])
        return x


def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Finds the most frequently-occurring element in a sorted Dynamic Array and the number of times it occurs.

    :param arr: a sorted dynamic array

    :returns: tuple of ([dynamic array of mode value(s)], frequency)
    """
    size = arr.length()
    mode_arr = DynamicArray()
    if size == 1:
        return arr, 1
    max, num = 1, 1
    count = 1
    # Loop through once to find the maximum frequency of any value
    while num < size:
        if arr.get_at_index(num) == arr.get_at_index(num-1):
            count += 1
            num += 1
            if count > max:
                max = count
        else:
            num += 1
            count = 1
    # Reset counters and loop through a second time to append each value to the mode array if its frequency == max freq
    num = 1
    count = 1
    if max == 1:
        for num in range(size):
            mode_arr.append(arr.get_at_index(num))
    while num < size:
        if arr.get_at_index(num) == arr.get_at_index(num-1):
            count += 1
            num += 1
            if count == max:
                mode_arr.append(arr.get_at_index(num-1))
        else:
            num += 1
            count = 1
    return mode_arr, max

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [54],
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
