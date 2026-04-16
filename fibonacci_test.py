from fibonacci import fibonacci_up_to

test_cases = [
    (-5, []),
    (0, [0]),
    (1, [0, 1]),
    (10, [0, 1, 1, 2, 3, 5, 8]),
    (100, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]),
]

print("Testing fibonacci_up_to(n):\n")
all_passed = True
for n, expected in test_cases:
    result = fibonacci_up_to(n)
    passed = result == expected
    status = "PASS" if passed else "FAIL"
    if not passed:
        all_passed = False
    print(f"  n={n:>4}  =>  {result}")
    print(f"           expected: {expected}")
    print(f"           [{status}]\n")

print(f"{'All 5 tests passed!' if all_passed else 'Some tests FAILED.'}")
