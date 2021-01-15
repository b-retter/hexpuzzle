import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D

def toint(array,coord):
    return int(array[tuple(coord)])

def pa(array,coords):
    vals = []
    for c in coords:
        vals.append(toint(array,c))
    #print(vals)
    print('    {:2d}  {:2d}  {:2d}    '.format(vals[0],vals[1],vals[2]))
    print('  {:2d}  {:2d}  {:2d}  {:2d}  '.format(vals[3],vals[4],vals[5],vals[6]))
    print('{:2d}  {:2d}  {:2d}  {:2d} {:2d}'.format(vals[7],vals[8],vals[9],vals[10],vals[11]))
    print('  {:2d}  {:2d}  {:2d}  {:2d}  '.format(vals[12],vals[13],vals[14],vals[15]))
    print('    {:2d}  {:2d}  {:2d}    '.format(vals[16],vals[17],vals[18]))
    return vals

def break_check(array):
    #returns true if solution incorrect
    if (np.sum(array,axis=(0,1)) > 38).any() or (np.sum(array,axis=(1,2)) > 38).any() or (np.sum(array,axis=(0,2)) > 38).any():
        return True
    else:
        return False
def solvcheck(array):
    if (np.sum(array,axis=(0,1)) == 38).all() and (np.sum(array,axis=(1,2)) == 38).all() and (np.sum(array,axis=(0,2)) == 38).all():
        return True
    else:
        return False
                                                                                                                    
def solve_values(array,numbers,pindex):
    global loops
    global debug
    #print(numbers)
    numbers=numbers[:]
    loops +=1
    pindex +=1
    coord = tuple(coords[pindex])
    for n in numbers:
        if loops > looplim:
            break                

        #check solution
        if solvcheck(array):
            return array
        array[coord] = n
        ## if any lines sum to greater than 38, return False
        if break_check(array):
            continue
        else:
            nums = numbers[:]
            nums.remove(n)
            if loops > looplim:
                print('hi')
                print(nums)
                break
            array = solve_values(array,nums,pindex)
    if not solvcheck(array):
        if not loops > looplim:
            array[coord] = 0
    return array

x = np.array([0,0,0,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4])
y = np.concatenate([np.arange(3),np.arange(4),np.arange(5),np.arange(1,5),np.arange(2,5)])
z = np.array([2,3,4,1,2,3,4,0,1,2,3,4,0,1,2,3,0,1,2])
coords = np.vstack((x,y,z)).T


        
class board(object):
    #initialise board
    values = range(19,0,-1)
    i = np.array([0,0,0,1,1,1,1,2,2,2,2,2,3,3,3,3,4,4,4])
    j = np.concatenate([np.arange(3),np.arange(4),np.arange(5),np.arange(1,5),np.arange(2,5)])
    k = np.array([2,3,4,1,2,3,4,0,1,2,3,4,0,1,2,3,0,1,2])
    coords = np.vstack((i,j,k)).T
    
    #initialise array
    p_array = np.zeros((5,5,5))
    
    def __init__(self,debug=False,looplim=0):
        self.hexlist = [hex(board.i[n],board.j[n],board.k[n]) for n in range(len(board.i))]
        self.debug = debug
        self.looplim=looplim
        self.loops=0
        self.make_rows()

    def make_rows(self):
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
        array = self.p_array
        vals = []
        for c in self.coords:
            vals.append(toint(array,c))
        #print(vals)
        print('    {:2d}  {:2d}  {:2d}    '.format(vals[0],vals[1],vals[2]))
        print('  {:2d}  {:2d}  {:2d}  {:2d}  '.format(vals[3],vals[4],vals[5],vals[6]))
        print('{:2d}  {:2d}  {:2d}  {:2d} {:2d}'.format(vals[7],vals[8],vals[9],vals[10],vals[11]))
        print('  {:2d}  {:2d}  {:2d}  {:2d}  '.format(vals[12],vals[13],vals[14],vals[15]))
        print('    {:2d}  {:2d}  {:2d}    '.format(vals[16],vals[17],vals[18]))
        
    def solve_check(self):
        array = board.p_array
        if (np.sum(array,axis=(0,1)) == 38).all() and (np.sum(array,axis=(1,2)) == 38).all() and (np.sum(array,axis=(0,2)) == 38).all():
            return True
        else:
            return False
        
    def solve(self,hindex):
        hex1 = self.hexlist[hindex]
        valtest = hex1.get_values(self)
        #print(valtest)
        if valtest is False:
            return False
        numbers = hex1.vals
        for n in numbers:
            #print('{}:{}'.format(hindex,n))

            if self.loops > self.looplim:
                return True
            hextest = hex1.set_value(n,self)
            self.loops +=1
            #if puzzle is solved stop working
            if self.solve_check():
                return True
            hextest = self.solve(hindex+1)
            if hextest is False:
                hex1.reset(self)
            #if puzzle is solved stop working
            if self.solve_check():
                return True
            if self.loops > self.looplim:
                return True
            #hex1.reset()
        return False
            
    def set_hex(self,hex,num):
        hex = self.hexlist[index].set_value(num)
        hex.set_value(num)

class line(board):
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
        #checks if line is almost full
        if np.sum(np.array(self.values) == 0) == 1:
            self.full=True
            return True
        else:
            self.full=False
            return False
        
class hex(board):
    def __init__(self,i,j,k):
        self.i = i
        self.j = j
        self.k = k
        self.val=0
    #def breakcheck(self):
    #    if np.sum(np.sum(p_array[self.i]),38-np.sum(p_array[self.j]),38-np.sum(p_array[self.k]))
    #    return None
    def vals(self):
        print(self.values)
    def pop_val(self,val):
        board.values.remove(val)
    def add_val(self,val):
        board.values.append(val)
    def get_values(self,b):
        initial = board.values[:]
        p_array = board.p_array

        #find largest number
        biggest = []
        if b.rows[self.i].isfull():
            biggest.append(38-b.rows[self.i].sum)
        if b.fcols[self.j].isfull():
            biggest.append(38-b.fcols[self.j].sum)
        if b.bcols[self.k].isfull():
            biggest.append(38-b.bcols[self.k].sum)
        if len(set(biggest)) > 1:
            return False
        elif len(set(biggest)) == 1:
            #print(biggest)
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
        self.val = num
        self.pop_val(num)
        self.update(board)
        board.p_array[self.i,self.j,self.k] = num
        
    def update(self,board):
        board.rows[self.i].update()
        board.fcols[self.j].update()
        board.bcols[self.k].update()
        
    def reset(self,board):
        self.add_val(self.val)
        self.val = 0
        self.update(board)
        board.p_array[self.i,self.j,self.k] = 0
        

b = board(True,130000)
a = b.hexlist
c = a[0]
c.get_values(b)

b.solve(0)
b.pa()