from datetime import date
#import os
#import pandas as pd

def NoKeyError(Exception):
    pass

def MouseDeceasedError(Exception):
    pass

def MouseNotFoundError(Exception):
    pass

#Track the globally unique numbers for mice and cages
global_mouse_number = 0
global_cage_number = 0

class Node:
    '''To implement a tree for tracking lineage.'''
    def __init__(self, mother, father):
        self.mother = mother
        self.father = father

    def pre_order(self):
        pass

    def post_order(self):
        pass

    def print_tree(self):
        pass

class Mouse:
    '''For each mouse, stores globally unqiue number, number in cage, age,\
        genotype, parents, children, and if mouse is alive.'''
    def __init__(self, number, mother_mouse, father_mouse, num_in_cage=0,
                d_o_b=date.today(), genotype=None, living=True):
        self.number = number
        self.lineage = Node(mother_mouse, father_mouse)
        self.num_in_cage = num_in_cage
        self.d_o_b = d_o_b
        self.genotype = genotype
        self.living = living
    
    def list_mouse_info(self):
        return [self.number, self.parents, self.num_in_cage, self.age,
                self.genotype, self.living]

class Cage:
    '''Stores cage number, physical location, and list of mice in cage.'''
    def __init__(self, number, location):
        self.number = number
        self.location = location
        self.mice = {}
    
    def list_mice(self):
        '''Returns a list of all mice in the cage.'''
        return [x[1] for x in self.mice.items()]

    def add_mouse(self, mouse):
        '''Adds a mouse to a cage.'''
        if mouse.number not in self.mice:
            self.mice[mouse.number] = mouse
        else:
            print(f"Error: Mouse {mouse.number} already in cage {self.number}.")

    def remove_mouse(self, mouse=None, key=None):
        '''Removes a mouse from a cage. Mouse specified by object or\
            directly by mouse number. NoKeyError if neither is provided.'''
        if key != None:
            try:
                return self.mice.pop(key)
            except KeyError:
                print(f"Error: Key {key} not found in cage {self.number}.")
        else:
            if mouse != None:
                try:
                    return self.mice.pop(mouse.number)
                except KeyError:
                    print(f"Error: Mouse {mouse.number} not found in cage \
                        {self.number}.")
            else:
                raise NoKeyError

class Colony:
    '''Stores all cages in a colony as a dictionary.'''
    def __init__(self, name, cages={}):
        self.name = name
        self.cages = cages
        self.deceased_mice = {}
    
    def list_cages(self):
        '''Returns a list of all cages in the colony.'''
        return [x[1] for x in self.cages.items()]

    def add_cage(self, cage):
        '''Adds a cage to the colony.'''
        if cage.number not in self.cages:
            self.cages[cage.number] = cage
        else:
            print(f"Error: Cage {cage.number} already in colony {self.name}.")

    def remove_cage(self, cage=None, key=None):
        '''Removes a cage from the colony. Cage specified by object or\
            directly by cage number. NoKeyError if neither is provided.'''
        if key != None:
            try:
                return self.cages.pop(key)
            except KeyError:
                print(f"Error: Key {key} not found in colony {self.name}.")
        else:
            if cage != None:
                try:
                    return self.cages.pop(cage.number)
                except KeyError:
                    print(f"Error: Cage {cage.number} not found in colony \
                        {self.name}.")
            else:
                raise NoKeyError
    
    def move_mouse_helper(self, mouse, new_cage, old_cage):
        '''Checks if new_cage exists in colony and creates it if not.\
            Moves mouse from old_cage to new_cage.'''
        if new_cage in self.cages:
            new_cage.mice[mouse.number] = old_cage.mice.pop(mouse.number)
        else:
            self.cages[new_cage.number] = new_cage
            new_cage.mice[mouse.number] = old_cage.mice.pop(mouse.number)

    def move_mouse(self, mouse, new_cage, old_cage=None):
        '''Moves a mouse from existing cage to a new one.'''
        if old_cage != None:
            if mouse.number in old_cage.mice:
                self.move_mouse_helper(mouse, new_cage, old_cage)
                return True
        else:
            for cage in self.cages:
                if mouse.number in cage.mice:
                    self.move_mouse_helper(mouse, new_cage, cage)
                    return True
        if mouse.number in self.deceased_mice:
            raise MouseDeceasedError
        else:
            raise MouseNotFoundError

    def sac_mouse(self, mouse, cage=None):
        '''Changes mouse living status to False. Removes (pops) mouse from\
            cage and adds it to Colony.deceased_mice.'''
        if cage != None:
            if mouse.number in cage:
                mouse.living = False
                self.deceased_mice[mouse.number] = cage.pop(mouse.number)
                return True
            else:
                if mouse.number in self.deceased_mice:
                    raise MouseDeceasedError
                else:
                    raise MouseNotFoundError
        else:
            for cage_tmp in self.cages:
                if mouse.number in cage_tmp:
                    mouse.living = False
                    self.deceased_mice[mouse.number] = cage_tmp.pop(
                                                            mouse.number)
                    return True
        if mouse.number in self.deceased_mice:
            raise MouseDeceasedError
        else:
            raise MouseNotFoundError

#Master Dict of All Colonies
colonies = {}

def add_colony(name):
    colonies[name] = Colony(name)

def remove_colony(name):
    if name in colonies:
        return colonies.pop(name)
    else:
        print(f"Error: Colony {name} not found.")


def list_colonies():
    return [x[1] for x in colonies.items()]

def import_mice(filename):
    '''Imports mice from a file. Supports multiple formats as long as the\
        header and indices are correct in file.'''
    pass #TODO, use pandas for csv/txt & Excel

def check_deceased(mouse, colony_in=None):
    '''Returns True if mouse is deceased, False if living.'''
    if colony_in == None:
        for colony in colonies:
            if mouse.number in colony.deceased_mice:
                return True
    else:
        if mouse.number in colony_in.deceased_mice:
            return True
    return False

def find_mouse(mouse, colony_in=None, cage_in=None):
    '''Searches for a mouse. Returns tuple of (colony, cage).'''
    if cage_in == None:
        if colony_in == None:
            for colony in colonies:
                for cage in colony.list_cages():
                    if mouse.number in cage.mice:
                        return (colony, cage)
        else:
            for cage in colony_in.list_cages():
                if mouse.number in cage.mice:
                    return (colony_in, cage)
    else:
        if colony_in == None:
            for colony in colonies:
                if cage_in.number in colony.cages:
                    if mouse.number in colony.cages[cage_in.number]:
                        return (colony, cage_in)
        else:
            if cage_in.number in colony_in.cages:
                if mouse.number in colony_in.cages[cage_in.number]:
                    return (colony_in, cage_in)
    if check_deceased(mouse, colony_in) == True:
        raise MouseDeceasedError
    else:
        raise MouseNotFoundError

def find_lineage(mouse):
    '''Returns the lineage of a mouse as the root of a binary tree.'''
    pass #TODO

def switch_colony(mouse, old_colony, new_colony, new_cage_num,
                  old_cage_num=None):
    '''Moves a mouse to a cage in a different colony.'''
    pass #TODO