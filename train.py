from xxlimited import new
from numpy import partition
from tree import add, exists,mul,minus,remove_subtree,insert_subtree,cal,assign,symbolize
from generator import Generator
import random
import json
from tqdm import tqdm
def fitness(hashmap,datapoints):
    total_loss=0.0
    for item in datapoints:
        new_hashmap=assign(hashmap,item['x'])
        total_loss+=(cal(new_hashmap,0)-item['y'])**2
    return total_loss/len(datapoints)

def select(datasets,fitnesses):
    new_fitness=sorted(fitnesses.copy())
    partition_id=int(0.32*len(datasets))
    partition_score=new_fitness[partition_id]
    group1_id=[i for i in range(len(datasets)) if fitnesses[i] <= partition_score]
    group1=[{k:v.copy() for k,v in datasets[id].items()} for id in group1_id]
    group2=[{k:v.copy() for k,v in datasets[id].items()} for id in range(len(datasets)) if id not in group1_id]
    size1=int(len(datasets)*0.8)
    size2=len(datasets)-size1
    new_dataset=[]
    for _ in range(size1):
        new_dataset.append(
            random.choice(group1)
        )

    for _ in range(size2):
        new_dataset.append(
            random.choice(group2)
        )
    
    return new_dataset

def mutation(hashmap,generator):
    hash={k:v.copy() for k,v in hashmap.items()}
    if random.random()>0.05:
        return hash
    new_hashmap=generator.generate()
    remove_id=random.choice(list(hash.keys()))
    rest_hashmap,_=remove_subtree(hash,remove_id)
    new_hashmap=insert_subtree(rest_hashmap,remove_id,new_hashmap)
    if not exists('x',new_hashmap):
        return hash
    return new_hashmap

def crossover (hashmap1,hashmap2):
    hash1={k:v.copy() for k,v in hashmap1.items()}
    hash2={k:v.copy() for k,v in hashmap2.items()}
    if random.random()>0.9:
        return hash1,hash2
    id_1=random.choice(list(hash1.keys()))
    id_2=random.choice(list(hash2.keys()))
    rest1,sub1=remove_subtree(hash1,id_1)
    rest2,sub2=remove_subtree(hash2,id_2)

    newhash1=insert_subtree(rest1,id_1,sub2)
    newhash2=insert_subtree(rest2,id_2,sub1)
    return_value=[]
    if not exists('x',newhash1):
        return_value.append(
            hash1
        )
    else:
        return_value.append(
            newhash1
        )
    if not exists('x',newhash2):
        return_value.append(
            hash2
        )
    else:
        return_value.append(
            newhash2
        )

    return return_value





def update():
    pass

if __name__=="__main__":
    datapoint=[]
    record=[]
    with open("data.jsonl",'r') as f:
        for item in f:
            datapoint.append(eval(item))
    g=Generator(10,1e-4,1e2)
    dataset=[]
    # generate dataset
    for i in range(1000):
        dataset.append(g.generate())
    # 100 epoch 迭代
    for epoch in range(100):
        fitnesses=[fitness(item,datapoint) for item in dataset]
        min_id=fitnesses.index(min(fitnesses))
        print("epoch{}:".format(epoch),min(fitnesses),symbolize(dataset[min_id],0))
        record.append(
            {"min_loss":min(fitnesses),"epoch":epoch, "best_expression":symbolize(dataset[min_id],0)     }
            )
        newdataset=select(dataset,fitnesses)
        new1dataset=[]
        i=0
        while i<len(newdataset):
            hash1,hash2=crossover(newdataset[i],newdataset[i+1])
            i+=2
            hash1=mutation(hash1,g)
            hash2=mutation(hash1,g)
            new1dataset.append(hash1)
            new1dataset.append(hash2)
            dataset=new1dataset        
    with open("loss.jsonl",'w') as f:
        for item in record:
            f.write(json.dumps(item)+'\n')


    # symbolize dataset

    #new=mutation(dataset[1],g)
    #print(symbolize(dataset[1],0))
    #print(symbolize(new,0))



    

