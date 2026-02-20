def get_character_frequency(input_string):
    frequency = {}
    for char in input_string:
        char = char.lower()  # Convert to lowercase for case-insensitive counting
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

mydict = get_character_frequency("Snow white and the Seven Dwarves")

print(mydict)
sorted_bykeys = dict(sorted(mydict.items()))
print(sorted_bykeys)