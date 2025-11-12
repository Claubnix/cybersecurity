def fibonacci_sequence(limit=1000):
    fibonacci = []
    a = 0
    b = 1
    for i in range(limit):
        fibonacci.append(b)
        a, b = b, a + b
    return fibonacci


def main():
    print(fibonacci_sequence())


# Driver code
if __name__ == '__main__':
    main()
