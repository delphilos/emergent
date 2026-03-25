#These are the simulation codes, written in Python 2.7, for Jingyi Wu (LSE Philosophy)'s paper "Better than Best," forthcoming in Philosophy of Science.
#This work is licensed under a Creative Commons Attribution 4.0 International License.
#For questions, please write to Jingyi.Wu@uci.edu.

import random
import numpy as np
from scipy.stats import beta
from numpy import random
from scipy.special import comb
from random import sample
from itertools import product
import multiprocessing as mp
from multiprocessing import Pool

n=20
k=5
#change the value of n and k for landscapes of different ruggedness

total_agents=100
proportion_range=[.2,.4,.6,.8] #proportion of agents who adopt the "better" strategy in a mixed community
rounds=200
simulation_runs=1000
probability_range=[.4,.6,.8,1] #probability of connection for a one way random network
velocity_range=[1,3,5]

triples=[]

for proportion in proportion_range:
	for probability in probability_range:
		for velocity in velocity_range:
			triples.append([proportion,probability,velocity])

def complete(total_agents):
	network=[[1 for agents in range(total_agents)] for other_agents in range(total_agents)]
	return network

def random_one_way_network(total_agents,probability):
	network=[[0 for agents in range(total_agents)] for other_agents in range(total_agents)]
	for agents in range(total_agents):
		for other_agents in range(total_agents):
			if agents==other_agents:
				network[agents][other_agents]=1
			elif agents!=other_agents:
				if random.uniform(0,1)<probability:
					network[agents][other_agents]=1
	return network

def dfs(visited, G, node, k):
	if node not in visited:
		visited.add(node)
		for n in range(k):
			if G[node][n]==1:
				dfs(visited, G, n, k)

def check_connection(G, k):
	connected=[]
	for n in range(k):
		visited=set()
		dfs(visited, G, n, k)
		connected.append(visited==set(list(range(k))))
	if all(connected):
		return True

def maximum_score(n,k,l,valuation_list):
	maximum_score=0
	for i in product([0,1],repeat=n):
		list_mode=list(i)
		score=score_calculation(list_mode,n,k,l,valuation_list)
		if score>maximum_score:
			maximum_score=score
	return maximum_score

def list_split(listA, n):
    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                [None for y in range(n-len(every_chunk))]
        yield every_chunk

def score_calculation(string,n,k,l,valuation_list):
	total=0
	working_list=[]
	for i in range(n):
		working_list=valuation_list[string[i]][:]
		for index in range(len(l)-1):
			working_list=working_list[string[i-l[index]]][:]
		total+=working_list[string[i-l[len(l)-1]]]
	return (total/n)**8

def list_duplicates_of(seq,item):
	start_at = -1
	locs = []
	while True:
		try:
			loc = seq.index(item,start_at+1)
		except ValueError:
			break
		else:
			locs.append(loc)
			start_at = loc
	return locs

def list_better(seq,value):
	better=[]
	for index in range(len(seq)):
		if seq[index]>value:
			better.append(index)
	return better

def behavioral_change_best_answer(best_agents,n,k,l,valuation_list,t,average_score_best,random_network,max_score,velocity):
	sorting_list=[]

	for agent_index in range(total_agents):
		sorting_list.append(score_calculation(best_agents[agent_index],n,k,l,valuation_list))

	average_score_best[t]+=(((sum(sorting_list)/len(sorting_list))/max_score))

	if t%velocity==0:
		for agent_index in range(total_agents):
			change_number=0
			product=[]
			for num1, num2 in zip(random_network[agent_index], sorting_list):
				product.append(num1 * num2)
			max_index=list_duplicates_of(product, max(product))
			if sorting_list[agent_index]!=max(product):
				best_agents[agent_index]=best_agents[random.choice(max_index)][:]
			else:
				change_number=random.randint(0,n)
				copy_string=best_agents[agent_index][:]
				copy_string[change_number]=(1-copy_string[change_number])
				if score_calculation(copy_string,n,k,l,valuation_list)>max(product):
					best_agents[agent_index]=copy_string[:]
	elif t%velocity!=0:
		for agent_index in range(total_agents):
			change_number=random.randint(0,n)
			copy_string=best_agents[agent_index][:]
			copy_string[change_number]=(1-copy_string[change_number])
			if score_calculation(copy_string,n,k,l,valuation_list)>sorting_list[agent_index]:
				best_agents[agent_index]=copy_string[:]

def behavioral_change_better_answer(better_agents,n,k,l,valuation_list,t,average_score_better,random_network,max_score,velocity):
	sorting_list=[]

	for agent_index in range(total_agents):
		sorting_list.append(score_calculation(better_agents[agent_index],n,k,l,valuation_list))

	average_score_better[t]+=(((sum(sorting_list)/len(sorting_list))/max_score))

	if t%velocity==0:
		for agent_index in range(total_agents):
			change_number=0
			product=[]
			for num1, num2 in zip(random_network[agent_index], sorting_list):
				product.append(num1 * num2)

			if sorting_list[agent_index]!=max(product):
				better_list=list_better(product, sorting_list[agent_index])
				better_agents[agent_index]=better_agents[random.choice(better_list)][:]
			else:
				change_number=random.randint(0,n)
				copy_string=better_agents[agent_index][:]
				copy_string[change_number]=(1-copy_string[change_number])
				if score_calculation(copy_string,n,k,l,valuation_list)>max(product):
					better_agents[agent_index]=copy_string[:]
	elif t%velocity!=0:
		for agent_index in range(total_agents):
			change_number=random.randint(0,n)
			copy_string=better_agents[agent_index][:]
			copy_string[change_number]=(1-copy_string[change_number])
			if score_calculation(copy_string,n,k,l,valuation_list)>sorting_list[agent_index]:
				better_agents[agent_index]=copy_string[:]

def behavioral_change_mixed(mixed_agents,n,k,l,valuation_list,t,average_score_mixed, average_score_mixed_better,average_score_mixed_best, random_network,max_score,velocity):
	sorting_list=[]

	for agent_index in range(total_agents):
		sorting_list.append(score_calculation(mixed_agents[agent_index],n,k,l,valuation_list))

	average_score_mixed[t]+=(((sum(sorting_list)/len(sorting_list))/max_score))
	average_score_mixed_better[t]+=((sum(sorting_list[0:int(total_agents*proportion)])/(total_agents*proportion))/max_score)
	average_score_mixed_best[t]+=((sum(sorting_list[int(total_agents*proportion):total_agents])/(total_agents*(1-proportion)))/max_score)

	if t%velocity==0:
		for agent_index in range(int(total_agents*proportion)):
			change_number=0
			product=[]
			for num1, num2 in zip(random_network[agent_index], sorting_list):
				product.append(num1 * num2)

			if sorting_list[agent_index]!=max(product):
				better_list=list_better(product, sorting_list[agent_index])
				mixed_agents[agent_index]=mixed_agents[random.choice(better_list)][:]
			else:
				change_number=random.randint(0,n)
				copy_string=mixed_agents[agent_index][:]
				copy_string[change_number]=(1-copy_string[change_number])
				if score_calculation(copy_string,n,k,l,valuation_list)>max(product):
					mixed_agents[agent_index]=copy_string[:]
		for agent_index in range(int(total_agents*proportion), total_agents):
			change_number=0
			product=[]
			for num1, num2 in zip(random_network[agent_index], sorting_list):
				product.append(num1 * num2)
			max_index=list_duplicates_of(product, max(product))
			if sorting_list[agent_index]!=max(product):
				mixed_agents[agent_index]=mixed_agents[random.choice(max_index)][:]
			else:
				change_number=random.randint(0,n)
				copy_string=mixed_agents[agent_index][:]
				copy_string[change_number]=(1-copy_string[change_number])
				if score_calculation(copy_string,n,k,l,valuation_list)>max(product):
					mixed_agents[agent_index]=copy_string[:]
	elif t%velocity!=0:
		for agent_index in range(total_agents):
			change_number=random.randint(0,n)
			copy_string=mixed_agents[agent_index][:]
			copy_string[change_number]=(1-copy_string[change_number])
			if score_calculation(copy_string,n,k,l,valuation_list)>sorting_list[agent_index]:
				mixed_agents[agent_index]=copy_string[:]

simulation=0
average_score_best=[0 for s in range(rounds)]
average_score_better=[0 for s in range(rounds)]
average_score_mixed=[0 for s in range(rounds)]
average_score_mixed_best=[0 for s in range(rounds)]
average_score_mixed_better=[0 for s in range(rounds)]

def run(triple):
	proportion=triple[0]
	probability=triple[1]
	velocity=triple[2]
	simulation=0
	average_score_best=[0 for s in range(rounds)]
	average_score_better=[0 for s in range(rounds)]
	average_score_mixed=[0 for s in range(rounds)]
	average_score_mixed_best=[0 for s in range(rounds)]
	average_score_mixed_better=[0 for s in range(rounds)]
	
	while simulation<simulation_runs:
		t=1
		l=sample(range(1,n),k)
		valuation_list=[[random.uniform(0,1) for w in range(2)] for m in range(2**k)]
		for i in range(k-1):
			valuation_list=list(list_split(valuation_list,2))
		best_agents=[[random.randint(0,2) for w in range(n)] for agents in range(total_agents)]
		better_agents=best_agents[:]
		complete_best_agents=best_agents[:]
		complete_better_agents=best_agents[:]
		mixed_agents=best_agents[:]

		random_network=random_one_way_network(total_agents,probability)
		while check_connection(random_network,total_agents)!=True:
			random_network=random_one_way_network(total_agents,probability)

		complete_network=complete(total_agents)

		max_score=maximum_score(n,k,l,valuation_list)

		while t<rounds:
			behavioral_change_better_answer(better_agents,n,k,l,valuation_list,t,average_score_better,random_network,max_score,velocity)
			behavioral_change_best_answer(best_agents,n,k,l,valuation_list,t,average_score_best,random_network,max_score,velocity)
			behavioral_change_mixed(mixed_agents,n,k,l,valuation_list,t,average_score_mixed, average_score_mixed_better,average_score_mixed_best, random_network,max_score,velocity)
			t+=1
		simulation+=1

	return [triple,average_score_best,average_score_better,average_score_mixed,average_score_mixed_better,average_score_mixed_best]

if __name__ == '__main__':
	p=Pool(mp.cpu_count())
	results=p.map(run, triples)

print results
