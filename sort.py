'''This program sorts arbitrary input information.\n
Input can be taken from the console or a text-based file.
'''

import os
import numpy as np
import pandas as pd

intro_message = ("This program sorts information from the console or \
    a text-based file.\nSelect input option in menu. Q to quit.")
print(intro_message)

def main_menu():
    choice = '0'
    while choice not in ['1', '2', '3']:
        print('Select Input:')
        print('1. Console')
        print('2. File')
        print('3. Quit')
        choice = input()
    return choice

def console_input():
    print('Please input text to be sorted:')
    user_input = input()
    print('Enter the delimiter for each item:')
    delimiter = input()

def extract_file_tup(file_path):
    file_basename = os.path.basename(file_path)
    return os.path.splitext(file_basename)

def default_delimiter(file_path):
    file_tup = extract_file_tup(file_path)
    file_ext = file_tup[1]
    if file_ext in ['.csv', '.xls', '.xlsx']:
        return ','
    elif file_ext in ['.txt', '.doc', '.docx']:
        return ' '
    else:
        print('Default could not be resolved. Enter delimiter:')
        return input()

def file_input():
    print('Please enter the file path:')
    filepath = input()
    #add error check on filepath (includes at least basename and extension)
    print('Enter delimiter to override file-type default:')
    delimiter = input()
    if delimiter == '':
        delimiter = default_delimiter()
    #add error check on delimiter (non-null)

input_choice = main_menu()

#main function/controller
while(input_choice != '3'):
    if(input_choice == '1'):
        console_input()
    elif(input_choice == '2'):
        file_input()
    else:
        print('Invalid choice. Try again.')
    input_choice = main_menu()