"""
Code for solving a hexagonal puzzle.
Puzzle pieces are labelled with the numbers from 1 to 19 and need to fit into 
a hexagonal grid such that every line adds up to 38. 
"""

import numpy as np

class board(object):
    
    ##initialise board class
    #each hex on the board has 3 coordinates relating to the horizontal-row,
    #backwards-diagonal column and forwards-diagonal column.
    
    values = range(19,0,-1)
    i = np.array([0,0,0,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4])
    j = np.concatenate([np.arange(3),np.arange(4),np.arange(5),np.arange(1,5),np.arange(2,5)])
    k = np.array([2,3,4,1,2,3,4,0,1,2,3,4,0,1,2,3,0,1,2])
    coords = np.vstack((i,j,k)).T
    
    #initialise 3d-array to contain board values.
    #since each hex is associated with 3 coords they can be placed in a 3d
    #array. This allows for quick summation over axes to determine if
    #solution has been found.
    
    p_array = np.zeros((5,5,5))
    
    def __init__(self,debug=False,looplim=0):
        """
        Set up board with list of hexes.
        """
        
        self.hexlist = [hex(board.i[n],board.j[n],board.k[n]) for n in range(len(board.i))]
        self.debug = debug
        self.looplim=looplim
        self.loops=0
        self.make_rows()

    def make_rows(self):
        """
        Make lists of hexes associated with each row, forward column and
        backward column.
        """
        
        self.rows = []
        self.fcols = []
        self.bcols = []
        for x in range(5):
            row = []
            fcol = []
            bcol = []
            for n in range(19):
                if self.hexlist[n].i == x:
                    row.append(self.hexlist[n])
                if self.hexlist[n].j == x:
                    fcol.append(self.hexlist[n])
                if self.hexlist[n].k == x:
                    bcol.append(self.hexlist[n])
                    
            self.rows.append(line(row))
            self.fcols.append(line(fcol))
            self.bcols.append(line(bcol))

    def pa(self):
        """
        Prints array in hex-like representation
        """
        
        array = self.p_array
        vals = []
        for c in self.coords:
            vals.append(toint(array,c))

        print('    {:2d}  {:2d}  {:2d}    '.format(vals[0],vals[1],vals[2]))
        print('  {:2d}  {:2d}  {:2d}  {:2d}  '.format(vals[3],vals[4],vals[5],vals[6]))
        print('{:2d}  {:2d}  {:2d}  {:2d} {:2d}'.format(vals[7],vals[8],vals[9],vals[10],vals[11]))
        print('  {:2d}  {:2d}  {:2d}  {:2d}  '.format(vals[12],vals[13],vals[14],vals[15]))
        print('    {:2d}  {:2d}  {:2d}    '.format(vals[16],vals[17],vals[18]))
        
    def solve_check(self):
        """
        Checks if solution has been found by summing over every set of two axes.
        If every element of every 1d array is equal to 38 then solution has
        been found.
        """
        
        array = self.p_array
        if (np.sum(array,axis=(0,1)) == 38).all() and (np.sum(array,axis=(1,2)) == 38).all() and (np.sum(array,axis=(0,2)) == 38).all():
            return True
        else:
            return False
        
    def solve(self,hindex):
        """
        Recursively sets hexes to each available value to find solution.
        """
        
        hex1 = self.hexlist[hindex]
        valtest = hex1.get_values(self)

        if valtest is False:
            return False
        numbers = hex1.vals

        #Loop over the possible numbers a hex can be
        for n in numbers:

            if self.loops > self.looplim:
                return True
            hextest = hex1.set_value(n,self)
            self.loops +=1
            
            #if puzzle is solved stop working
            if self.solve_check():
                return True

            #move to next hex
            hextest = self.solve(hindex+1)
            
            if hextest is False:
                hex1.reset(self)
                
            #if puzzle is solved stop working
            if self.solve_check():
                return True
            if self.loops > self.looplim:
                return True

        return False
            
class line(board):
    """
    A collection of hexes in a straight line make up a line.
    The line class allows for hexes to determine which possible values they can
    be.
    """
    
    def __init__(self,hexlist):
        self.hexlist = hexlist
        self.update()
        self.get_sum()
        self.isfull()
        
    def update(self):
        self.values = []
        for h in self.hexlist:
            self.values.append(h.val)
        self.get_sum()
        self.isfull()
            
    def get_sum(self):
        self.sum = sum(self.values)
        return self.sum
    
    def isfull(self):
        """
        checks if line is one hex from being full
        i.e. if there is one zero-value hex in line.
        """
        
        if np.sum(np.array(self.values) == 0) == 1:
            self.full=True
            return True
        else:
            self.full=False
            return False
        
class hex(board):
    """
    The available spaces on the board are objects from the hex class.
    A hex can find its possible values and add and remove values from itself 
    and the board.
    """
    
    def __init__(self,i,j,k):
        self.i = i
        self.j = j
        self.k = k
        self.val=0
      
    def pop_val(self,val):
        #Remove the hex value from list of possible values
        board.values.remove(val)
        
    def add_val(self,val):
        #Appends the hex value to list of possible hex values
        board.values.append(val)
        
    def get_values(self,b):
        initial = board.values[:]
        p_array = board.p_array

        #Look if there are any lines that are one hex from being full and
        #find what value is required to add up to 38.
        
        biggest = []
        if b.rows[self.i].isfull():
            biggest.append(38-b.rows[self.i].sum)
        if b.fcols[self.j].isfull():
            biggest.append(38-b.fcols[self.j].sum)
        if b.bcols[self.k].isfull():
            biggest.append(38-b.bcols[self.k].sum)
        if len(set(biggest)) > 1:
            #If more than one value is required to fill lines, then current 
            #solution is wrong.
            return False
        
        elif len(set(biggest)) == 1:

            #Find if value is available from the board
            tests = list(set(biggest)&set(initial))
            if len(tests) == 0:
                return False
            else:
                self.vals = tests
                return True
        
        #find smallest number
        smallest = int(min(38-np.sum(p_array[self.i,:,:]),38-np.sum(p_array[:,self.j,:]),38-np.sum(p_array[:,:,self.k])))
        if smallest < 1:
            return False
        else:
            self.vals = list(set(range(smallest,0,-1))&set(initial))
            return True
        
    def set_value(self,num,board):
        """
        Set hex value and update board.
        """
        
        self.val = num
        self.pop_val(num)
        self.update(board)
        board.p_array[self.i,self.j,self.k] = num
        
    def update(self,board):
        """
        Update rows with current value.
        """
        board.rows[self.i].update()
        board.fcols[self.j].update()
        board.bcols[self.k].update()
        
    def reset(self,board):
        """
        Return current hex value to pool and set current hex value to zero. 
        """
        
        self.add_val(self.val)
        self.val = 0
        self.update(board)
        board.p_array[self.i,self.j,self.k] = 0
        

def toint(array,coord):
    """
    Return integer at coordinate in array
    """
    return int(array[tuple(coord)])
     


b = board(True,130000)
b.solve(0)
b.pa()
