"""
Path of Exile 2 Trade Bot
------------------------

IMPORTANT DISCLAIMER: This product isn't affiliated with or endorsed by Grinding Gear Games in any way.

This bot is designed for educational purposes only. Users are responsible for ensuring their use
of this software complies with Path of Exile's Terms of Service and trading guidelines.

Path of Exile and Path of Exile 2 are registered trademarks of Grinding Gear Games.
"""

import pandas as pd
import requests
import time
import math
import keyboard
import logging
import json
import os
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tradebot.log'),
        logging.StreamHandler()
    ]
)

class POE2TradeBot:
    def __init__(self):
        self.prices = {}
        self.conversion_rates = {}
        self.last_trade_time = 0
        self.trade_cooldown = 5  # seconds between trades
        self.min_profit_margin = 0.1  # 10% minimum profit margin
        self.temp_data_file = 'temp_market_data.json'
        self.base_url = 'https://www.pathofexile.com/trade2/exchange/poe2/Dawn%20of%20the%20Hunt'
        self.setup_selenium()
        
    def setup_selenium(self):
        """Initialize Selenium WebDriver"""
        try:
            options = webdriver.ChromeOptions()
            
            # Stealth settings
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Additional settings to appear more human-like
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            options.add_argument(f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
            
            # Performance settings
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-infobars')
            
            # Create driver with options
            self.driver = webdriver.Chrome(options=options)
            
            # Execute CDP commands to bypass detection
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            })
            
            # Execute JavaScript to modify navigator properties
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.driver.set_page_load_timeout(30)
            logging.info("Selenium WebDriver initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize Selenium: {str(e)}")
            raise

    def handle_captcha(self):
        """Handle the human verification page"""
        try:
            # Wait for verification to be visible
            wait = WebDriverWait(self.driver, 10)
            verification_text = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Verifying you are human')]"))
            )
            
            if verification_text:
                logging.info("Human verification detected, waiting for manual verification...")
                print("\n=== Human Verification Required ===")
                print("Please complete the verification in the browser window.")
                print("The bot will continue automatically after verification.")
                
                # Wait for verification to complete (wait for trade page to load)
                wait = WebDriverWait(self.driver, 300)  # 5 minute timeout
                wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="search-"]'))
                )
                
                logging.info("Verification completed successfully")
                return True
                
        except TimeoutException:
            # If we don't find verification text, we might already be verified
            return True
        except Exception as e:
            logging.error(f"Error handling verification: {str(e)}")
            return False

    def fetch_market_data(self, mode='buy'):
        """Fetch current market data from POE2 trade site"""
        max_retries = 3
        current_retry = 0
        
        while current_retry < max_retries:
            try:
                # Clear browser data before loading page
                self.driver.delete_all_cookies()
                
                # Add random delay before loading page (1-3 seconds)
                time.sleep(1 + random.random() * 2)
                
                # Load the page
                self.driver.get(self.base_url)
                
                # Handle human verification if needed
                if not self.handle_captcha():
                    raise Exception("Failed to handle human verification")
                
                # Wait for page to be fully loaded
                wait = WebDriverWait(self.driver, 20)
                
                # Add random delay between actions (0.5-1.5 seconds)
                time.sleep(0.5 + random.random())
                
                # Wait for currency section to be visible
                currency_section = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class*="search-"]'))
                )
                
                # Additional random delay
                time.sleep(0.5 + random.random())
                
                market_data = {}
                
                # Get all currency items from both "I Want" and "I Have" sections
                currency_items = self.driver.find_elements(By.CSS_SELECTOR, 'div[class*="currency-"] img')
                
                for item in currency_items:
                    try:
                        # Add random delay between currency checks (0.3-0.8 seconds)
                        time.sleep(0.3 + random.random() * 0.5)
                        
                        currency_name = item.get_attribute('alt')
                        if currency_name:
                            # Move mouse to element before clicking (more human-like)
                            action = webdriver.ActionChains(self.driver)
                            action.move_to_element(item).perform()
                            time.sleep(0.2)  # Short pause after mouse movement
                            item.click()
                            
                            # Random delay after click
                            time.sleep(0.5 + random.random())
                            
                            # Get the exchange rates
                            if mode == 'buy':
                                rate_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div[class*="price-right"]')
                            else:
                                rate_elements = self.driver.find_elements(By.CSS_SELECTOR, 'div[class*="price-left"]')
                            
                            if rate_elements:
                                rate_text = rate_elements[0].text.strip().replace(',', '')
                                try:
                                    rate = float(rate_text)
                                    market_data[currency_name] = {
                                        'price': rate,
                                        'mode': mode
                                    }
                                except ValueError:
                                    logging.warning(f"Could not convert price for {currency_name}: {rate_text}")
                            
                            # Clear the selection with random delay
                            time.sleep(0.2 + random.random() * 0.3)
                            item.click()
                            
                    except Exception as e:
                        logging.warning(f"Error processing currency {currency_name}: {str(e)}")
                        continue
                
                if market_data:
                    self.save_market_data(market_data)
                    logging.info(f"Successfully fetched {mode} mode market data with {len(market_data)} items")
                    return market_data
                else:
                    raise Exception("No market data found in the page")
                
            except Exception as e:
                current_retry += 1
                logging.error(f"Error fetching market data (attempt {current_retry}/{max_retries}): {str(e)}")
                if current_retry < max_retries:
                    # Add longer delay between retries (5-10 seconds)
                    time.sleep(5 + random.random() * 5)
                    try:
                        self.driver.quit()
                        self.setup_selenium()
                    except:
                        pass
                else:
                    cached_data = self.load_market_data()
                    if cached_data:
                        logging.info("Using cached market data")
                        return cached_data
                    return {}
        
        return {}

    def save_market_data(self, data):
        """Save market data to temporary file"""
        try:
            with open(self.temp_data_file, 'w') as f:
                json.dump({
                    'timestamp': datetime.now().isoformat(),
                    'data': data
                }, f)
            logging.info("Market data saved to temporary file")
        except Exception as e:
            logging.error(f"Error saving market data: {str(e)}")

    def load_market_data(self):
        """Load market data from temporary file"""
        try:
            if os.path.exists(self.temp_data_file):
                with open(self.temp_data_file, 'r') as f:
                    data = json.load(f)
                    # Check if data is not too old (e.g., less than 5 minutes)
                    saved_time = datetime.fromisoformat(data['timestamp'])
                    if (datetime.now() - saved_time).total_seconds() < 300:
                        return data['data']
            return {}
        except Exception as e:
            logging.error(f"Error loading market data: {str(e)}")
            return {}

    def update_conversion_rates(self):
        """Update conversion rates based on current market data"""
        try:
            # Fetch both buy and sell data
            print("\n=== Fetching Market Data from POE2 Trade ===")
            print("Fetching buy prices...")
            buy_data = self.fetch_market_data(mode='buy')
            print("Fetching sell prices...")
            sell_data = self.fetch_market_data(mode='sell')
            
            # Calculate conversion rates
            self.conversion_rates = {}
            currencies = set(buy_data.keys()) | set(sell_data.keys())
            
            print("\n=== Current Market Rates ===")
            print("Currency Pair".ljust(30) + "Rate".ljust(10) + "Profit/Loss %")
            print("-" * 50)
            
            for from_curr in currencies:
                self.conversion_rates[from_curr] = {}
                for to_curr in currencies:
                    if from_curr != to_curr:
                        # Calculate conversion rate based on buy/sell prices
                        if from_curr in sell_data and to_curr in buy_data:
                            sell_price = sell_data[from_curr]['price']
                            buy_price = buy_data[to_curr]['price']
                            if sell_price > 0 and buy_price > 0:
                                rate = buy_price / sell_price
                                self.conversion_rates[from_curr][to_curr] = rate
                                
                                # Calculate profit/loss percentage
                                profit_loss = (rate - 1) * 100
                                
                                # Format and print the rate info with colors
                                pair = f"{from_curr} -> {to_curr}".ljust(30)
                                rate_str = f"{rate:.4f}".ljust(10)
                                
                                if profit_loss > 0:
                                    print(f"{pair}{rate_str}\033[92m+{profit_loss:.2f}%\033[0m")  # Green for profit
                                else:
                                    print(f"{pair}{rate_str}\033[91m{profit_loss:.2f}%\033[0m")  # Red for loss
            
            print("\n=== Market Data Update Complete ===")
            logging.info("Conversion rates updated successfully")
        except Exception as e:
            logging.error(f"Error updating conversion rates: {str(e)}")
            print(f"\nError updating conversion rates: {str(e)}")

    def find_arbitrage(self, min_profit=0.1):
        """Find arbitrage opportunities using Bellman-Ford algorithm"""
        currencies = list(self.conversion_rates.keys())
        n = len(currencies)
        currency_index = {currency: i for i, currency in enumerate(currencies)}
        
        graph = [[math.inf] * n for _ in range(n)]
        for source, targets in self.conversion_rates.items():
            for target, rate in targets.items():
                if rate > 0:
                    source_idx = currency_index[source]
                    target_idx = currency_index[target]
                    graph[source_idx][target_idx] = -math.log(rate)

        opportunities = []
        for start in range(n):
            distances = [math.inf] * n
            predecessors = [-1] * n
            distances[start] = 0

            # Run Bellman-Ford
            for _ in range(n - 1):
                for u in range(n):
                    for v in range(n):
                        if graph[u][v] != math.inf and distances[u] + graph[u][v] < distances[v]:
                            distances[v] = distances[u] + graph[u][v]
                            predecessors[v] = u

            # Check for profitable cycles
            for u in range(n):
                for v in range(n):
                    if (graph[u][v] != math.inf and 
                        distances[u] + graph[u][v] < distances[v]):
                        
                        cycle = []
                        visited = set()
                        current = v
                        
                        while current not in visited:
                            visited.add(current)
                            cycle.append(currencies[current])
                            current = predecessors[current]
                        
                        # Calculate profit
                        total_rate = 1.0
                        for i in range(len(cycle)-1):
                            total_rate *= self.conversion_rates[cycle[i]][cycle[i+1]]
                        
                        if total_rate > (1 + min_profit):
                            opportunities.append({
                                'cycle': cycle,
                                'profit': total_rate - 1
                            })

        return opportunities

    def execute_trade(self, item_from, item_to):
        """Execute a trade between two items"""
        current_time = time.time()
        if current_time - self.last_trade_time < self.trade_cooldown:
            time.sleep(self.trade_cooldown - (current_time - self.last_trade_time))

        try:
            # Update market data before executing trade
            self.update_conversion_rates()
            
            # Verify the trade is still profitable
            if item_from in self.conversion_rates and item_to in self.conversion_rates[item_from]:
                rate = self.conversion_rates[item_from][item_to]
                if rate > (1 + self.min_profit_margin):
                    logging.info(f"Executing trade: {item_from} -> {item_to} (Rate: {rate:.4f})")
                    
                    # Navigate to trade page
                    self.driver.get(self.base_url)
                    wait = WebDriverWait(self.driver, 20)
                    
                    # Select the "from" currency in "I Have" section
                    from_currency = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'img[alt="{item_from}"]'))
                    )
                    from_currency.click()
                    
                    # Select the "to" currency in "I Want" section
                    to_currency = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'img[alt="{item_to}"]'))
                    )
                    to_currency.click()
                    
                    # Wait for search results
                    time.sleep(2)
                    
                    # Find the best trade offer
                    trade_buttons = self.driver.find_elements(By.CSS_SELECTOR, '.trade-button')
                    if trade_buttons:
                        # Click the first (best) trade offer
                        trade_buttons[0].click()
                        time.sleep(1)
                        
                        # Here you would implement the actual trade messaging/execution
                        
                        self.last_trade_time = time.time()
                        return True
                    else:
                        logging.warning("No trade offers found")
                        return False
                else:
                    logging.warning(f"Trade no longer profitable: {item_from} -> {item_to}")
                    return False
            else:
                logging.warning(f"Trade pair not available: {item_from} -> {item_to}")
                return False
        except Exception as e:
            logging.error(f"Trade execution failed: {str(e)}")
            return False

    def monitor_trade_chat(self):
        """Monitor trade opportunities"""
        try:
            while True:
                # Update market data
                self.update_conversion_rates()
                
                # Find arbitrage opportunities
                opportunities = self.find_arbitrage(self.min_profit_margin)
                
                if opportunities:
                    for opp in opportunities:
                        logging.info(f"Found opportunity: {opp['cycle']} with {opp['profit']*100:.2f}% profit")
                        
                        # Execute trades in sequence
                        success = True
                        for i in range(len(opp['cycle'])-1):
                            if not self.execute_trade(opp['cycle'][i], opp['cycle'][i+1]):
                                success = False
                                break
                        
                        if success:
                            logging.info(f"Successfully completed trade cycle with {opp['profit']*100:.2f}% profit")
                        else:
                            logging.warning("Trade cycle interrupted due to execution failure")
                
                # Wait before next check
                time.sleep(1)
                
                # Check for exit command
                if keyboard.is_pressed('esc'):
                    logging.info("Exit command received")
                    break
                
        except KeyboardInterrupt:
            logging.info("Bot stopped by user")
        except Exception as e:
            logging.error(f"Error in trade monitoring: {str(e)}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        try:
            self.driver.quit()
            if os.path.exists(self.temp_data_file):
                os.remove(self.temp_data_file)
            logging.info("Cleanup completed successfully")
        except Exception as e:
            logging.error(f"Error during cleanup: {str(e)}")

def main():
    try:
        bot = POE2TradeBot()
        logging.info("Trade bot initialized")
        bot.monitor_trade_chat()
    except Exception as e:
        logging.error(f"Bot crashed: {str(e)}")

if __name__ == "__main__":
    main()
