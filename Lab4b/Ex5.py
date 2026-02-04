sentence = input("Enter a sentence: ")

# 1. turn the string into a list of words
words = sentence.split(" ")

# 2. reverse the list
words.reverse()
print("Reversed list of words:", words)

# 3. join the reverse list back into a string
reversed_sentence = " ".join(words)
print("Reversed sentence:", reversed_sentence)


