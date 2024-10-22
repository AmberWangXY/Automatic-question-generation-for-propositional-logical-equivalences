import re
import hashlib


def hash_id():
    number = input("Please enter student ID number: ")
    pattern = r'^\d{10}$'
    match = re.match(pattern, number)
    if not match:
        print("Invalid student ID number, please try again!")
        hash_id()
    number = number.encode('utf-8')
    m = hashlib.md5()
    m.update(number)
    m.hexdigest()
    return m.hexdigest()


number = hash_id()
