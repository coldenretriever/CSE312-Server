from util.request import Request


def extract_credentials(request):
    body = request.body
    print(body)

    return []


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
            elif pw[i].isUpper():
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