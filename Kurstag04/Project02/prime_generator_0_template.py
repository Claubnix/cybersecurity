def algorithm(limit=1000):
    """
    Returns a list of prime numbers below the number "limit"
    """
    primes = []
    for pruefzahl in range(2, limit+1):
        prime = True
        # Check if pruefzahl is prime
        for i in range(2, int(pruefzahl ** 0.5) + 1):
            if pruefzahl % i == 0:
                prime = False
                break
        if prime:
            primes.append(pruefzahl)
    return primes

def main():
    assert (algorithm(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                              73, 79, 83, 89, 97])
    print(algorithm())

# Driver code
if __name__ == '__main__':
    main()
