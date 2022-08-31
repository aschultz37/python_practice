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
    print('Select Input:')
    print('1. Console')
    print('2. File')
    print('3. Quit')
    while choice not in ['1', '2', '3']:
        choice = input()
    return choice

def sort_menu():
    choice = '0'
    print('Select Sort:')
    print('1. Main Menu/New Input')
    print('2. Output to Console')
    print('3. Output to File')
    print('4. Ascending')
    print('5. Descending')
    while choice not in ['1', '2', '3', '4', '5']:
        choice = input()
    return choice

def console_input():
    print('Please input text to be sorted:')
    user_input = input()
    while user_input == '':
        print('Invalid input. Try again:')
        user_input = input()
    print('Enter the delimiter (default: space):')
    delimiter = input()
    if delimiter == '':
        delimiter = ' '
    return (user_input, delimiter)

def parse_input(user_input, delimiter):
    '''Return pd.DataFrame from string user_input split by delimiter.'''
    parsed_strings = user_input.split(delimiter)
    parsed_dict = {x: parsed_strings[x] for x in range(0, len(parsed_strings))}
    return pd.DataFrame(data=parsed_dict, index=[0])

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
                return pd.read_csv(file_path, header=None)
            else:
                return pd.read_csv(file_path, sep=delimiter, header=None)
        elif file_ext == '.txt':
            if delimiter == '':
                return pd.read_csv(file_path, delim_whitespace=True,
                                   header=None)
            else:
                return pd.read_csv(file_path, sep=delimiter, header=None)
        else:
            raise FileExtError
    except FileNotFoundError:
        raise FileNotFoundError

def output_dataframe(df):
    written = False
    while written == False:
        file_path = ''
        while file_path == '':
            print('Enter the output file path:')
            file_path = input()
        #todo add option to override default delimiter
        file_tup = extract_file_tup(file_path)
        file_ext = file_tup[1]
        if file_ext == '.csv':
            df.to_csv(file_path, header=False, index=False)
            written = True
        elif file_ext == '.txt':
            df.to_csv(file_path, header=False, index=False, sep=' ')
            written = True
        else:
            raise FileExtError        

def do_sort(df, option):
    axis_in = ''
    if option in ['4', '5']:
        print('Sort within: 1. Row; or 2. Column?')
        while axis_in not in ['1', '2']:
            axis_in = input()      
    if option == '2':
        print(df)
    elif option == '3':
        try:
            output_dataframe(df)
        except FileExtError:
            print('Error: File extension not supported.')
    elif option == '4':
        if axis_in == '1':
            df.sort_values(by=list(df.index), axis='columns', 
                                ascending=True, inplace=True, kind='quicksort')
        else:
            df.sort_values(by=list(df.columns), axis='index', 
                                ascending=True, inplace=True, kind='quicksort')
    elif option == '5':
        if axis_in == '1':
            df.sort_values(by=list(df.index), axis='columns', 
                                ascending=False, inplace=True, kind='quicksort')
        else:
            df.sort_values(by=list(df.columns), axis='index',
                                ascending=False, inplace=True, kind='quicksort')
    else:
        print('Error: Invalid sort selection.')

#initial menu choice to start the main loop
input_choice = main_menu()

#main function/controller
while input_choice != '3':
    if input_choice == '1':
        input_info = console_input()
        console_dataframe = parse_input(input_info[0], input_info[1])
        sort_choice = '0'
        while sort_choice != '1':
            sort_choice = sort_menu()
            if sort_choice != '1':
                do_sort(console_dataframe, sort_choice)
    elif input_choice == '2':
        read_info = file_input()
        try:
            file_dataframe = read_file(read_info[0], read_info[1])
        except FileExtError:
            print('Error: File extension not supported.\n')
        except FileNotFoundError:
            print('Error: File not found.\n')
        else:
            sort_choice = '0'
            while sort_choice != '1':
                sort_choice = sort_menu()
                if sort_choice != '1':
                    do_sort(file_dataframe, sort_choice)
    else:
        print('Invalid choice. Try again.')
    input_choice = main_menu()