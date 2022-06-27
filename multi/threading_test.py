# Python program to illustrate the concept
# of threading
#import threading
from multiprocessing import Pool
from itertools import permutations
import time
  
def print_cube(num):
    """
    function to print cube of given num
    """
    #print("Cube: {}".format(num * num * num))
    return num*num*num
  
def print_square(dat):
    """
    function to print square of given num
    """
    #print("Square: {}".format(num * num),end=", ")
    aux = 0
    for num in dat:
        aux += num
    return aux
    #print("in",dat,"sum",aux)

if __name__ == "__main__":
    # creating thread
    tic = time.time()
    perms = permutations([1,2,3,4,5,6,7,8,9],r=9)
    #for item in perms:
    #    print(item)
    pool = Pool(processes=6)
    idx = 0
    for res in pool.map(print_square,perms):
        #apply print_square to each item in perms
        idx += 1
        print(res)
    toc = time.time()

    """t1 = threading.Thread(target=print_square, args=(10,))
    t2 = threading.Thread(target=print_cube, args=(10,))

    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()

    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()"""
  
    # both threads completely executed
    print("Done!",toc-tic)
