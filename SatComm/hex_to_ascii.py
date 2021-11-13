def hex_to_ascii(input_string):
    bytes_object = bytes.fromhex(input_string)
    ascii_string = bytes_object.decode("ASCII")
    print(ascii_string)
    return ascii_string


def remove_spaces(str):
    i = 1
    c = 0
    word = ""
    words = {}
    gps = False
    while i < len(str):
        # print(str[i])
        if str[i-1] == "(":
            gps = True
        if str[i-1] == " " and str[i] != " " and word != "" and not gps:
            words.update({c: word})
            word = ""
            c += 1
        elif str[i-1] != " ":
            word += str[i-1]
        i += 1
    words.update({c: word})
    return words



# test1 = "This is a string"
# testing = remove_spaces(test1)
#
# print('{0}'.format(testing))

# test = "0x524230303132383238202032312e313320202032322e373520203933342e303420203638312e3633202834362e3733332c202d3131372e3030352920"[2:]
# hex_to_ascii(test)
# print('{0}'.format(remove_spaces(hex_to_ascii(test))))