# Navigating Epistemic Monocultures in AI-Driven Science: A Simulation Study

Replication scripts for Fazelpour et al. (ms), which explores the homogenization of research methods resulting from the use of AI to guide hypothesis generation.

---

## Scripts

### `LandscapeConstruction_NK_Modular.py`

Constructs an NK landscape with an additional parameter **R**, which defines the proportion of in- and out-module bits when the landscape is divided into 2 modules.

> **Note:** The code currently performs an exhaustive search of the landscape to identify the maximum point for normalization and likely needs to be streamlined for efficiency.

---

### `Agent_Decision_Procedures.py`

Defines agent decision procedures for 3 groups of agents:

- **Personalized agents** — receive updates from the AI tool based on their current location.
- **Non-personalized agents** — receive updates from the AI tool based on the best-performing agent in their community.
- **Randomized agents** — receive a solution from the AI tool randomly drawn from the top 10% of best-performing agents.

#### Arguments

| Flag | Description |
|------|-------------|
| `--n` | Number of dimensions on the landscape |
| `--k` | Ruggedness of the landscape (number of interdependencies per bit); must satisfy `0 < K < N` |
| `--a` | Number of agents in the simulation |
| `--r` | Number of rounds (timesteps) per simulation run |
| `--s` | Number of simulations to run |
| `--f` | Output results CSV filename |

#### Example

To run 10 simulations, each with 30 rounds and 100 agents, where N=20 and K=5:

```bash
python Agent_Decision_Procedures.py --n 20 --k 5 --a 100 --r 30 --s 10 --f 'results'
```
