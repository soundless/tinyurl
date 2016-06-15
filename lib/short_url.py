#!/usr/bin/env python
# -*- utf-8 -*-
#
# Converts any interger to a base[BASE] number.
# Base as 62 to represent using all of alphanumeric characters.
# [no space characters] = {0..9}, {B..Z}, {b..z}.
# encode(): take an integer and turns it into the base 51 string.
# decode(): take the base 62 key as a string, turns it back into an integer.
#

ALPHABET='23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ-_'
LENGTH = 6
BASE = len(ALPHABET)

class ShortUrl(object):
    @staticmethod
    def encode(num):
        if ( type(num) is not int ) or num <= 0:
            raise Exception("invalid num input")
        url = ""
        while num > 0:
            char = ALPHABET[num % BASE]
            url = char + url
            num = num // BASE
        if len(url) < LENGTH:
            url = '0' * (LENGTH - len(url)) + url
        return url

    @staticmethod
    def decode(url):
        if not url:
            raise Exception("invalid url input")
        num = 0
        for char in url:
            if char not in ALPHABET:
                continue
            num = num * BASE + ALPHABET.index(char)
        return num

# local tests
if __name__ == '__main__':
    su = ShortUrl() 
    print su.encode(1) == '000003'
    print su.decode('3') == 1
    print su.encode(125) == '00004v'
    print su.decode("4v") == 125
    print su.encode(28976) == '000f9b'
    print su.decode('f9b') == 28976
