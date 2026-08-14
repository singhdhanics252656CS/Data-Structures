def linear_probing_insert(hash_size, data):
    hash_table = [None] * hash_size

    for value in data:
        hash_index = value % hash_size
        original_index = hash_index

       
        while hash_table[hash_index] is not None:
            hash_index = (hash_index + 1) % hash_size
            if hash_index == original_index:
                print("Hash table is full!")
                return hash_table

        hash_table[hash_index] = value

    return hash_table


hash_size = int(input("Enter size of hash table: "))
data_input = input("Enter data (space-separated numbers): ")
data = list(map(int, data_input.split()))


final_table = linear_probing_insert(hash_size, data)


print("\nFinal Hash Table:")
for i, v in enumerate(final_table):
    print(f"Index {i}: {v}")

