def hex_to_ascii(input_string):
    bytes_object = bytes.fromhex(input_string)
    ascii_string = bytes_object.decode("ASCII")
    print(ascii_string)
    return ascii_string


def remove_spaces(str):
    i = 0
    c = 0
    word = ""
    words = {}
    while i < len(str):
        # print(input[i])
        if str[i] == " " and str[i + 1] != " " and word != "":
            words.update({c: word})
            word = ""
            c += 1
        elif str[i] != " ":
            word += str[i]
        i += 1
    words.update({c: word})
    return words


"""
test1 = "This is a string"
testing = remove_spaces(test1)

print('{0}'.format(testing))

test = "0x616263"[2:]
hex_to_ascii(test)
"""