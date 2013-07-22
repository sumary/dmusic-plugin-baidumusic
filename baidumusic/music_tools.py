#! /usr/bin/env python
# -*- coding: utf-8 -*-

def encode_utf8(chars):    
    if isinstance(chars, basestring):
        if isinstance(chars, unicode):
            return chars.encode("utf-8")
        return chars
    return str(chars)
