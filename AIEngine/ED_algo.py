def normalized_edit_distance(str1, str2):
    len1 = len(str1)
    len2 = len(str2)

    if len1 == 0:
        return len2
    if len2 == 0:
        return len1

    matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        matrix[i][0] = i

    for j in range(len2 + 1):
        matrix[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            )

    edit_distance = matrix[len1][len2]
    normalized_distance = edit_distance / max(len1, len2)
    return normalized_distance


def nlp_step(erroneous_characters, drug_names, num_closest=1):
    closest_names = []
    distances = []

    for name in drug_names:
        distance = normalized_edit_distance(erroneous_characters, name)
        distances.append((distance, name))

    distances.sort(key=lambda x: x[0])
    # print(distances)

    for i in range(min(num_closest, len(distances))):
        closest_names.append(distances[i][1])

    return closest_names


# Read drug names from the text file
drug_names_file = "C:/Users/Ghayth Ali/Desktop/Grad_Project/Server/RXReader-server/AIEngine/closest_drug_names.txt"
with open(drug_names_file, 'r') as file:
    drug_names = [line.strip() for line in file]

# Convert drug names to lowercase
drug_names = [name.lower() for name in drug_names]


def replace_false_with_space(input_dict, word):
    modified_word = ''.join(c if flag else ' ' for c, flag in zip(word, input_dict[word]))
    modified_word = word[0] + modified_word[1:]
    return modified_word


def stream_to_multilabel(prob_values):
    str = ""
    tf = []
    for p in prob_values:
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
        str: tf
    }

    for key in input_dict.keys():
        modified_word = replace_false_with_space(input_dict, key)
    modified_word = modified_word.lower()

    print(modified_word)

    erroneous_characters = modified_word
    closest_names = nlp_step(erroneous_characters, drug_names, num_closest=3)
    print(f"The closest drug names to '{erroneous_characters}' are: {closest_names}")
    return closest_names
