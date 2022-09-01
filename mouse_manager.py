#import os
#import pandas as pd

def NoKeyError(Exception):
    pass

def MouseNotFound(Exception):
    pass

class Mouse:
    '''For each mouse, stores globally unqiue number, number in cage, age,\
        genotype, parents, children, and if mouse is alive.'''
    def __init__(self, number, parents, num_in_cage=0, age=0, genotype='',
                 children=[], living=True):
        self.number = number
        self.parents = parents
        self.num_in_cage = num_in_cage
        self.age = age
        self.genotype = genotype
        self.children = children
        self.living = living
    
    def list_mouse_info(self):
        return [self.number, self.parents, self.num_in_cage, self.age,
                self.genotype, self.children, self.living]

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
            print("Error: Mouse already in cage.")

    def remove_mouse(self, mouse=None, key=''):
        '''Removes a mouse from a cage. Mouse specified by object or\
            directly by mouse number. NoKeyError if neither is provided.'''
        if key != '':
            try:
                return self.mice.pop(key)
            except KeyError:
                print("Error: Key not found in cage.")
        else:
            if mouse != None:
                try:
                    return self.mice.pop(mouse.number)
                except KeyError:
                    print("Error: Mouse not found in cage.")
            else:
                raise NoKeyError

class Colony:
    '''Stores all cages in a colony as a dictionary.'''
    def __init__(self, cages={}):
        self.cages = cages
        self.deceased_mice = {}
    
    def list_cages(self):
        '''Returns a list of call cages in the colony.'''
        return [x[1] for x in self.cages.items()]

    def add_cage(self, cage):
        '''Adds a cage to the colony.'''
        if cage.number not in self.cages:
            self.cages[cage.number] = cage
        else:
            print("Error: Cage already in colony.")

    def remove_cage(self, cage=None, key=''):
        '''Removes a cage from the colony. Cage specified by object or\
            directly by cage number. NoKeyError if neither is provided.'''
        if key != '':
            try:
                return self.cages.pop(key)
            except KeyError:
                print("Error: Key not found in colony.")
        else:
            if cage != None:
                try:
                    return self.cages.pop(cage.number)
                except KeyError:
                    print("Error: Cage not found in colony.")
            else:
                raise NoKeyError
    
    def move_mouse(self, mouse, new_cage, old_cage=None):
        '''Moves a mouse from existing cage to a new one.'''
        #If old_cage is provided, check that mouse is in the cage
        #If old_cage is not provided, find it by searching for mouse
        #Check if new_cage exists; if not, make new_cage
        #Remove mouse from old cage (popped from dict)
        #Add mouse to new cage (from return of remove statement)
        pass #TODO

    def sac_mouse(self, mouse, cage=None, cage_num=None):
        '''Changes mouse living status to False. Removes (pops) mouse from\
            cage and adds it to Colony.deceased_mice.'''
        pass #TODO

#Master Dict of All Colonies
colonies = {}

def list_colonies():
    return [x[1] for x in colonies.items()]

def import_mice(filename):
    '''Imports mice from a file. Supports multiple formats as long as the\
        header and indices are correct in file.'''
    pass #TODO

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
    raise MouseNotFound

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

def find_lineage(mouse):
    '''Returns list of mice which is the complete lineage for a mouse.\
        The first element is parent tuple (mother, father). Second element\
         is maternal grandparents tuple, etc.'''
    pass #TODO

def switch_colony(mouse, old_colony, new_colony, new_cage_num,
                  old_cage_num=None):
    '''Moves a mouse to a cage in a different colony.'''
    pass #TODO