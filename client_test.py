import unittest
from client3 import getDataPoint
from client3 import getRatio  # Make sure getRatio is imported


class ClientTest(unittest.TestCase):
    def test_getDataPoint_calculatePrice(self):
        quotes = [
            {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            expected_price = (bid_price + ask_price) / 2
            self.assertEqual(price, expected_price)

    def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
        quotes = [
            {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
            {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
        ]
        for quote in quotes:
            stock, bid_price, ask_price, price = getDataPoint(quote)
            expected_price = (bid_price + ask_price) / 2
            self.assertEqual(price, expected_price)
            
    def test_getDataPoint_bidEqualsAsk(self):
        quote = {'top_ask': {'price': 120.0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        stock, bid_price, ask_price, price = getDataPoint(quote)
        self.assertEqual(price, 120.0)

    def test_getDataPoint_negativePrices(self):
        quote = {'top_ask': {'price': -100.0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': -50.0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        stock, bid_price, ask_price, price = getDataPoint(quote)
        self.assertEqual(price, -75.0)
    def test_getDataPoint_missingBidPrice(self):
        quote = {'top_ask': {'price': 121.0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': None, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        stock, bid_price, ask_price, price = getDataPoint(quote)
        expected_price = ask_price  # Since bid_price is missing
        self.assertEqual(price, expected_price)

    def test_getDataPoint_missingAskPrice(self):
        quote = {'top_ask': {'price': None, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        stock, bid_price, ask_price, price = getDataPoint(quote)
        expected_price = bid_price  # Since ask_price is missing
        self.assertEqual(price, expected_price)
        
    def test_getDataPoint_missingBothPrices(self):
        quote = {'top_ask': {'price': None, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': None, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        stock, bid_price, ask_price, price = getDataPoint(quote)
        self.assertIsNone(price)  # Since both bid and ask prices are missing
        
    def test_getDataPoint_smallBidAskDifference(self):
        quote = {'top_ask': {'price': 120.01, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.00, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        stock, bid_price, ask_price, price = getDataPoint(quote)
        expected_price = (bid_price + ask_price) / 2
        self.assertAlmostEqual(price, expected_price, places=4)  # Precision for small differences
        
    def test_getDataPoint_largeNumbers(self):
        quote = {'top_ask': {'price': 1000000000.0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 999999999.0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        stock, bid_price, ask_price, price = getDataPoint(quote)
        expected_price = (bid_price + ask_price) / 2
        self.assertEqual(price, expected_price)
        
    def test_getDataPoint_zeroPrices(self):
        quote = {'top_ask': {'price': 0.0, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 0.0, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'}
        stock, bid_price, ask_price, price = getDataPoint(quote)
        self.assertEqual(price, 0.0)  # Price should be zero
    
    def test_getRatio_zeroPriceB(self):
        price_a = 120.0
        price_b = 0.0
        self.assertIsNone(getRatio(price_a, price_b))  # Should return None to avoid division by zero
        
    def test_getRatio_equalPrices(self):
          
        price_a = 120.0
        price_b = 120.0
        expected_ratio = 1.0
        self.assertEqual(getRatio(price_a, price_b), expected_ratio)
      
    def test_getRatio_largeNumbers(self):
        price_a = 1000000000.0
        price_b = 500000000.0
        expected_ratio = 2.0
        self.assertEqual(getRatio(price_a, price_b), expected_ratio)

    def test_getRatio_smallDecimals(self):
        price_a = 0.0001
        price_b = 0.00005
        expected_ratio = 2.0
        self.assertEqual(getRatio(price_a, price_b), expected_ratio)

    
    









      



if __name__ == '__main__':
    unittest.main()
