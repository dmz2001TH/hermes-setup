def fibonacci_up_to(n):
    """Calculate Fibonacci numbers up to n (inclusive).
    
    Args:
        n: Maximum value to include in the sequence.
    
    Returns:
        List of Fibonacci numbers <= n.
    """
    if n < 0:
        return []
    elif n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    
    fib_sequence = [0, 1]
    while True:
        next_fib = fib_sequence[-1] + fib_sequence[-2]
        if next_fib > n:
            break
        fib_sequence.append(next_fib)
    
    return fib_sequence

if __name__ == "__main__":
    import sys
    # Default to n=10 if no argument provided
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    result = fibonacci_up_to(n)
    print(f"Fibonacci numbers up to {n}: {result}")
