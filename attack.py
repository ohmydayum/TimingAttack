#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import time
import timeit

MAX_USERNAME_LENGTH = 3
MAX_PASSWORD_LENGTH = 3
ALLOWED_CHARACTERS = "0123456789"


USERS = {"156": "486",
         "481": "123",
         "181": "001"}

def validate(username, password):
    if username not in USERS:
        return False

    real_password = USERS[username]
    if len(real_password) != len(password):
        return False

    for index in range(len(real_password)):
        if real_password[index] != password[index]:
            return False
    return True


def validate_wrapper(username, password):
    return lambda: validate(username, password)


def find_maximum_validator(validators, number):
    timings = []
    for validator in validators:
        timings.append(timeit.timeit(validator, number=number))
    return timings.index(max(timings))


def sub_strings(max_length, characters):
    if max_length < 1:
        return [""]

    shorter_substrings = sub_strings(max_length - 1, characters)
    total_substrings = shorter_substrings[:]
    for c in characters:
        for shorter_substring in shorter_substrings:
            total_substrings.append(c + shorter_substring)
    return list(set(total_substrings))


def find_username():
    usernames = sub_strings(MAX_USERNAME_LENGTH, ALLOWED_CHARACTERS)
    validators = [validate_wrapper(username, '') for username in usernames]
    return usernames[find_maximum_validator(validators, 100000)]


def find_password_length(username):
    validators = [validate_wrapper(username, ' '*n) for n in range(MAX_PASSWORD_LENGTH)]
    return find_maximum_validator(validators, 1000000000)


def find_password_next_character(username, prefix, total_length):
    validators = [validate_wrapper(username, prefix + c + ' '*(total_length-1)) for c in ALLOWED_CHARACTERS]
    character_index = find_maximum_validator(validators, 1000000)
    return ALLOWED_CHARACTERS[character_index]


def find_password(username, password_length):
    current_password = ''
    while len(current_password) < password_length:
        c = find_password_next_character(username, current_password, password_length - len(current_password))
        print c
        current_password += c
    return current_password


if __name__ == "__main__":
    print "Finding username..."
    username = find_username()
    print "Username found is: " + username
    print

    print "Finding password length..."
    length = find_password_length(username)
    print "Password length is: " + str(length)
    print

    print "Finding password characters..."
    password = find_password(username, length)
    print "Password is: " + password
    print

    print "(" + username + ", " + password + ") ? " + str(validate(username, password))
