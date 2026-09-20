import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import time

st.set_page_config(page_title="Stock Market Analytics", layout="wide")

st.title("📈 Stock Market Analytics Dashboard")
st.markdown("Analyze stock prices with DAA algorithms for optimal trading periods")

@st.cache_data
def load_data(file_path):
    """Load stock data from CSV file"""
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date')


# ==============================================================================
# ALGORITHM 1: KADANE'S MAXIMUM SUBARRAY ALGORITHM
# ==============================================================================
# Time Complexity: O(n)
# Space Complexity: O(1)
# 
# Kadane's algorithm finds the maximum sum of a contiguous subarray in linear time.
# It works by maintaining the maximum sum ending at the current position and the
# overall maximum sum seen so far.
# 
# For stock trading: finds the best buy-sell period with maximum profit using
# daily price changes as the input array.
# ==============================================================================

def kadane_max_profit(price_changes):
    """
    Kadane's Algorithm for Maximum Subarray Sum.
    
    Args:
        price_changes: List of daily price changes
        
    Returns:
        Tuple of (max_profit, start_index, end_index)
    """
    if len(price_changes) == 0:
        return 0, 0, 0
    
    max_profit = price_changes[0]
    max_start = 0
    max_end = 0
    current_sum = price_changes[0]
    temp_start = 0
    
    for i in range(1, len(price_changes)):
        # If starting a new subarray gives better result than extending
        if current_sum < 0:
            current_sum = price_changes[i]
            temp_start = i
        else:
            current_sum += price_changes[i]
        
        # Update maximum profit and its indices
        if current_sum > max_profit:
            max_profit = current_sum
            max_start = temp_start
            max_end = i
    
    return max_profit, max_start, max_end


# ==============================================================================
# ALGORITHM 2: DIVIDE-AND-CONQUER MAXIMUM SUBARRAY ALGORITHM
# ==============================================================================
# Time Complexity: O(n log n)
# Space Complexity: O(log n) due to recursion stack
#
# This algorithm divides the array into two halves, recursively finds the
# maximum subarray in each half, and also finds the maximum subarray that
# crosses the midpoint. Then it returns the maximum of these three.
#
# For stock trading: finds the best buy-sell period with maximum profit by
# dividing and conquering the daily price changes array.
# ==============================================================================

def find_max_crossing_subarray(arr, low, mid, high):
    """
    Find the maximum subarray that crosses the midpoint.
    
    Args:
        arr: Array of price changes
        low: Lower index
        mid: Midpoint index
        high: Upper index
        
    Returns:
        Tuple of (max_sum, left_index, right_index)
    """
    # Find maximum sum on the left side including mid
    left_sum = float('-inf')
    sum_val = 0
    max_left = mid
    for i in range(mid, low - 1, -1):
        sum_val += arr[i]
        if sum_val > left_sum:
            left_sum = sum_val
            max_left = i
    
    # Find maximum sum on the right side including mid + 1
    right_sum = float('-inf')
    sum_val = 0
    max_right = mid + 1
    for i in range(mid + 1, high + 1):
        sum_val += arr[i]
        if sum_val > right_sum:
            right_sum = sum_val
            max_right = i
    
    return left_sum + right_sum, max_left, max_right


def divide_conquer_max_profit(arr, low, high):
    """
    Divide and Conquer Algorithm for Maximum Subarray Sum.
    
    Args:
        arr: Array of price changes
        low: Lower index
        high: Upper index
        
    Returns:
        Tuple of (max_profit, start_index, end_index)
    """
    if low == high:
        return arr[low], low, high
    
    mid = (low + high) // 2
    
    # Recursively find max subarray in left half
    left_sum, left_start, left_end = divide_conquer_max_profit(arr, low, mid)
    
    # Recursively find max subarray in right half
    right_sum, right_start, right_end = divide_conquer_max_profit(arr, mid + 1, high)
    
    # Find max subarray crossing the midpoint
    cross_sum, cross_start, cross_end = find_max_crossing_subarray(arr, low, mid, high)
    
    # Return the maximum of the three
    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_sum, left_start, left_end
    elif right_sum >= cross_sum:
        return right_sum, right_start, right_end
    else:
        return cross_sum, cross_start, cross_end


file_path = Path("data/sample_stock_data.csv")

if file_path.exists():
    df = load_data(file_path)
    
    st.sidebar.header("📊 Dashboard Controls")
    
    stock_symbols = sorted(df['Symbol'].unique())
    selected_symbols = st.sidebar.multiselect(
        "Select Stock Symbol(s)",
        options=stock_symbols,
        default=[stock_symbols[0]] if stock_symbols else []
    )
    
    if selected_symbols:
        filtered_df = df[df['Symbol'].isin(selected_symbols)].copy()
        
        # ====================================================================
        # EXISTING DASHBOARD FEATURES (PRESERVED)
        # ====================================================================
        
        st.subheader("📋 Stock Price Data")
        col1, col2, col3, col4 = st.columns(4)
        
        for i, symbol in enumerate(selected_symbols):
            symbol_data = filtered_df[filtered_df['Symbol'] == symbol]
            if not symbol_data.empty:
                latest_close = symbol_data['Close'].iloc[-1]
                latest_open = symbol_data['Open'].iloc[-1]
                price_change = latest_close - latest_open
                
                with col1 if i % 4 == 0 else col2 if i % 4 == 1 else col3 if i % 4 == 2 else col4:
                    st.metric(
                        label=f"{symbol}",
                        value=f"${latest_close:.2f}",
                        delta=f"${price_change:.2f}" if price_change != 0 else "No change",
                        delta_color="normal"
                    )
        
        st.subheader("📈 Stock Price Trend")
        fig, ax = plt.subplots(figsize=(12, 6))
        
        for symbol in selected_symbols:
            symbol_data = filtered_df[filtered_df['Symbol'] == symbol]
            ax.plot(symbol_data['Date'], symbol_data['Close'], 
                   marker='o', label=symbol, linewidth=2, markersize=4)
        
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price ($)", fontsize=12)
        ax.set_title("Stock Closing Prices Over Time", fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        st.pyplot(fig)
        
        st.subheader("📊 Daily Price Changes")
        display_df = filtered_df[['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
        display_df['Daily Change ($)'] = display_df['Close'] - display_df['Open']
        display_df['Daily Change (%)'] = ((display_df['Close'] - display_df['Open']) / display_df['Open'] * 100).round(2)
        display_df = display_df.sort_values('Date', ascending=False)
        
        st.dataframe(display_df, use_container_width=True)
        
        st.subheader("📈 Statistics")
        
        stats_col1, stats_col2 = st.columns(2)
        
        with stats_col1:
            st.write("**Price Statistics**")
            for symbol in selected_symbols:
                symbol_data = filtered_df[filtered_df['Symbol'] == symbol]
                if not symbol_data.empty:
                    st.write(f"**{symbol}**")
                    st.write(f"  • Highest Price: ${symbol_data['High'].max():.2f}")
                    st.write(f"  • Lowest Price: ${symbol_data['Low'].min():.2f}")
                    st.write(f"  • Average Price: ${symbol_data['Close'].mean():.2f}")
        
        with stats_col2:
            st.write("**Volume & Change**")
            for symbol in selected_symbols:
                symbol_data = filtered_df[filtered_df['Symbol'] == symbol]
                if not symbol_data.empty:
                    avg_volume = symbol_data['Volume'].mean()
                    total_change = symbol_data['Close'].iloc[-1] - symbol_data['Close'].iloc[0]
                    pct_change = (total_change / symbol_data['Close'].iloc[0] * 100) if symbol_data['Close'].iloc[0] != 0 else 0
                    
                    st.write(f"**{symbol}**")
                    st.write(f"  • Avg Volume: {avg_volume:,.0f}")
                    st.write(f"  • Period Change: ${total_change:.2f} ({pct_change:.2f}%)")
        
        # ====================================================================
        # NEW: DAA MAXIMUM PROFIT ANALYSIS (SINGLE STOCK SELECTED)
        # ====================================================================
        
        if len(selected_symbols) == 1:
            st.divider()
            st.subheader("🎯 Maximum Profit Trading Period Analysis (DAA)")
            
            symbol = selected_symbols[0]
            symbol_data = filtered_df[filtered_df['Symbol'] == symbol].sort_values('Date').reset_index(drop=True)
            
            # Calculate daily price changes (buy-sell differences)
            daily_changes = (symbol_data['Close'].diff()).dropna().values.tolist()
            
            if len(daily_changes) > 0:
                # Run Kadane's Algorithm
                start_kadane = time.time()
                kadane_profit, kadane_start, kadane_end = kadane_max_profit(daily_changes)
                time_kadane = (time.time() - start_kadane) * 1000  # Convert to milliseconds
                
                # Adjust indices (since we used diff, the actual buy date is index+1)
                kadane_start_adj = kadane_start + 1
                kadane_end_adj = kadane_end + 1
                
                # Run Divide-and-Conquer Algorithm
                start_dc = time.time()
                dc_profit, dc_start, dc_end = divide_conquer_max_profit(daily_changes, 0, len(daily_changes) - 1)
                time_dc = (time.time() - start_dc) * 1000  # Convert to milliseconds
                
                # Adjust indices
                dc_start_adj = dc_start + 1
                dc_end_adj = dc_end + 1
                
                # Get dates for best trading period (Kadane's)
                kadane_buy_date = symbol_data.iloc[kadane_start_adj]['Date'].strftime('%Y-%m-%d')
                kadane_sell_date = symbol_data.iloc[kadane_end_adj]['Date'].strftime('%Y-%m-%d')
                kadane_buy_price = symbol_data.iloc[kadane_start_adj]['Open']
                kadane_sell_price = symbol_data.iloc[kadane_end_adj]['Close']
                
                # Get dates for best trading period (Divide-and-Conquer)
                dc_buy_date = symbol_data.iloc[dc_start_adj]['Date'].strftime('%Y-%m-%d')
                dc_sell_date = symbol_data.iloc[dc_end_adj]['Date'].strftime('%Y-%m-%d')
                dc_buy_price = symbol_data.iloc[dc_start_adj]['Open']
                dc_sell_price = symbol_data.iloc[dc_end_adj]['Close']
                
                # Display Algorithm Results Side-by-Side
                st.write(f"**Stock: {symbol}**")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🔵 Kadane's Algorithm (O(n))")
                    st.metric("Maximum Profit", f"${kadane_profit:.2f}")
                    st.write(f"**Buy Date:** {kadane_buy_date} @ ${kadane_buy_price:.2f}")
                    st.write(f"**Sell Date:** {kadane_sell_date} @ ${kadane_sell_price:.2f}")
                    st.write(f"**Trading Period:** Day {kadane_start_adj} to Day {kadane_end_adj}")
                    st.write(f"**Execution Time:** {time_kadane:.4f} ms")
                
                with col2:
                    st.markdown("### 🟢 Divide-and-Conquer Algorithm (O(n log n))")
                    st.metric("Maximum Profit", f"${dc_profit:.2f}")
                    st.write(f"**Buy Date:** {dc_buy_date} @ ${dc_buy_price:.2f}")
                    st.write(f"**Sell Date:** {dc_sell_date} @ ${dc_sell_price:.2f}")
                    st.write(f"**Trading Period:** Day {dc_start_adj} to Day {dc_end_adj}")
                    st.write(f"**Execution Time:** {time_dc:.4f} ms")
                
                # Algorithm Comparison
                st.markdown("### 📊 Algorithm Comparison")
                
                comp_col1, comp_col2, comp_col3 = st.columns(3)
                
                with comp_col1:
                    match = "✅ YES" if abs(kadane_profit - dc_profit) < 0.01 else "❌ NO"
                    st.metric("Same Maximum Profit?", match)
                
                with comp_col2:
                    time_diff = abs(time_kadane - time_dc)
                    st.metric("Time Difference", f"{time_diff:.4f} ms")
                
                with comp_col3:
                    faster = "Kadane" if time_kadane < time_dc else "Divide-and-Conquer" if time_dc < time_kadane else "Equal"
                    st.metric("Faster Algorithm", faster)
                
                # Visualization: Highlight Best Trading Period
                st.markdown("### 📈 Best Trading Period (Kadane's Algorithm)")
                
                fig, ax = plt.subplots(figsize=(12, 6))
                
                # Plot the full price trend
                ax.plot(symbol_data.index, symbol_data['Close'], 
                       marker='o', label='Close Price', linewidth=2, markersize=6, color='steelblue')
                
                # Highlight the best trading period
                best_period_data = symbol_data.iloc[kadane_start_adj:kadane_end_adj+1]
                ax.fill_between(best_period_data.index, best_period_data['Close'].min() * 0.95, 
                               best_period_data['Close'].max() * 1.05, 
                               alpha=0.3, color='green', label='Best Trading Period')
                
                # Mark buy and sell points
                ax.plot(kadane_start_adj, kadane_buy_price, 'go', markersize=12, label='Buy Point', zorder=5)
                ax.plot(kadane_end_adj, kadane_sell_price, 'r^', markersize=12, label='Sell Point', zorder=5)
                
                # Add annotation arrows
                ax.annotate('BUY', xy=(kadane_start_adj, kadane_buy_price), 
                           xytext=(kadane_start_adj, kadane_buy_price * 0.95),
                           fontsize=11, fontweight='bold', color='green',
                           ha='center', arrowprops=dict(arrowstyle='->', color='green', lw=2))
                ax.annotate('SELL', xy=(kadane_end_adj, kadane_sell_price), 
                           xytext=(kadane_end_adj, kadane_sell_price * 1.05),
                           fontsize=11, fontweight='bold', color='red',
                           ha='center', arrowprops=dict(arrowstyle='->', color='red', lw=2))
                
                ax.set_xlabel("Day Index", fontsize=12)
                ax.set_ylabel("Price ($)", fontsize=12)
                ax.set_title(f"Maximum Profit Trading Period for {symbol} (Profit: ${kadane_profit:.2f})", 
                           fontsize=14, fontweight='bold')
                ax.legend(loc='best', fontsize=10)
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                
                st.pyplot(fig)
                
                # Information Box
                st.info(f"💡 **Insight:** The best trading period for {symbol} is from {kadane_buy_date} to {kadane_sell_date}, with a maximum profit of ${kadane_profit:.2f}. Both algorithms identify the same optimal solution.")
            else:
                st.warning("Not enough data to calculate price changes.")
        else:
            st.info("📌 Select only ONE stock to see the Maximum Profit Analysis (DAA algorithms).")
        
        st.divider()
        st.info("💡 This dashboard displays historical stock data. Always do your own research before making investment decisions.")
        
    else:
        st.warning("Please select at least one stock symbol from the sidebar.")
else:
    st.error(f"Data file not found at {file_path}")
    st.info("Please ensure the 'data/sample_stock_data.csv' file exists in the project directory.")
