import os

def NoKeyError(Exception):
    pass

class Mouse:
    '''For each mouse, stores globally unqiue number, number in cage, age,\
        genotype, parents, children, and if mouse is alive.'''
    def __init__(self, number, parents, cagenumber=0, age=0, genotype='',
                 children=[], living=True):
        self.number = number
        self.parents = parents
        self.cagenumber = cagenumber
        self.age = age
        self.genotype = genotype
        self.children = children
        self.living = living

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

def find_lineage(mouse):
    '''Returns list of mice which is the complete lineage for a mouse.\
        The first element is parent tuple (mother, father). Second element\
         is maternal grandparents tuple, etc.'''
    pass