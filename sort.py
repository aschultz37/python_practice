'''This program sorts arbitrary input information.\n
Input can be taken from the console or a text-based file.
'''

import os
import numpy as np
import pandas as pd

intro_message = ("This program sorts information from the console or \
    a text-based file.\nSelect input option in menu. Q to quit.")
print(intro_message)

class FileExtError(Exception):
    pass

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
    while user_input == '':
        print('Invalid input. Try again:')
        user_input = input()
    print('Enter the delimiter:')
    delimiter = input()
    while delimiter == '':
        print('Invalid input. Try again:')
        user_input = input()
    return (user_input, delimiter)

def extract_file_tup(file_path):
    file_basename = os.path.basename(file_path)
    return os.path.splitext(file_basename)

def file_input():
    print('Please enter the file path:')
    file_path = input()
    #add error check on filepath (includes at least basename and extension)
    print('Enter delimiter to override file-type default:')
    delimiter = input()
    return (file_path, delimiter)

def read_file(file_path, delimiter):
    file_ext = extract_file_tup(file_path)[1]
    try:
        if file_ext == '.csv':
            if(delimiter == ''):
                return pd.read_csv(file_path)
            else:
                return pd.read_csv(file_path, sep=delimiter)
        elif file_ext == '.txt':
            if delimiter == '':
                return pd.read_csv(file_path, delim_whitespace=True)
            else:
                return pd.read_csv(file_path, sep=delimiter)
        else:
            raise FileExtError
    except FileNotFoundError:
        raise FileNotFoundError


input_choice = main_menu()

#main function/controller
while(input_choice != '3'):
    if(input_choice == '1'):
        input_info = console_input()
        #parse and go to sort menu
    elif(input_choice == '2'):
        read_info = file_input()
        #read file, then go to sort menu
        try:
            raw_file = read_file(read_info[0], read_info[1])
        except FileExtError:
            print('Error: File extension not supported.\n')
        except FileNotFoundError:
            print('Error: File not found.\n')
        else:
            pass
    else:
        print('Invalid choice. Try again.')
    input_choice = main_menu()