from Tokenizer import Tokenizer

# Initialize
tokenizer = Tokenizer()

#Train (Run this once)
tokenizer.train("the_complete_work.txt", 4000)

#ENCODE & DECODE A SENTENCE
text = "I think the noble Duke is good"
print(f"Original: {text}")

ids = tokenizer.encode(text)
print(f"Encoded: {ids}")

decoded = tokenizer.decode(ids)
print(f"Decoded: {decoded}")