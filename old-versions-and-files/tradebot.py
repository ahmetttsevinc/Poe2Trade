import math
# currency conversion rates
conversion_rates = {
    'Exalted': {'Chaos': 1/2.8, 'Aug': 400, 'Trans': 210, 'Regal': 21, 'Alchemy': 4.95, 'Divine': 1/147.5},
    'Chaos': {'Exalted': 2.79, 'Aug': 2000, 'Trans': 0, 'Regal': 60, 'Alchemy': 13, 'Divine': 1/50.0},
    'Aug': {'Exalted': 1/240, 'Chaos': 1/750, 'Trans': 1/3.0, 'Regal': 1/20.0, 'Alchemy': 1/70.0, 'Divine': 1/16000},
    'Trans': {'Exalted': 1/110, 'Chaos': 1/190, 'Aug': 5, 'Regal': 1/30.0, 'Alchemy': 1/6000.0, 'Divine': 1/6000.0},
    'Regal': {'Exalted': 1/20.0, 'Chaos': 1/33.0, 'Aug': 109, 'Trans': 45, 'Alchemy': 1/4.55, 'Divine': 1/1600.0},
    'Alchemy': {'Exalted': 4.5, 'Chaos': 1/11.5, 'Aug': 580, 'Trans': 50, 'Regal': 6, 'Divine': 1/630},
    'Divine': {'Exalted': 147, 'Chaos': 50,'Aug': 0, 'Trans': 0, 'Regal': 3100, 'Alchemy': 750}
}

def find_arbitrage(conversion_rates):
    currencies = list(conversion_rates.keys())
    
    # path = {currency: "" for currency in currencies}
    path = []

    for currency in currencies:
        path.append(currency)

        value = {currency: 1 for currency in currencies}  # starting value 1
        for neighbor, rate in conversion_rates[currency].items():
            value[neighbor] = value[currency] * rate
            if conversion_rates[neighbor][currency] != 0 and value[neighbor] > 1/conversion_rates[neighbor][currency]:
                #print("Arbitrage: " + str(conversion_rates[neighbor][currency]) +" "+ currency +  " -> "+ neighbor)
                path.append(neighbor)
                # finalize path
                path.append(currency)
                print(path)
                path = []
            else:
                currency = neighbor
                for neighbor2, rate2 in conversion_rates[neighbor].items():
                    value[neighbor2] = value[neighbor] * rate2
                    if conversion_rates[neighbor2][neighbor] != 0 and value[neighbor2] > 1/conversion_rates[neighbor2][neighbor]:
                        #print("Arbitrage: " + str(conversion_rates[neighbor2][neighbor]) +" "+ currency +  " -> "+ neighbor + " -> " + neighbor2)
                        path.append(neighbor2)
                        # finalize path
                        path.append(currency)
                        print(path)
                        path = []
                    else:
                        break

















    print(path)
          


find_arbitrage(conversion_rates)