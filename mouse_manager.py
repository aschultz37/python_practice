"""Mouse Management Program
*TODO*: Update code to utilize mouse_in_cage, mouse_in_colony,
        cage_in_colony, etc. to make easier to read.
        Also update to use Cage.list_mice(), Colony.list_cages(), etc.
"""

from calendar import monthrange
from datetime import date
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
#import os
#import numpy as np
#import pandas as pd

def NoKeyError(Exception):
    pass

def MouseDeceasedError(Exception):
    pass

def MouseNotFoundError(Exception):
    pass

def CageNotEmptyError(Exception):
    pass

def CageNotFoundError(Exception):
    pass

def ColonyNotEmptyError(Exception):
    pass

#Track the globally unique numbers for mice and cages
global_mouse_number = 0
global_cage_number = 0

class Mouse:
    '''For each mouse, stores globally unqiue number, number in cage, age,
        genotype, parents, children, and if mouse is alive.'''
    def __init__(self, mother, father, lineage: Node=None, 
                num_in_cage: int=None, d_o_b: date=date.today(), genotype=None,
                living=True):
        '''WARN: mother and father MUST be of type Mouse.'''
        global global_mouse_number
        self.number = global_mouse_number
        self.mother = mother
        self.father = father
        self.lineage = lineage
        self.num_in_cage = num_in_cage
        self.d_o_b = d_o_b
        self.genotype = genotype
        self.living = living
        global_mouse_number = global_mouse_number + 1
    
    def list_mouse_info(self):
        '''Returns a list containing all data in Mouse object.'''
        return [self.number, self.lineage, self.num_in_cage, self.d_o_b,
                self.genotype, self.living]

class Cage:
    '''Stores cage number, physical location, and list of mice in cage.'''
    def __init__(self, location: str):
        global global_cage_number
        self.number = global_cage_number
        self.location = location
        self.mice = {}
        global_cage_number = global_cage_number + 1
    
    def mouse_in_cage(self, mouse: Mouse):
        '''Checks if a mouse is in cage.'''
        if mouse.number in self.mice:
            return True
        else:
            return False

    def list_mice(self):
        '''Returns a list of all mice in the cage.'''
        return [x[1] for x in self.mice.items()]

    def add_mouse(self, mouse: Mouse):
        '''Adds a mouse to a cage.'''
        if mouse.number not in self.mice:
            self.mice[mouse.number] = mouse
        else:
            print(f"Error: Mouse {mouse.number} already in cage {self.number}.")

    def remove_mouse(self, mouse: Mouse=None, key: int=None):
        '''Removes a mouse from a cage. Mouse specified by object or
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
    '''Stores all cages in a colony as a dictionary. Tracks deceased mice and
     inactive cages as dictionaries.'''
    def __init__(self, name: str, cages: dict=None):
        self.name = name
        self.cages = cages
        self.deceased_mice = {}
        self.inactive_cages = {}
    
    def mouse_in_colony(self, mouse: Mouse):
        '''Checks if a mouse is in colony (in any cage).'''
        for cage in self.cages.items():
            if cage.mouse_in_cage(mouse) == True:
                return True
        return False

    def cage_in_colony(self, cage: Cage):
        '''Checks if a cage is in colony.'''
        if cage.number in self.cages:
            return True
        else:
            return False

    def list_active_cages(self):
        '''Returns a list of all active cages in the colony.'''
        return [x[1] for x in self.cages.items()]

    def list_inactive_cages(self):
        '''Returns a list of all inactive cages in the colony.'''
        return [x[1] for x in self.inactive_cages.items()]

    def list_all_cages(self):
        '''Returns a dictionary of all cages formatted as
        {'active': [], 'inactive': []}.'''
        return {'active': self.list_active_cages(), 
                'inactive': self.list_inactive_cages()}
    
    def list_living_mice(self):
        '''Returns a list of all living mice in the colony.'''
        return [mouse[1] for cage in self.cages.items() 
                for mouse in cage[1].mice.items()]
    
    def list_deceased_mice(self):
        '''Returns a list of all deceased mice in the colony.'''
        return [mouse[1] for cage in self.cages.items() 
                for mouse in cage[1].mice.items()]

    def list_all_mice(self):
        '''Returns a dictionary of all mice formatted as
        {'living': [], 'deceased': []}.'''
        return {'living': self.list_living_mice(), 
                'deceased': self.list_deceased_mice()}

    def add_cage(self, cage: Cage):
        '''Adds a cage to the colony.'''
        if cage.number not in self.cages:
            self.cages[cage.number] = cage
        else:
            print(f"Error: Cage {cage.number} already in colony {self.name}.")

    def remove_cage(self, cage: Cage=None, key: int=None):
        '''Removes a cage from the colony. Cage specified by object or
            directly by cage number. NoKeyError if neither is provided.'''
        if key != None:
            try:
                if len(self.cages[key].mice) != 0:
                    raise CageNotEmptyError
                else:
                    return self.cages.pop(key)
            except KeyError:
                print(f"Error: Key {key} not found in colony {self.name}.")
        else:
            if cage != None:
                try:
                    if len(self.cages[cage.number].mice) != 0:
                        raise CageNotEmptyError
                    else:
                        return self.cages.pop(cage.number)
                except KeyError:
                    print(f"Error: Cage {cage.number} not found in colony \
                        {self.name}.")
            else:
                raise NoKeyError
    
    def move_mouse_helper(self, mouse: Mouse, new_cage: Cage, old_cage: Cage):
        '''Checks if new_cage exists in colony and creates it if not.
            Moves mouse from old_cage to new_cage.'''
        if new_cage in self.cages:
            new_cage.mice[mouse.number] = old_cage.mice.pop(mouse.number)
        else:
            self.cages[new_cage.number] = new_cage
            new_cage.mice[mouse.number] = old_cage.mice.pop(mouse.number)

    def move_mouse(self, mouse: Mouse, new_cage: Cage, old_cage: Cage=None):
        '''Moves a mouse from existing cage to a new one.'''
        if old_cage != None:
            if mouse.number in old_cage.mice:
                self.move_mouse_helper(mouse, new_cage, old_cage)
                return True
        else:
            for cage in self.cages.items():
                if mouse.number in cage[1].mice:
                    self.move_mouse_helper(mouse, new_cage, cage[1])
                    return True
        if mouse.number in self.deceased_mice:
            raise MouseDeceasedError
        else:
            raise MouseNotFoundError

    def sac_mouse(self, mouse: Mouse, cage: Cage=None):
        '''Changes mouse living status to False. Removes (pops) mouse from
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
            for cage_tmp in self.cages.items():
                if mouse.number in cage_tmp[1]:
                    mouse.living = False
                    self.deceased_mice[mouse.number] = cage_tmp[1].pop(
                                                            mouse.number)
                    return True
        if mouse.number in self.deceased_mice:
            raise MouseDeceasedError
        else:
            raise MouseNotFoundError

    def sac_cage(self, cage: Cage):
        '''For all mice in a cage, changes mouse living status to False.
         Removes cage from Colony.cages.'''
        if cage.number in self.cages.items():
            for mouse in cage[1]:
                self.sac_mouse(mouse, cage[1])
            self.cages.pop(cage.number)
        else:
            raise CageNotFoundError


#Master Dict of All Colonies
colonies = {}

def add_colony(name: str):
    if name not in colonies:
        colonies[name] = Colony(name)
    else:
        print(f"Error: Colony {name} already exists.")

def remove_colony(name: str):
    if name in colonies:
        if len(colonies[name].list_living_mice()) != 0:
            raise ColonyNotEmptyError
        return colonies.pop(name)
    else:
        print(f"Error: Colony {name} not found.")


def list_colonies():
    return [x[1] for x in colonies.items()]

def import_mice(filename: str):
    '''Imports mice from a file. Supports multiple formats as long as the
        header and indices are correct in file.'''
    pass #TODO, use pandas for csv/txt & Excel

def check_deceased(mouse, colony_in: Colony=None):
    '''Returns True if mouse is deceased, False if living.'''
    if colony_in == None:
        for colony in colonies.items():
            if mouse.number in colony[1].deceased_mice:
                return True
    else:
        if mouse.number in colony_in.deceased_mice:
            return True
    return False

def find_mouse(mouse: Mouse, colony_in: Colony=None, cage_in: Cage=None):
    '''Searches for a mouse. Returns tuple of (colony, cage).'''
    if cage_in == None: #TODO UPDATE with list_x_cages, mouse_in_x, cage_in_x
        if colony_in == None:
            for colony in colonies.items():
                for cage in colony[1].list_cages(): #here
                    if cage.mouse_in_cage(mouse) == True: #here
                        return (colony, cage)
        else:
            for cage in colony_in.list_cages(): #here
                if cage.mouse_in_cage(mouse) == True: #here
                    return (colony_in, cage)
    else:
        if colony_in == None:
            for colony in colonies.items(): #here
                if cage_in.number in colony[1].cages: #here & \/
                    if mouse.number in colony[1].cages[cage_in.number].mice:
                        return (colony, cage_in)
        else:
            if cage_in.number in colony_in.cages: #here & \/
                if mouse.number in colony_in.cages[cage_in.number].mice: 
                    return (colony_in, cage_in)
    if check_deceased(mouse, colony_in) == True:
        raise MouseDeceasedError
    else:
        raise MouseNotFoundError

def generate_lineage(mouse: Mouse, prev_node: Node=None):
    '''Returns the lineage of a mouse as the root of a tree.'''
    #TODO read through this again; start at mouse as root node
    root = Node({'mother': mouse.mother, 'father': mouse.father}, prev_node)
    if mouse.mother != None:
        generate_lineage(mouse.mother, root)
    if mouse.father != None:
        generate_lineage(mouse.father, root)
    return root


def switch_colony(mouse: Mouse, old_colony: Colony, new_colony: Colony,
                  new_cage_num: int, old_cage_num: int=None):
    '''Moves a mouse to a cage in a different colony.'''
    pass #TODO