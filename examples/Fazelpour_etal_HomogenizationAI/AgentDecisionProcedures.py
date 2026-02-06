import random
import numpy as np
from random import sample
import multiprocessing as mp
from multiprocessing import Pool, shared_memory
from tqdm import tqdm
import pandas as pd
import csv
from scipy.spatial import distance
import heapq
import networkx as nx
import gc
from typing import List, Tuple
import argparse

# Import the optimized landscape
from LandscapeConstruction_NK_Modular import OptimizedNKLandscape

# Argument parser
parser = argparse.ArgumentParser('AISIM Modular Optimized')
parser.add_argument('--n', required=True, type=int, help='n: number of dimensions')
parser.add_argument('--k', required=True, type=int, help='k: ruggedness of landscape')
parser.add_argument('--a', required=True, type=int, help='a: number of agents')
parser.add_argument('--r', required=True, type=int, help='r: number of timesteps')
parser.add_argument('--s', required=True, type=int, help='s: number of simulations')
parser.add_argument('--f', required=True, type=str, help='f: filename')
parser.add_argument('--cache_size', type=int, default=50000, help='Maximum cache size for fitness values')

args = parser.parse_args()
n = args.n
k = args.k
total_agents = args.a
rounds = args.r
simulation_runs = args.s
filename = args.f
cache_size = args.cache_size

# Reduced parameter combinations for faster testing
probability_range = [.25, .75]  # Reduced from 3 to 2 values
velocity_range = [.25, .75]     # Reduced from 2 to 2 values  
trigger_AI = [.25, .75]         # Reduced from 2 to 2 values
r_range = [.25, .75]            # Reduced from 3 to 2 values

simtuples = []
for probability in probability_range:
    for velocity in velocity_range:
        for trigger in trigger_AI:
            for r in r_range:
                simtuples.append([probability, velocity, trigger, r])

print(f"Total parameter combinations: {len(simtuples)}")

# Optimized helper functions
def csr_matrix_to_lists_optimized(csr_matrix):
    """More memory-efficient adjacency list conversion"""
    return csr_matrix.toarray().astype(np.uint8)

def list_duplicates_of(seq, item):
    """Optimized duplicate finding"""
    return [i for i, x in enumerate(seq) if x == item]

def avg_ham_optimized(agents: np.ndarray) -> float:
    """Vectorized Hamming distance calculation"""
    if len(agents) <= 1:
        return 0.0
    
    # Convert to numpy array if not already
    agents_array = np.array(agents, dtype=np.uint8)
    
    # Vectorized pairwise Hamming distance
    total_dist = 0
    pairs = 0
    
    for i in range(len(agents_array)):
        for j in range(i + 1, len(agents_array)):
            hamming_dist = np.mean(agents_array[i] != agents_array[j])
            total_dist += hamming_dist
            pairs += 1
    
    return total_dist / pairs if pairs > 0 else 0

def single_bit_optimization_optimized(agent: np.ndarray, landscape) -> np.ndarray:
    """Optimized single bit optimization with numpy"""
    current_fitness = landscape.get_fitness(agent)
    
    best_improvement = 0
    best_bit_to_flip = None
    
    # Focus on computational module (bits 10-19)
    for bit_idx in range(10, 20):
        if bit_idx < len(agent):
            # Create test agent efficiently
            test_agent = agent.copy()
            test_agent[bit_idx] = 1 - test_agent[bit_idx]
            
            new_fitness = landscape.get_fitness(test_agent)
            improvement = new_fitness - current_fitness
            
            if improvement > best_improvement:
                best_improvement = improvement
                best_bit_to_flip = bit_idx
    
    if best_bit_to_flip is not None:
        agent[best_bit_to_flip] = 1 - agent[best_bit_to_flip]
    
    return agent

def top10idx_optimized(inputs: List[float]) -> List[int]:
    """Optimized top 10 index finding"""
    return heapq.nlargest(10, range(len(inputs)), key=inputs.__getitem__)

# Optimized simulation functions
def NOAI_optimized(agents: np.ndarray, landscape, t: int, metrics: dict, 
                  network: np.ndarray, velocity: float):
    """Memory-optimized NOAI function"""
    # Calculate all fitness values at once
    fitness_scores = np.array([landscape.get_fitness(agent) for agent in agents])
    
    # Update metrics
    metrics['average_score_best'][t] += np.mean(fitness_scores)
    metrics['noAI_hamming'][t] += avg_ham_optimized(agents)
    
    # Vectorized learning decisions
    learning_probs = np.random.random(total_agents)
    
    for agent_idx in range(total_agents):
        if learning_probs[agent_idx] <= velocity:
            # Social learning
            products = network[agent_idx] * fitness_scores
            max_product = np.max(products)
            
            if fitness_scores[agent_idx] < max_product:
                max_indices = np.where(products == max_product)[0]
                chosen_idx = np.random.choice(max_indices)
                agents[agent_idx] = agents[chosen_idx].copy()
        else:
            # Individual exploration
            change_bit = random.randint(0, n - 1)
            test_agent = agents[agent_idx].copy()
            test_agent[change_bit] = 1 - test_agent[change_bit]
            
            if landscape.get_fitness(test_agent) > fitness_scores[agent_idx]:
                agents[agent_idx] = test_agent

def PERSONALIZED_optimized(agents: np.ndarray, landscape, t: int, metrics: dict,
                          network: np.ndarray, velocity: float, trigger: float):
    """Optimized personalized AI function"""
    fitness_scores = np.array([landscape.get_fitness(agent) for agent in agents])
    
    metrics['average_score_personalized'][t] += np.mean(fitness_scores)
    metrics['personalized_hamming'][t] += avg_ham_optimized(agents)
    
    num_triggers = 0
    sum_inc_fit = 0
    learning_probs = np.random.random(total_agents)
    
    for agent_idx in range(total_agents):
        if learning_probs[agent_idx] <= velocity:
            # Social learning (same as NOAI)
            products = network[agent_idx] * fitness_scores
            max_product = np.max(products)
            
            if fitness_scores[agent_idx] < max_product:
                max_indices = np.where(products == max_product)[0]
                chosen_idx = np.random.choice(max_indices)
                agents[agent_idx] = agents[chosen_idx].copy()
        else:
            trigger_prob = random.random()
            if trigger_prob <= trigger:
                # AI optimization
                num_triggers += 1
                old_fitness = fitness_scores[agent_idx]
                agents[agent_idx] = single_bit_optimization_optimized(agents[agent_idx], landscape)
                new_fitness = landscape.get_fitness(agents[agent_idx])
                sum_inc_fit += (new_fitness - old_fitness)
            else:
                # Individual exploration
                change_bit = random.randint(0, n - 1)
                test_agent = agents[agent_idx].copy()
                test_agent[change_bit] = 1 - test_agent[change_bit]
                
                if landscape.get_fitness(test_agent) > fitness_scores[agent_idx]:
                    agents[agent_idx] = test_agent
    
    metrics['personal_counter'][t] += num_triggers
    if num_triggers > 0:
        metrics['avgScoreInc_personal'][t] += sum_inc_fit / num_triggers

def NONPERSONALIZED_optimized(agents: np.ndarray, landscape, t: int, metrics: dict,
                             network: np.ndarray, velocity: float, trigger: float):
    """Optimized non-personalized AI function"""
    fitness_scores = np.array([landscape.get_fitness(agent) for agent in agents])
    
    metrics['average_score_nopersonalized'][t] += np.mean(fitness_scores)
    metrics['nonpersonal_hamming'][t] += avg_ham_optimized(agents)
    
    num_triggers = 0
    sum_fit = 0
    num_adopted = 0
    sum_inc_fit = 0
    learning_probs = np.random.random(total_agents)
    
    for agent_idx in range(total_agents):
        if learning_probs[agent_idx] <= velocity:
            # Social learning
            products = network[agent_idx] * fitness_scores
            max_product = np.max(products)
            
            if fitness_scores[agent_idx] < max_product:
                max_indices = np.where(products == max_product)[0]
                chosen_idx = np.random.choice(max_indices)
                agents[agent_idx] = agents[chosen_idx].copy()
        else:
            best_score_idx = np.argmax(fitness_scores)
            best_agent = agents[best_score_idx]
            
            trigger_prob = random.random()
            if trigger_prob <= trigger:
                num_triggers += 1
                copy_solution = agents[agent_idx].copy()
                copy_fit = fitness_scores[agent_idx]
                
                # Get the last module from the best agent
                last_module_idx = landscape.M - 1
                last_module_bits = landscape._get_module_bits(last_module_idx)
                
                # Apply the best agent's last module to current agent
                new_solution = copy_solution.copy()
                for bit_idx in last_module_bits:
                    new_solution[bit_idx] = best_agent[bit_idx]
                
                new_fit = landscape.get_fitness(new_solution)
                change_fitness = new_fit - copy_fit
                sum_fit += change_fitness
                
                if new_fit > copy_fit:
                    num_adopted += 1
                    sum_inc_fit += change_fitness
                    agents[agent_idx] = new_solution
            else:
                # Individual exploration
                change_bit = random.randint(0, n - 1)
                test_agent = agents[agent_idx].copy()
                test_agent[change_bit] = 1 - test_agent[change_bit]
                
                if landscape.get_fitness(test_agent) > fitness_scores[agent_idx]:
                    agents[agent_idx] = test_agent
    
    metrics['nopersonal_counter'][t] += num_triggers
    metrics['nopersonal_IncCounter'][t] += num_adopted
    if num_triggers > 0:
        metrics['avgScoreSuggestion_nopersonal'][t] += sum_fit / num_triggers
    if num_adopted > 0:
        metrics['avgScoreInc_nopersonal'][t] += sum_inc_fit / num_adopted

def RANDOMIZED_optimized(agents: np.ndarray, landscape, t: int, metrics: dict,
                        network: np.ndarray, velocity: float, trigger: float):
    """Optimized randomized AI function"""
    fitness_scores = np.array([landscape.get_fitness(agent) for agent in agents])
    
    metrics['average_score_random'][t] += np.mean(fitness_scores)
    metrics['random_hamming'][t] += avg_ham_optimized(agents)
    
    num_triggers = 0
    sum_fit = 0
    num_adopted = 0
    sum_inc_fit = 0
    learning_probs = np.random.random(total_agents)
    
    for agent_idx in range(total_agents):
        if learning_probs[agent_idx] <= velocity:
            # Social learning
            products = network[agent_idx] * fitness_scores
            max_product = np.max(products)
            
            if fitness_scores[agent_idx] < max_product:
                max_indices = np.where(products == max_product)[0]
                chosen_idx = np.random.choice(max_indices)
                agents[agent_idx] = agents[chosen_idx].copy()
        else:
            trigger_prob = random.random()
            if trigger_prob <= trigger:
                num_triggers += 1
                top10_indices = top10idx_optimized(fitness_scores.tolist())
                chum = [agents[i] for i in top10_indices]
                
                copy_solution = agents[agent_idx].copy()
                copy_fit = fitness_scores[agent_idx]
                rando = random.randint(0, len(chum) - 1)
                temp = chum[rando]
                
                last_module_idx = landscape.M - 1
                last_module_bits = landscape._get_module_bits(last_module_idx)
                
                # Create new solution by replacing last module
                new_solution = copy_solution.copy()
                for bit_idx in last_module_bits:
                    new_solution[bit_idx] = temp[bit_idx]
                
                new_fit = landscape.get_fitness(new_solution)
                change_fitness = new_fit - copy_fit
                sum_fit += change_fitness
                
                if new_fit > copy_fit:
                    num_adopted += 1
                    sum_inc_fit += change_fitness
                    agents[agent_idx] = new_solution
            else:
                # Individual exploration
                change_bit = random.randint(0, n - 1)
                test_agent = agents[agent_idx].copy()
                test_agent[change_bit] = 1 - test_agent[change_bit]
                
                if landscape.get_fitness(test_agent) > fitness_scores[agent_idx]:
                    agents[agent_idx] = test_agent
    
    metrics['random_counter'][t] += num_triggers
    metrics['random_IncCounter'][t] += num_adopted
    if num_triggers > 0:
        metrics['avgScoreSuggestion_random'][t] += sum_fit / num_triggers
    if num_adopted > 0:
        metrics['avgScoreInc_random'][t] += sum_inc_fit / num_adopted

def run_modular_optimized(simtuple: List[float]) -> List:
    """Optimized main simulation function"""
    probability, velocity, trigger, r = simtuple
    
    # Initialize metrics with more memory-efficient storage
    metrics = {
        'average_score_best': np.zeros(rounds, dtype=np.float32),
        'average_score_personalized': np.zeros(rounds, dtype=np.float32), 
        'average_score_nopersonalized': np.zeros(rounds, dtype=np.float32),
        'average_score_random': np.zeros(rounds, dtype=np.float32),
        'noAI_hamming': np.zeros(rounds, dtype=np.float32),
        'personalized_hamming': np.zeros(rounds, dtype=np.float32),
        'nonpersonal_hamming': np.zeros(rounds, dtype=np.float32),
        'random_hamming': np.zeros(rounds, dtype=np.float32),
        'avgScoreInc_personal': np.zeros(rounds, dtype=np.float32),
        'personal_counter': np.zeros(rounds, dtype=np.int32),
        'random_counter': np.zeros(rounds, dtype=np.int32),
        'avgScoreSuggestion_random': np.zeros(rounds, dtype=np.float32),
        'random_IncCounter': np.zeros(rounds, dtype=np.int32),
        'avgScoreInc_random': np.zeros(rounds, dtype=np.float32),
        'avgScoreSuggestion_nopersonal': np.zeros(rounds, dtype=np.float32),
        'nopersonal_counter': np.zeros(rounds, dtype=np.int32),
        'nopersonal_IncCounter': np.zeros(rounds, dtype=np.int32),
        'avgScoreInc_nopersonal': np.zeros(rounds, dtype=np.float32)
    }
    
    pbar = tqdm(desc=f"R={r:.2f}, p={probability:.2f}", total=simulation_runs, leave=False)
    
    for simulation in range(simulation_runs):
        # Create optimized landscape with smaller cache
        landscape = OptimizedNKLandscape(N=n, K=k, R=r, seed=simulation, 
                                       use_cache=True, max_cache_size=cache_size)
        
        # Initialize agents with efficient data types
        initial_agents = np.random.randint(0, 2, (total_agents, n), dtype=np.uint8)
        
        # Create separate copies for each condition
        noai_agents = initial_agents.copy()
        personal_agents = initial_agents.copy()
        nopersonal_agents = initial_agents.copy()
        random_agents = initial_agents.copy()
        
        # Create network more efficiently
        network = nx.gnp_random_graph(total_agents, probability, directed=True)
        adj_matrix = nx.adjacency_matrix(network).toarray().astype(np.uint8)
        
        # Run simulation rounds
        for t in range(1, rounds):
            NOAI_optimized(noai_agents, landscape, t, metrics, adj_matrix, velocity)
            PERSONALIZED_optimized(personal_agents, landscape, t, metrics, adj_matrix, velocity, trigger)
            NONPERSONALIZED_optimized(nopersonal_agents, landscape, t, metrics, adj_matrix, velocity, trigger)
            RANDOMIZED_optimized(random_agents, landscape, t, metrics, adj_matrix, velocity, trigger)
            
            # Clear cache periodically to manage memory
            if t % 100 == 0:
                landscape.clear_cache()
        
        # Clean up landscape to free memory
        del landscape
        gc.collect()
        
        pbar.update(1)
    
    pbar.close()
    
    # Convert metrics to lists and normalize by simulation runs
    result = [simtuple]
    for key in ['average_score_best', 'noAI_hamming', 
                'average_score_personalized', 'personal_counter', 'avgScoreInc_personal', 'personalized_hamming',
                'average_score_nopersonalized', 'nonpersonal_hamming', 'nopersonal_counter', 'avgScoreSuggestion_nopersonal', 'nopersonal_IncCounter', 'avgScoreInc_nopersonal',
                'average_score_random', 'random_counter', 'avgScoreSuggestion_random', 'random_IncCounter', 'avgScoreInc_random', 'random_hamming']:
        if key in metrics:
            normalized_values = (metrics[key] / simulation_runs).tolist()
            result.append(normalized_values)
    
    return result

if __name__ == '__main__':
    print(f"Starting optimized simulation with {mp.cpu_count()} cores")
    print(f"Problem size: N={n}, K={k}")
    print(f"Landscape size: 2^{n} = {2**n:,} states")
    print(f"Cache size per landscape: {cache_size:,} states")
    
    # Use fewer processes for very large problems to avoid memory issues
    max_processes = min(mp.cpu_count(), 8) if n > 16 else mp.cpu_count()
    
    with Pool(max_processes) as p:
        results = p.map(run_modular_optimized, simtuples)
    
    # Save results
    output_filename = f'optimized_modular_results_n{n}_k{k}_a{total_agents}_r{rounds}_s{simulation_runs}_{filename}.csv'
    
    with open(output_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)
    
    print(f"Results saved to: {output_filename}")
    print("Simulation complete!")