import math
import random
from collections import OrderedDict
from operator import getitem
import textwrap
from matplotlib import pyplot as plt;

# CALCULATE FITNESS VALUE
def fitnessFunc( chromosome):
	fitness = 10*len(chromosome)
	for i in range(len(chromosome)):
		fitness += chromosome[i]**2 - (10*math.cos(2*math.pi*chromosome[i]))
	return fitness

# CALCULATE BINARY 
def binary(n,allele):
    x=bin(n)[2:]
    while(True):
        if(len(x)==allele):
            break
        x="0"+x
    return x

ihterations_points=[]
fitness_ponits=[]
range_of_genes = (-1000,1000)
optimize="Minimize"
no_of_allele = 4
no_of_genes_per_chromosomes = 5
no_of_chromosomes =6
no_of_parents_selected = no_of_chromosomes//2
mapping=[]
s=range_of_genes[0]
step = (range_of_genes[1]-range_of_genes[0])/(2**no_of_allele-1)

# MAPPING ALLELE TO ORIGINAL VALUES
for i in range(2**no_of_allele-1):
    mapping.append(int(s))
    s+=step
mapping.append(int(s))

# ADDING RANDOM CHROMOSOME AND THEIR FITNESS VALUE
table={}
for i in range(no_of_chromosomes):
    table[i]={}
for i in range(no_of_chromosomes):
    chromosomes=[]
    binary_chromosomes=[]
    original_value=[]
    for j in range(no_of_genes_per_chromosomes):
        n=random.randint(0,2**no_of_allele-1)
        chromosomes.append(n)
        original_value.append(mapping[n])
        binary_chromosomes.append(binary(n,no_of_allele))
    table[i]['chromosome']=chromosomes
    table[i]['orginalvalues']=original_value
    table[i]['binary']=binary_chromosomes
    table[i]['fitness']= fitnessFunc(table[i]['orginalvalues'])

    
#  SORTING TABLE ACCRDING TO FITNESS VALUE
for interations in range(500):
    

    table= OrderedDict(sorted(table.items(),key=lambda x:getitem(x[1], 'fitness')))
    for key in table.keys():
        fitness_ponits.append(table[key]['fitness'])
        break
    ihterations_points.append(interations)
    

    # SELECTING PARENTS
    while(len(table)!=no_of_parents_selected):
        table.popitem()

    # ASSIGN RANKS

    if(optimize=='Minimize'):
        i=1
        total=no_of_parents_selected*(no_of_parents_selected+1)/2
        for chromosome,val in table.items():
            val['rank']=i
            
            val['probability']=round((no_of_parents_selected-(i-1))/total,3)
            i+=1
    elif(optimize=='Maximize'):
        i=no_of_parents_selected
        for chromosome,val in table.items():
            val['rank']=i
            val['probability']=round((i/no_of_parents_selected),3)
            i-=1


    selected=[]
    child_chromosome=[]
    for key in table.keys():
        selected.append(key)
    point_of_crossover=random.randint(1,2**no_of_allele-1)

    for i in range(no_of_parents_selected):
        # CROSSOVER
        child_chromosome=[]
        originalvalues=[]
        while(True):
            choosen_pair=random.randint(0,no_of_parents_selected-1)
            if(choosen_pair!=i):
                break
        parent_1="".join(table[selected[i]]['binary'])
        parent_2="".join(table[selected[choosen_pair]]['binary']) 
        total_crossover= parent_1[:point_of_crossover]+parent_2[point_of_crossover:]
        
        

        # MUTATION
        mutation_bit = random.randint(
            0, no_of_allele*no_of_genes_per_chromosomes-1)

        if(total_crossover[mutation_bit]=='1'):
            total_crossover=total_crossover[:mutation_bit]+'0'+total_crossover[mutation_bit+1:]
        else:
            total_crossover=total_crossover[:mutation_bit]+'1'+total_crossover[mutation_bit+1:]

        child_binary=textwrap.wrap(total_crossover,no_of_allele)

        for ch in child_binary:
            child_chromosome.append(int(ch,2))
            originalvalues.append(mapping[int(ch,2)])
        
        for j in range(no_of_chromosomes):
            if j not in table.keys():
                table[j]={}
                break
        table[j]['chromosome']=child_chromosome
        table[j]['orginalvalues']=originalvalues
        table[j]['binary']=child_binary
        table[j]['fitness']= fitnessFunc(table[j]['orginalvalues'])
        table= OrderedDict(sorted(table.items(),key=lambda x:getitem(x[1], 'fitness')))

# PLOTTING ON GRAPH

plt.plot(ihterations_points,fitness_ponits)
plt.xlabel('No.of ihterations')
plt.ylabel("Fitness value")
plt.show()
