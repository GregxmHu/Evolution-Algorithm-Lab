from tree import *
from  math import cos,sin
import random
class Generator(object):
    def __init__(self,max_depth,low_bound,high_bound):
        self.last_layer_begin_id=0
        self.low_bound=low_bound
        self.high_bound=high_bound
        layer=1
        while(layer<max_depth-1):
            self.last_layer_begin_id=2*self.last_layer_begin_id+2
            layer+=1
        self.last_layer_begin_id+=1
        self.F=[
            {'type':'op','func':add,'name':'+'},
            {'type':'op','func':mul,'name':'*'},
            {'type':'op','func':minus,'name':'-'},
            {'type':'op','func':divide,'name':'/'},
            {'type':'op','func':cos,'name':'cos'},
            {'type':'op','func':sin,'name':'sin'}
        ]
        self.var=[
            {'type':'var','name':'x','data':'unassigned'}
        ]

    def __generate__(self):
        generate_hashmap={}
        generate_id=[0]
        generate_hashmap[0]=random.choice(self.F)
        for i in generate_id:
            if generate_hashmap[i]['type']=="op":
                generate_id.append(2*i+1)
                generate_hashmap[2*i+1]=self.select(2*i+1)
                if generate_hashmap[i]['name']=="sin" or generate_hashmap[i]['name']=="cos":
                    continue
                generate_id.append(2*i+2)
                select_item_2=self.select(2*i+2)
                while generate_hashmap[i]['name']=='/' and select_item_2['type'] == 'const' and select_item_2['data'] == 0:
                   select_item_2=self.select(2*i+2)
                if generate_hashmap[i]['name']=='/' and select_item_2['type'] == 'var':
                    select_item_2['taboo']=0

                generate_hashmap[2*i+2]=select_item_2



        return generate_hashmap
    def generate(self):
        g=self.__generate__()
        while (exists('x',g)==[]):
            g=self.__generate__()
        return g


    def select(self,id):
        choices=[random.choice(self.var)]
        random_float=random.uniform(self.low_bound,self.high_bound)
        choices.append(
            {'type':'const','name':str(random_float),'data':random_float}
            )
        if id < self.last_layer_begin_id:
            choices.append(random.choice(self.F))
        
        return random.choice(choices)
