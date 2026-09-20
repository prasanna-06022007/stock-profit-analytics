# 📈 Stock Market Analytics & Profit Optimization System

A beginner-friendly Streamlit web application for analyzing stock market data using classical Design and Analysis of Algorithms (DAA) techniques to identify optimal trading periods.

## Problem Statement

Given a series of daily stock prices, find the best day to buy and the best day to sell (after the buy day) to maximize profit. This is solved using two fundamental algorithmic approaches:

1. **Kadane's Algorithm** - O(n) linear-time solution
2. **Divide-and-Conquer Algorithm** - O(n log n) solution

Both algorithms process the daily price changes and identify the maximum profit that could have been made over any contiguous trading period.

## Objective

The application demonstrates:
- Implementation of two classic DAA algorithms
- Practical application of algorithms to real-world stock data
- Performance comparison between different algorithmic approaches
- Educational value for computer science students

## Features

### Existing Dashboard Features
- 📊 **Load Stock Data**: Import stock price data from CSV files
- 📈 **Price Charts**: Interactive line charts showing stock price trends
- 💹 **Daily Changes**: Calculate and display daily price movements
- 📋 **Data Display**: View detailed stock information and volume data
- 📉 **Statistics**: Get quick insights into price highs, lows, and averages
- 🎯 **Multi-Stock Support**: Analyze multiple stocks simultaneously

### NEW: DAA Algorithm Features
- 🔵 **Kadane's Algorithm**: O(n) maximum subarray solution
- 🟢 **Divide-and-Conquer Algorithm**: O(n log n) maximum subarray solution
- ⏱️ **Execution Time Comparison**: Measure and compare algorithm performance
- 📊 **Algorithm Comparison**: Verify both algorithms produce identical results
- 📈 **Trading Period Visualization**: Highlight the optimal buy/sell dates on a chart
- 💰 **Maximum Profit Calculation**: Shows the best profit possible for the selected stock

## Dataset

The application uses stock market data with the following CSV format:

```
Date,Symbol,Open,High,Low,Close,Volume
2024-01-01,AAPL,150.25,152.50,149.80,151.75,1000000
2024-01-02,AAPL,151.75,153.25,151.00,152.50,950000
```

**Columns:**
- `Date`: Trading date (YYYY-MM-DD)
- `Symbol`: Stock ticker symbol (AAPL, GOOGL, MSFT, TSLA)
- `Open`: Opening price
- `High`: Highest price of the day
- `Low`: Lowest price of the day
- `Close`: Closing price
- `Volume`: Number of shares traded

**Sample Data Included:** AAPL, GOOGL, MSFT, TSLA (January 2024)

## Algorithm Details

### 1. Kadane's Algorithm (O(n))

**Time Complexity:** O(n)  
**Space Complexity:** O(1)

Kadane's algorithm finds the maximum sum of a contiguous subarray in linear time. It maintains:
- `current_sum`: Maximum sum ending at current position
- `max_profit`: Maximum sum seen so far
- `max_start`: Start index of maximum subarray
- `max_end`: End index of maximum subarray

**How it works:**
1. Iterate through daily price changes
2. If `current_sum < 0`, start a new subarray
3. Otherwise, extend the current subarray
4. Update maximum profit and indices whenever a better sum is found

**For stock trading:** The algorithm finds the optimal buy-sell period by treating each daily price change as an array element. The maximum sum represents the maximum profit possible.

```python
def kadane_max_profit(price_changes):
    max_profit = price_changes[0]
    current_sum = price_changes[0]
    max_start = max_end = temp_start = 0
    
    for i in range(1, len(price_changes)):
        if current_sum < 0:
            current_sum = price_changes[i]
            temp_start = i
        else:
            current_sum += price_changes[i]
        
        if current_sum > max_profit:
            max_profit = current_sum
            max_start = temp_start
            max_end = i
    
    return max_profit, max_start, max_end
```

### 2. Divide-and-Conquer Algorithm (O(n log n))

**Time Complexity:** O(n log n)  
**Space Complexity:** O(log n) - recursive call stack

The divide-and-conquer approach solves the maximum subarray problem by:
1. **Divide**: Split the array into two halves
2. **Conquer**: Recursively solve for each half
3. **Combine**: Find the maximum subarray that crosses the midpoint

The maximum of these three cases is the answer.

**Steps:**
1. Base case: If array has one element, return that element
2. Divide array at midpoint
3. Recursively find max subarray in left half
4. Recursively find max subarray in right half
5. Find max subarray crossing the midpoint
6. Return the maximum of the three

**For stock trading:** Same logic as Kadane's, but using a recursive divide-and-conquer strategy.

## Time Complexity Analysis

| Algorithm | Best Case | Average Case | Worst Case | Space |
|-----------|-----------|--------------|-----------|-------|
| **Kadane's** | O(n) | O(n) | O(n) | O(1) |
| **Divide-and-Conquer** | O(n log n) | O(n log n) | O(n log n) | O(log n) |

**Conclusion:** For this problem, Kadane's algorithm is more efficient due to its O(n) linear time complexity. However, both algorithms always produce the same optimal solution.

## Project Structure

```
stock-profit-analytics/
├── app.py                          # Main Streamlit application with DAA algorithms
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore rules
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── data/
    └── sample_stock_data.csv       # Sample stock data
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd stock-profit-analytics
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Local Development
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

### Streamlit Community Cloud
1. Push your code to GitHub
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Click "New app" and select your repository
4. Set the main file to `app.py`
5. Deploy!

## Technologies Used

- **Streamlit**: Web framework for data apps
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **NumPy**: Numerical computations
- **Python Standard Library**: `time` module for performance measurement

*No machine learning, no paid APIs, no unnecessary dependencies.*

## Usage

### General Dashboard
1. Select one or more stock symbols from the sidebar
2. View real-time price metrics in the metrics cards
3. Analyze price trends in the interactive chart
4. Check daily price changes in the data table
5. Review statistics for selected stocks (highs, lows, averages, volume)

### DAA Algorithm Analysis (Single Stock Mode)
1. Select **ONE stock** from the sidebar
2. Scroll to the "Maximum Profit Trading Period Analysis (DAA)" section
3. View results from both algorithms:
   - **Kadane's Algorithm:** Shows O(n) solution
   - **Divide-and-Conquer Algorithm:** Shows O(n log n) solution
4. Compare execution times and results
5. View the highlighted trading period on the chart
6. See the optimal buy and sell dates and prices

## Expected Output

When you select a single stock (e.g., AAPL), the application displays:

```
🎯 Maximum Profit Trading Period Analysis (DAA)
Stock: AAPL

🔵 Kadane's Algorithm (O(n))
  Maximum Profit: $10.50
  Buy Date: 2024-01-01 @ $150.25
  Sell Date: 2024-01-12 @ $160.75
  Trading Period: Day 1 to Day 10
  Execution Time: 0.0015 ms

🟢 Divide-and-Conquer Algorithm (O(n log n))
  Maximum Profit: $10.50
  Buy Date: 2024-01-01 @ $150.25
  Sell Date: 2024-01-12 @ $160.75
  Trading Period: Day 1 to Day 10
  Execution Time: 0.0025 ms

📊 Algorithm Comparison
  Same Maximum Profit?: ✅ YES
  Time Difference: 0.0010 ms
  Faster Algorithm: Kadane
```

**Chart:** Visual representation with green highlighted area showing the optimal trading period, green dot at buy point, red triangle at sell point.

## Educational Value

This project teaches:
- **Data Structures & Algorithms**: Classic maximum subarray problem
- **Algorithm Analysis**: Big-O notation and complexity comparison
- **Divide-and-Conquer**: Recursive algorithm design
- **Dynamic Programming Concepts**: Optimal substructure in Kadane's algorithm
- **Performance Measurement**: Timing and comparing algorithms
- **Real-world Application**: Stock market analysis

## Notes

⚠️ **Disclaimer:** This application is for **educational purposes only**. It demonstrates algorithmic concepts applied to stock data. The historical maximum profit shown is a theoretical calculation based on knowing all future prices. In reality:
- Trading costs and commissions are not included
- You cannot predict future prices
- Past performance does not guarantee future results
- Always conduct thorough research before making any investment decisions

## Limitations

- Uses historical data only (no real-time data)
- Single buy-sell transaction per analysis
- No consideration of trading costs or taxes
- No ML or predictive capabilities
- Limited to CSV data format

## Future Enhancements

- Multiple buy-sell transactions
- Real-time data from APIs
- Portfolio tracking and analysis
- More advanced technical indicators
- Graphical algorithm visualization
- Performance benchmarking on larger datasets

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository.

## Author

Created as an educational project for Stock Market Analytics & Profit Optimization System using Design and Analysis of Algorithms (DAA).
