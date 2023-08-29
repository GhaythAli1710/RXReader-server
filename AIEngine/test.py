from AIEngine.ED_algo import nlp_step, drug_names
from AIEngine.TrOCR import image_to_stream
from PIL import Image

image = Image.open('C:/Users/Ghayth Ali/Desktop/Grad_Project/Server/RXReader-server/AIEngine/ghtest3.jpg')

prob = image_to_stream(image)
print(prob)

str = ""
tf = []
for p in prob:
    str = str + p[0]
    if p[1] >= 0.75:
        for letter in list(p[0]):
            if letter == 'Ġ':
                tf.append(False)
            else:
                tf.append(True)
    else:
        for letter in list(p[0]):
            tf.append(False)

print(str)
print(tf)

# Test input dictionary
input_dict = {
    # "t zoderm": [True, False, True, False, True, False, True],
    # "polaramine repetabs": [True, False, False, False, False, False, True,False, False, True, False, True, False, True,False, False, True, False, True],
    # "disalic 50": [True, False, True, False, False, False, True,False, False,False],
    # "unadol forte": [True, False, False, False, False, True,False, True,False, False,False,False],
    str: [True, False, False, False, False, False, False, True, True, True, True]
}


# Function to replace False characters with spaces and return the modified word
def replace_false_with_space(word):
    return ''.join(c if flag else ' ' for c, flag in zip(word, input_dict[word]))


# Loop through the dictionary, replace the original words, and add the modified words to the list
for key in input_dict.keys():
    modified_word = replace_false_with_space(key)
modified_word = modified_word.lower()
# Print the list of modified words
print(modified_word)

erroneous_characters = modified_word
closest_names = nlp_step(erroneous_characters, drug_names, num_closest=3)
print(f"The closest drug names to '{erroneous_characters}' are: {closest_names}")
