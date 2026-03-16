import numpy as np
from typing import Dict, List, Tuple, Optional
import gc

class OptimizedNKLandscape:
    """
    Optimized NK Landscape with memory-efficient fitness calculation
    Key optimizations:
    1. Streaming min/max calculation without storing all fitness values
    2. On-demand fitness calculation using mathematical transformation
    3. Memory-efficient state representation
    4. Optional fitness caching with memory limits
    """
    
    def __init__(self, N: int, K: int, R: float = 0.0, seed: Optional[int] = None, 
                 use_cache: bool = True, max_cache_size: int = 100000):
        # Input validation
        if N % 2 != 0:
            raise ValueError(f"N must be even (divisible by 2). Got N={N}")
        if K >= N:
            raise ValueError(f"K must be less than N. Got K={K}, N={N}")
        if K < 0:
            raise ValueError(f"K must be non-negative. Got K={K}")
        if not 0 <= R <= 1:
            raise ValueError(f"R must be between 0 and 1. Got R={R}")
        
        self.N = N
        self.K = K
        self.M = 2
        self.R = R
        self.module_size = N // 2
        self.rng = np.random.RandomState(seed)
        self.use_cache = use_cache
        self.max_cache_size = max_cache_size
        
        # Validate intra-module dependencies
        max_intra_per_bit = min(K, self.module_size - 1)
        max_possible_R = max_intra_per_bit / K if K > 0 else 1.0
        if R > max_possible_R:
            raise ValueError(f"R={R} is too high. Maximum possible R is {max_possible_R:.3f}")
        
        # Generate interaction structure and fitness contributions
        self.interactions = self._generate_interactions()
        self.fitness_contributions = self._generate_fitness_contributions()
        
        # Initialize normalization parameters
        self.true_min_raw = None
        self.true_max_raw = None
        self.is_normalized = False
        
        # Memory-efficient cache with LRU-style eviction
        self.fitness_cache = {}
        self.cache_access_order = []
        
        # Find true min/max with streaming calculation
        self._find_normalization_bounds()
    
    def _find_normalization_bounds(self):
        """Find min/max fitness values using streaming calculation - no storage of all values"""
        print(f"Finding fitness bounds via streaming calculation (2^{self.N} = {2**self.N} states)...")
        
        min_fitness = float('inf')
        max_fitness = float('-inf')
        
        # Process states in batches to avoid memory issues
        batch_size = min(10000, 2**self.N)
        
        for batch_start in range(0, 2**self.N, batch_size):
            batch_end = min(batch_start + batch_size, 2**self.N)
            
            for i in range(batch_start, batch_end):
                # Convert integer to binary state efficiently
                state = np.array([(i >> bit) & 1 for bit in range(self.N)], dtype=np.uint8)
                
                # Calculate raw fitness
                raw_fitness = self._get_raw_fitness(state)
                
                # Update bounds
                min_fitness = min(min_fitness, raw_fitness)
                max_fitness = max(max_fitness, raw_fitness)
            
            # Progress indicator for large landscapes
            if batch_end % (2**min(self.N, 15)) == 0:
                progress = batch_end / (2**self.N) * 100
                print(f"Progress: {progress:.1f}%")
        
        self.true_min_raw = min_fitness
        self.true_max_raw = max_fitness
        self.is_normalized = True
        
        print(f"Bounds found. Raw range: [{self.true_min_raw:.6f}, {self.true_max_raw:.6f}]")
        print(f"Memory usage: No fitness lookup table stored")
    
    def _get_raw_fitness(self, state: np.ndarray) -> float:
        """Calculate raw fitness without caching"""
        if len(state) != self.N:
            raise ValueError(f"State must have length {self.N}")
        
        total_fitness = 0.0
        for i in range(self.N):
            affecting_bits = self.interactions[i]
            # Use numpy indexing for efficiency
            affecting_states = state[affecting_bits]
            # Convert binary array to index efficiently
            index = np.dot(affecting_states, 1 << np.arange(len(affecting_states)))
            total_fitness += self.fitness_contributions[i][index]
        
        return total_fitness / self.N
    
    def get_fitness(self, state: np.ndarray) -> float:
        """Calculate fitness with optional caching and mathematical transformation"""
        if len(state) != self.N:
            raise ValueError(f"State must have length {self.N}")
        
        # Use tuple for hashable cache key
        state_key = tuple(state) if self.use_cache else None
        
        # Check cache first
        if self.use_cache and state_key in self.fitness_cache:
            # Update access order for LRU
            self.cache_access_order.remove(state_key)
            self.cache_access_order.append(state_key)
            return self.fitness_cache[state_key]
        
        # Calculate raw fitness
        raw_fitness = self._get_raw_fitness(state)
        
        # Apply normalization and transformation
        if self.is_normalized and self.true_max_raw is not None:
            fitness_range = self.true_max_raw - self.true_min_raw
            if fitness_range > 0:
                normalized_fitness = (raw_fitness - self.true_min_raw) / fitness_range
                transformed_fitness = normalized_fitness ** 4
            else:
                transformed_fitness = 1.0
        else:
            transformed_fitness = raw_fitness
        
        # Cache the result if caching is enabled
        if self.use_cache:
            # Manage cache size
            if len(self.fitness_cache) >= self.max_cache_size:
                # Remove oldest entries (LRU eviction)
                oldest_key = self.cache_access_order.pop(0)
                del self.fitness_cache[oldest_key]
            
            self.fitness_cache[state_key] = transformed_fitness
            self.cache_access_order.append(state_key)
        
        return transformed_fitness
    
    def clear_cache(self):
        """Clear fitness cache to free memory"""
        self.fitness_cache.clear()
        self.cache_access_order.clear()
        gc.collect()
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'cache_size': len(self.fitness_cache),
            'max_cache_size': self.max_cache_size,
            'cache_enabled': self.use_cache
        }
    
    # Keep all the existing methods for compatibility
    def _get_module(self, bit_idx: int) -> int:
        return bit_idx // self.module_size
    
    def _get_module_bits(self, module_idx: int) -> List[int]:
        start = module_idx * self.module_size
        end = start + self.module_size
        return list(range(start, end))
    
    def _generate_interactions(self) -> Dict[int, np.ndarray]:
        """Generate interactions with numpy arrays for efficiency"""
        interactions = {}
        
        for i in range(self.N):
            affecting_bits = [i]
            if self.K == 0:
                interactions[i] = np.array(affecting_bits, dtype=np.int32)
                continue
            
            module_idx = self._get_module(i)
            
            if module_idx == 0:
                # First module: completely random dependencies
                available_bits = [b for b in range(self.N) if b != i]
                if len(available_bits) >= self.K:
                    chosen_deps = self.rng.choice(available_bits, self.K, replace=False)
                else:
                    chosen_deps = available_bits
                affecting_bits.extend(chosen_deps)
                
            else:
                # Second module: R controls intra-module percentage
                module_bits = self._get_module_bits(1)
                available_intra = [b for b in module_bits if b != i]
                available_inter = self._get_module_bits(0)
                
                num_intra = int(round(self.K * self.R))
                num_inter = self.K - num_intra
                
                num_intra = min(num_intra, len(available_intra))
                num_inter = min(num_inter, len(available_inter))
                
                if num_intra + num_inter < self.K:
                    remaining = self.K - num_intra - num_inter
                    if len(available_intra) > num_intra:
                        additional_intra = min(remaining, len(available_intra) - num_intra)
                        num_intra += additional_intra
                        remaining -= additional_intra
                    if remaining > 0 and len(available_inter) > num_inter:
                        additional_inter = min(remaining, len(available_inter) - num_inter)
                        num_inter += additional_inter
                
                chosen_deps = []
                
                if num_intra > 0 and available_intra:
                    intra_choices = self.rng.choice(available_intra, num_intra, replace=False)
                    chosen_deps.extend(intra_choices)
                
                if num_inter > 0 and available_inter:
                    inter_choices = self.rng.choice(available_inter, num_inter, replace=False)
                    chosen_deps.extend(inter_choices)
                
                affecting_bits.extend(chosen_deps)
            
            interactions[i] = np.array(sorted(affecting_bits), dtype=np.int32)
        
        return interactions
    
    def _generate_fitness_contributions(self) -> Dict[int, np.ndarray]:
        """Generate fitness contributions with appropriate data types"""
        fitness_contributions = {}
        
        for i in range(self.N):
            num_affecting = len(self.interactions[i])
            table_size = 2 ** num_affecting
            # Use float32 to save memory if precision allows
            fitness_contributions[i] = self.rng.random(table_size).astype(np.float32)
        
        return fitness_contributions
    
    def random_state(self) -> np.ndarray:
        """Generate random state with efficient data type"""
        return self.rng.randint(0, 2, self.N, dtype=np.uint8)
    
    def get_neighbors(self, state: np.ndarray) -> List[np.ndarray]:
        """Get neighbors with memory-efficient operations"""
        neighbors = []
        for i in range(self.N):
            neighbor = state.copy()
            neighbor[i] = 1 - neighbor[i]
            neighbors.append(neighbor)
        return neighbors
    
    # Keep existing analysis methods for compatibility
    def get_interaction_matrix(self) -> np.ndarray:
        matrix = np.zeros((self.N, self.N), dtype=np.uint8)  # Use uint8 for binary matrix
        for i, affecting_bits in self.interactions.items():
            matrix[i, affecting_bits] = 1
        return matrix
    
    def analyze_modularity(self) -> Dict:
        """Analyze modularity - kept for compatibility"""
        module0_intra = 0
        module1_intra = 0
        inter_dependencies = 0
        
        for i, affecting_bits in self.interactions.items():
            module_i = self._get_module(i)
            for j in affecting_bits:
                if i != j:
                    module_j = self._get_module(j)
                    if module_i == module_j:
                        if module_i == 0:
                            module0_intra += 1
                        else:
                            module1_intra += 1
                    else:
                        inter_dependencies += 1
        
        total_dependencies = module0_intra + module1_intra + inter_dependencies
        
        module1_total_deps = 0
        for i in range(self.module_size, self.N):
            module1_total_deps += len([j for j in self.interactions[i] if j != i])
        
        actual_R_module1 = module1_intra / module1_total_deps if module1_total_deps > 0 else 0
        
        return {
            'total_dependencies': total_dependencies,
            'module0_intra_dependencies': module0_intra,
            'module1_intra_dependencies': module1_intra,
            'inter_module_dependencies': inter_dependencies,
            'target_R': self.R,
            'actual_R_module1': actual_R_module1,
            'module0_intra_fraction': module0_intra / (module0_intra + inter_dependencies // 2) if (module0_intra + inter_dependencies // 2) > 0 else 0,
            'module1_intra_fraction': module1_intra / module1_total_deps if module1_total_deps > 0 else 0,
            'avg_dependencies_per_bit': total_dependencies / self.N
        }
    
    def visualize_interactions(self, save_path: Optional[str] = None, figsize: Tuple[int, int] = (10, 8)):
        """Visualize interaction matrix (helpful for validating params)"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
        except ImportError:
            raise ImportError("matplotlib is required for visualization. Install with: pip install matplotlib")
        
        # Get interaction matrix
        matrix = self.get_interaction_matrix()
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=figsize)
        
        # Create the heatmap (interactions are always binary)
        im = ax.imshow(matrix, cmap='Blues', aspect='equal', origin='upper')
        
        # Add module boundary lines
        module_boundary = self.module_size - 0.5
        ax.axhline(y=module_boundary, color='red', linewidth=2, alpha=0.7)
        ax.axvline(x=module_boundary, color='red', linewidth=2, alpha=0.7)
        
        # Add module labels
        ax.text(self.module_size // 2, -0.5, 'Module 0\n(Random Dependencies)', 
                ha='center', va='top', fontsize=12, fontweight='bold')
        ax.text(self.module_size + self.module_size // 2, -0.5, f'Module 1\n(R={self.R:.2f})', 
                ha='center', va='top', fontsize=12, fontweight='bold')
        
        # Add module boundary rectangles for clarity
        rect1 = patches.Rectangle((0-0.5, 0-0.5), self.module_size, self.module_size, 
                                 linewidth=2, edgecolor='green', facecolor='none', alpha=0.7)
        rect2 = patches.Rectangle((self.module_size-0.5, self.module_size-0.5), 
                                 self.module_size, self.module_size, 
                                 linewidth=2, edgecolor='orange', facecolor='none', alpha=0.7)
        ax.add_patch(rect1)
        ax.add_patch(rect2)
        
        # Customize plot
        ax.set_xlabel('Affecting Bit Index', fontsize=12)
        ax.set_ylabel('Affected Bit Index', fontsize=12)
        ax.set_title(f'NK Landscape Interaction Matrix\nN={self.N}, K={self.K}, R={self.R:.2f}', 
                    fontsize=14, fontweight='bold')
        
        # Set ticks
        ax.set_xticks(range(0, self.N, max(1, self.N // 10)))
        ax.set_yticks(range(0, self.N, max(1, self.N // 10)))
        
        # Add grid
        ax.grid(True, alpha=0.3, linewidth=0.5)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Dependency Exists', fontsize=12)
        
        # Add legend
        legend_elements = [
            patches.Patch(color='green', alpha=0.7, label='Module 0 (Random)'),
            patches.Patch(color='orange', alpha=0.7, label=f'Module 1 (R={self.R:.2f})'),
            patches.Patch(color='red', alpha=0.7, label='Module Boundaries')
        ]
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.15, 0.5))
        
        # Adjust layout
        plt.tight_layout()
        
        # Save if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to: {save_path}")
        
        return fig
    
    def print_interaction_summary(self):
        """Summary of interaction structure"""
        analysis = self.analyze_modularity()
        
        print(f"\n{'='*60}")
        print(f"NK LANDSCAPE INTERACTION SUMMARY")
        print(f"{'='*60}")
        print(f"Parameters: N={self.N}, K={self.K}, R={self.R:.3f}")
        print(f"Module Structure: 2 modules of {self.module_size} bits each")
        print(f"")
        
        print(f"DEPENDENCY BREAKDOWN:")
        print(f"  Total dependencies: {analysis['total_dependencies']}")
        print(f"  Module 0 intra-dependencies: {analysis['module0_intra_dependencies']}")
        print(f"  Module 1 intra-dependencies: {analysis['module1_intra_dependencies']}")
        print(f"  Inter-module dependencies: {analysis['inter_module_dependencies']}")
        print(f"")
        
        print(f"MODULARITY METRICS:")
        print(f"  Target R (Module 1): {analysis['target_R']:.3f}")
        print(f"  Actual R (Module 1): {analysis['actual_R_module1']:.3f}")
        print(f"  Module 1 intra fraction: {analysis['module1_intra_fraction']:.3f}")
        print(f"  Average dependencies per bit: {analysis['avg_dependencies_per_bit']:.2f}")
        print(f"")
        
        # Show few interactions as examples
        print(f"EXAMPLE INTERACTIONS:")
        for i in [0, 1, self.module_size, self.module_size + 1]:
            if i < self.N:
                affecting = [j for j in self.interactions[i] if j != i]  # Exclude self
                module_i = self._get_module(i)
                intra = [j for j in affecting if self._get_module(j) == module_i]
                inter = [j for j in affecting if self._get_module(j) != module_i]
                
                print(f"  Bit {i:2d} (Module {module_i}): "
                      f"intra={len(intra):2d} {intra}, inter={len(inter):2d} {inter}")
        
        print(f"{'='*60}\n")