def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    dig, upp, low = False, False, False
    for char in password:
        if char.isdigit():
            dig = True
        if char.isupper():
            upp = True
        if char.islower():
            low = True
    if dig and upp and low:
        return password
    raise ValueError("Password must contain: digit, lower and uppercase")


print(validate_password("hej123123"))