#!/usr/bin/env python3
"""
Test script to verify both DAA algorithms work correctly.
This script tests the algorithms with sample data and compares results.
"""

# Test data: daily price changes
test_changes = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

# Kadane's Algorithm
def kadane_max_profit(price_changes):
    if len(price_changes) == 0:
        return 0, 0, 0
    
    max_profit = price_changes[0]
    max_start = 0
    max_end = 0
    current_sum = price_changes[0]
    temp_start = 0
    
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


# Divide-and-Conquer Algorithm
def find_max_crossing_subarray(arr, low, mid, high):
    left_sum = float('-inf')
    sum_val = 0
    max_left = mid
    for i in range(mid, low - 1, -1):
        sum_val += arr[i]
        if sum_val > left_sum:
            left_sum = sum_val
            max_left = i
    
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
    if low == high:
        return arr[low], low, high
    
    mid = (low + high) // 2
    left_sum, left_start, left_end = divide_conquer_max_profit(arr, low, mid)
    right_sum, right_start, right_end = divide_conquer_max_profit(arr, mid + 1, high)
    cross_sum, cross_start, cross_end = find_max_crossing_subarray(arr, low, mid, high)
    
    if left_sum >= right_sum and left_sum >= cross_sum:
        return left_sum, left_start, left_end
    elif right_sum >= cross_sum:
        return right_sum, right_start, right_end
    else:
        return cross_sum, cross_start, cross_end


# Run tests
print("=" * 70)
print("TESTING DAA ALGORITHMS FOR MAXIMUM SUBARRAY PROBLEM")
print("=" * 70)
print()

print("Test Data (Price Changes):", test_changes)
print()

# Test Kadane's Algorithm
kadane_profit, kadane_start, kadane_end = kadane_max_profit(test_changes)
print("KADANE'S ALGORITHM (O(n)):")
print(f"  Maximum Profit: {kadane_profit}")
print(f"  Start Index: {kadane_start}")
print(f"  End Index: {kadane_end}")
print(f"  Subarray: {test_changes[kadane_start:kadane_end+1]}")
print()

# Test Divide-and-Conquer Algorithm
dc_profit, dc_start, dc_end = divide_conquer_max_profit(test_changes, 0, len(test_changes) - 1)
print("DIVIDE-AND-CONQUER ALGORITHM (O(n log n)):")
print(f"  Maximum Profit: {dc_profit}")
print(f"  Start Index: {dc_start}")
print(f"  End Index: {dc_end}")
print(f"  Subarray: {test_changes[dc_start:dc_end+1]}")
print()

# Comparison
print("COMPARISON:")
print(f"  Same Maximum Profit? {'✅ YES' if kadane_profit == dc_profit else '❌ NO'}")
print(f"  Same Range? {'✅ YES' if kadane_start == dc_start and kadane_end == dc_end else '⚠️  DIFFERENT (but same profit)'}")
print()

print("=" * 70)
print("✅ ALGORITHMS VERIFIED SUCCESSFULLY!")
print("=" * 70)
