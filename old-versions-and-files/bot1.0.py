import math
# Dönüşüm oranları (currency conversion rates)
conversion_rates = {
    'Exalted': {'Chaos': 1/2.8, 'Aug': 400, 'Trans': 210, 'Regal': 21, 'Alchemy': 4.95, 'Divine': 1/147.5},
    'Chaos': {'Exalted': 2.79, 'Aug': 2000, 'Trans': 0, 'Regal': 60, 'Alchemy': 13, 'Divine': 1/50.0},
    'Aug': {'Exalted': 1/240, 'Chaos': 1/750, 'Trans': 1/3.0, 'Regal': 1/20.0, 'Alchemy': 1/70.0, 'Divine': 1/16000},
    'Trans': {'Exalted': 1/110, 'Chaos': 1/190, 'Aug': 5, 'Regal': 1/30.0, 'Alchemy': 1/6000.0, 'Divine': 1/6000.0},
    'Regal': {'Exalted': 1/20.0, 'Chaos': 1/33.0, 'Aug': 109, 'Trans': 45, 'Alchemy': 1/4.55, 'Divine': 1/1600.0},
    'Alchemy': {'Exalted': 4.5, 'Chaos': 1/11.5, 'Aug': 580, 'Trans': 50, 'Regal': 6, 'Divine': 1/630},
    'Divine': {'Exalted': 147, 'Chaos': 50,'Aug': 0, 'Trans': 0, 'Regal': 3100, 'Alchemy': 750}
}


# Bellman-Ford algoritması ile döviz arbitrage'ını tespit etme
def find_arbitrage(conversion_rates):
    # Döviz birimleri
    currencies = list(conversion_rates.keys())
    
    # Bellman-Ford algoritmasını uygulamak için mesafe ve önceki düğümleri başlat
    value = {currency: 1 for currency in currencies}  # Başlangıç değerleri 1
    predecessors = {currency: None for currency in currencies}
    
    # Bellman-Ford algoritması - |V| - 1 iterasyon
    for _ in range(len(currencies) - 1):
        for currency in currencies:
            for neighbor, rate in conversion_rates[currency].items():
                
                new_value = value[currency] * rate
                if new_value > value[neighbor]:
                    value[neighbor] = new_value
                    predecessors[neighbor] = currency
    
    # Negatif döngü var mı kontrol et
    arbitrage_path = []
    for currency in currencies:
        for neighbor, rate in conversion_rates[currency].items():
            if value[currency] * rate > value[neighbor]:
                # Negatif döngü bulduğumuzda, yol oluşturma
                # Sadece döngüdeki dövizleri kaydedelim
                arbitrage_path.append(neighbor)
                current_currency = neighbor
                visited = set()  # Döngüyi engellemek için ziyaret edilenleri kontrol et
                while current_currency != currency and current_currency not in visited:
                    visited.add(current_currency)
                    current_currency = predecessors[current_currency]
                    arbitrage_path.append(current_currency)
                arbitrage_path.reverse()  # Yolu tersten düzenleyelim
                return arbitrage_path
    
    return "No arbitrage opportunity found."

# Arbitrage fırsatını bul ve yazdır
arbitrage_path = find_arbitrage(conversion_rates)
print("Arbitrage Path:", arbitrage_path)

# Kazançları değerlendirme (örneğin başlangıç ve bitiş dövizini karşılaştırarak)
def evaluate_arbitrage(conversion_rates, path):
    total_value = 1  # Başlangıç olarak 1 birim değer kabul edelim
    for i in range(len(path) - 1):
        total_value *= conversion_rates[path[i]].get(path[i+1], 0)  # Dönüşüm oranlarını kullanarak değeri güncelle
    return total_value

# Kazancı hesapla
if arbitrage_path != "No arbitrage opportunity found.":
    profit = evaluate_arbitrage(conversion_rates, arbitrage_path)
    if profit > 1:
        print(f"Arbitrage Opportunity Detected! Profit: {profit - 1:.2f}")
    else:
        print("Arbitrage opportunity detected, but no profit!")
else:
    print("No arbitrage opportunity found.")
