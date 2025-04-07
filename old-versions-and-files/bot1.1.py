import math

def find_arbitrage(conversion_rates):
    currencies = list(conversion_rates.keys())
    n = len(currencies)

    # Create a mapping of currency names to indices for easier processing
    currency_index = {currency: i for i, currency in enumerate(currencies)}

    # Initialize the graph with negative logarithms of the rates
    graph = [[math.inf] * n for _ in range(n)]
    for source, targets in conversion_rates.items():
        for target, rate in targets.items():
            if rate > 0:  # Ensure no zero or invalid rates
                source_idx = currency_index[source]
                target_idx = currency_index[target]
                graph[source_idx][target_idx] = -math.log(rate)

    # Bellman-Ford algorithm to detect negative cycles
    distances = [math.inf] * n
    predecessors = [-1] * n

    for start in range(n):
        distances[start] = 0
        for _ in range(n - 1):
            for u in range(n):
                for v in range(n):
                    if graph[u][v] < math.inf and distances[u] + graph[u][v] < distances[v]:
                        distances[v] = distances[u] + graph[u][v]
                        predecessors[v] = u

        # Check for negative cycles
        for u in range(n):
            for v in range(n):
                if graph[u][v] < math.inf and distances[u] + graph[u][v] < distances[v]:
                    # Negative cycle found; reconstruct the cycle
                    cycle = []
                    visited = set()
                    current = v
                    while current not in visited:
                        visited.add(current)
                        current = predecessors[current]

                    # Extract the cycle
                    start_cycle = current
                    cycle.append(current)
                    current = predecessors[current]
                    while current != start_cycle:
                        cycle.append(current)
                        current = predecessors[current]
                    cycle.append(start_cycle)
                    cycle.reverse()

                    # Ensure the cycle has at least 3 different currencies
                    if len(cycle) >= 3:
                        # Convert indices back to currency names
                        cycle_names = [currencies[i] for i in cycle]

                        # Validate that the cycle is not just a direct repetition of a currency
                        if len(set(cycle_names)) >= 3:  # Check for at least 3 unique currencies
                            return cycle_names

    return None

# Example conversion rates
conversion_rates = {
    'A': {'B': 1.5, 'C': 2.2, 'D': 3.0},
    'B': {'A': 0.7, 'C': 1.4, 'D': 2.8},
    'C': {'A': 0.45, 'B': 0.7, 'D': 1.9},
    'D': {'A': 0.33, 'B': 0.35, 'C': 0.53}
}




# Find arbitrage opportunities
arbitrage_cycle = find_arbitrage(conversion_rates)
if arbitrage_cycle:
    print("Arbitrage opportunity found:", " -> ".join(arbitrage_cycle))
else:
    print("No arbitrage opportunities found.")
