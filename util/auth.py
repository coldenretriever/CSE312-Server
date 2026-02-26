from util.request import Request


def extract_credentials(request):
    body_bytes = request.body
    body = body_bytes.decode()

    user_side, password_side = body.split("&", 1)
    pre_user, username = user_side.split("=", 1)
    pre_pass, encoded_password = password_side.split("=", 1)
    password = ''
    num_iterations = len(encoded_password)
    i = 0
    while i < num_iterations:
        print("got in")
        if not encoded_password[i] == "%":
            password = password + encoded_password[i]
            i = i + 1
        else:
            num = encoded_password[i+1:i+3]
            char = ''
            if num == '21':
                char = '!'
            elif num == '40':
                char = '@'
            elif num == '23':
                char = '#'
            elif num == '24':
                char = '$'
            elif num == '25':
                char = '%'
            elif num =='5E':
                char = '^'
            elif num == '26':
                char = '&'
            elif num == '28':
                char = '('
            elif num == '29':
                char = ')'
            elif num == '2D':
                char = '-'
            elif num == '5F':
                char = '_'
            elif num == '3D':
                char = '='
            password = password + char
            i = i + 3
    print(body)
    print(username)
    print(password)

    return [username, password]


def validate_password(pw):
    special_list = ['!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '=']
    if len(pw) > 7:
        lower = False
        upper = False
        number = False
        special = False
        invalid = False
        for i in range(len(pw)):
            if pw[i].islower():
                lower = True
            elif pw[i].isupper():
                upper = True
            elif pw[i].isnumeric():
                number = True
            elif pw[i] in special_list:
                special = True
            else:
                invalid = True
        if lower and upper and number and special and not invalid:
            return True
    return False