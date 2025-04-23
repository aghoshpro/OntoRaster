from numba import jit, cuda
import numpy as np 
from tqdm import tqdm
from timeit import default_timer as timer    
  
# normal function to run on cpu 
def func(a, n):                                 
    for i in tqdm(range(n)): 
        a[i]+= 1      
  
## function optimized to run on gpu  (# @jit(nopython=True)  and @cuda.jit)
@jit
def func2(a, n): 
    for i in range(n): 
        a[i]+= 1


if __name__=="__main__": 
    n = 1000000000 # numpy.core._exceptions._ArrayMemoryError: Unable to allocate 74.5 GiB for an array with shape (10000000000,) OR 10^8 and data type float64
    a = np.ones(n, dtype = np.float64) 
      
    start = timer() 
    func(a, n) 
    print("\n CPU :", timer()-start,"\n")     
      
    start = timer() 
    func2(a, n) 
    print(" GPU :", timer()-start,"\n") 


    ### https://medium.com/@nickshpilevoy/python-numba-and-jit-compilation-b074dc7ccb53