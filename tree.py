import os
def mul(a,b):
    return a*b
def add(a,b):
    return a+b
def minus(a,b):
    return a-b
def divide(a,b):
    return a/(b+1e-5)

def priorto(x,y):
    # justify whether x is prior to y
    if x in ["*",'/'] and y in ["+","-"]:
        return True
    return False

def exists(name,hashmap):
    list=[]
    for k,v in hashmap.items():
        if name == v['name']:
            list.append(k)
    return list

def cal(hashmap,i):
    x_id=exists('x',hashmap)
    if x_id ==[]:
        print("Rebuild the tree by adding necessary variable!")
        os._exit(0)
    shut=False
    if hashmap[x_id[0]]['data'] == "unassigned":
        print("x is unassigned")
        shut=True
    if shut:
        os._exit(0)
        
    if hashmap[i]['type'] == "const" or hashmap[i]['type'] =="var":
        return hashmap[i]['data']
    else:
        if 2*i+2 in hashmap:
            return hashmap[i]['func'](
                cal(hashmap,2*i+1),cal(hashmap,2*i+2)
                )
        else:
            return hashmap[i]['func'](
                cal(hashmap,2*i+1)
                )

def assign(hashmap,x):
    copyhashmap={k:v.copy() for k,v in hashmap.items()}
    x_id=exists('x',copyhashmap)
    if x_id ==[]:
        print("Rebuild the tree by adding necessary variable!")
        os._exit(0)
    for xi in x_id:
        copyhashmap[xi]['data']=x
    return copyhashmap

def remove_subtree(hashmap,i):
    # remove the subtree which root is in i-place

    remove_list=[]
    new_list=[]
    remove_list.append(i)
    new_list.append(0)
    new_id=0
    for i in remove_list:
        if 2*i+1 in hashmap:
            remove_list.append(2*i+1)
            new_list.append(2*new_list[new_id]+1)
        if 2*i+2 in hashmap:
            remove_list.append(2*i+2)
            new_list.append(2*new_list[new_id]+2)
        new_id+=1
    remove_hashmap={}
    for i in range(len(remove_list)):
        remove_hashmap[new_list[i]]=hashmap[remove_list[i]].copy()
    rest_hashmap={k:v.copy() for k,v in hashmap.items() if k not in remove_list}

    return rest_hashmap,remove_hashmap

def insert_subtree(hashmap,i,insert_hashmap):
    # insert a subtree which root will be  in i-place
    insert_list=[]
    new_list=[]
    insert_list.append(0)
    new_list.append(i)
    new_id=0
    for i in insert_list:
        if 2*i+1 in insert_hashmap:
            insert_list.append(2*i+1)
            new_list.append(2*new_list[new_id]+1)
        if 2*i+2 in insert_hashmap:
            insert_list.append(2*i+2)
            new_list.append(2*new_list[new_id]+2)
        new_id+=1
    for i in range(len(insert_list)):
        hashmap[new_list[i]]=insert_hashmap[insert_list[i]].copy()
    
    return hashmap

def symbolize(hashmap,i):
    x_id=exists('x',hashmap)
    if x_id ==[]:
        print("Rebuild the tree by adding necessary variable!")
        os._exit(0)
    if hashmap[i]['type'] == 'op':
        if hashmap[i]['name']=='cos' or hashmap[i]['name'] =='sin':
            return "{}({})".format(
                hashmap[i]['name'],symbolize(hashmap,2*i+1)
            )
        if priorto(hashmap[i]['name'],hashmap[2*i+1]['name']):
            str="({}){}".format(symbolize(hashmap,2*i+1),hashmap[i]['name'])
        else:
            str="{}{}".format(symbolize(hashmap,2*i+1),hashmap[i]['name'])
        if priorto(hashmap[i]['name'],hashmap[2*i+2]['name']):
            str+="({})".format(symbolize(hashmap,2*i+2))
        else:
            str+="{}".format(symbolize(hashmap,2*i+2))
        return str
    else:
        return hashmap[i]['name']

