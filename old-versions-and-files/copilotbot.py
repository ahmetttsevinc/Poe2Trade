# Dönüşüm oranlarını tanımlayın
conversion_rates = {
    'Exalted': {'Chaos': 1/2.8, 'Aug': 400, 'Trans': 210, 'Regal': 21, 'Alchemy': 4.95, 'Divine': 1/147.5},
    'Chaos': {'Exalted': 2.79, 'Aug': 2000, 'Regal': 60, 'Alchemy': 13, 'Divine': 1/50.0},
    'Aug': {'Exalted': 1/240, 'Chaos': 1/750, 'Trans': 1/3.0, 'Regal': 1/20.0, 'Alchemy': 1/70.0, 'Divine': 1/16000},
    'Trans': {'Exalted': 1/110, 'Chaos': 1/190, 'Aug': 5, 'Regal': 1/30.0, 'Alchemy': 1/6000.0, 'Divine': 1/6000.0},
    'Regal': {'Exalted': 1/20.0, 'Chaos': 1/33.0, 'Aug': 109, 'Trans': 45, 'Alchemy': 1/4.55, 'Divine': 1/1600.0},
    'Alchemy': {'Exalted': 4.5, 'Chaos': 1/11.5, 'Aug': 580, 'Trans': 50, 'Regal': 6, 'Divine': 1/630},
    'Divine': {'Exalted': 147, 'Chaos': 50, 'Regal': 3100, 'Alchemy': 750}
}

# Başlangıç miktarlarını belirleyin
inventory = {
    'Exalted': 10,
    'Chaos': 0,
    'Aug': 0,
    'Trans': 0,
    'Regal': 0,
    'Alchemy': 0,
    'Divine': 0
}

def maximize_value(inventory, conversion_rates, iterations=100):
    for _ in range(iterations):
        for item in inventory:
            for target in conversion_rates[item]:
                amount_to_convert = inventory[item]
                if amount_to_convert > 0:
                    conversion_rate = conversion_rates[item][target]
                    inventory[target] += amount_to_convert * conversion_rate
                    inventory[item] = 0
    return inventory

# Dönüşümü gerçekleştir
maximized_inventory = maximize_value(inventory, conversion_rates)
print(maximized_inventory)
