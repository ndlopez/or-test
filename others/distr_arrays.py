#!/usr/bin/python.exe
init_arr=[]
for idx in range(100):
    init_arr.append(idx)

#print(init_arr)
prime,remain,even=[],[],[]

def is_prime(num):
    for idx in range(2,num):
        if num % idx == 0:
            #remain.append(num)
            break
    else:
        prime.append(elm)

def is_even(num):
    if num % 2 == 0:
        even.append(num)
    else:
        remain.append(num)

for elm in init_arr:
    if elm > 1 :
        is_prime(elm)
        is_even(elm)
    else:
        remain.append(elm)

print(prime,even,remain)
print(len(prime),len(even),len(remain))
