#!/usr/bin/python

import argparse

def test(req,*reqtest):
    if reqtest:
        print(f"LOOOOL: {reqtest}")
    else:
        print(req)

parser = argparse.ArgumentParser(description="Testing stuff.")
parser.add_argument("--debug", action="store_true", help="Debug")
args = parser.parse_args()
if args.debug:
    test("lol","debug")
else:
    test("lolok")