"""
Count how many numbers exist between a given range in each row
"""
import time
import numpy as np
import multiprocessing as mp

np.random.RandomState(100)
arr = np.random.randint(0,10,size=[20,5])
data = arr.tolist()
data[:5]

def howmany_within_range(row,min,max):
    count = 0
    for n in row:
        if min <= n <= max:
            count += 1
    
    return count

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count())
    #pool = mp.Pool(processes=3)

    tic = time.time()

    result = [pool.apply(howmany_within_range,args=(row,4,8)) for row in data]

    pool.close()
    toc = time.time()
    print(result[:10],toc-tic)
