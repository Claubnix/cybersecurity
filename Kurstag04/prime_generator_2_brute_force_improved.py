import math


def brute_force_improved(limit=1000000000):
    """
    Returns a list of prime numbers below the number "limit"
    """
    primes = []
    if limit >= 2:
        primes.append(2)
    for pruefzahl in range(3, limit+1, 2):
        prime = True
        for divident in range(3, math.floor(math.sqrt(pruefzahl))+1):
            if pruefzahl % divident == 0:
                prime = False
        if prime:
            primes.append(pruefzahl)
    return primes


def main():
    assert (brute_force_improved(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                                          73, 79, 83, 89, 97])
    print(brute_force_improved())


# Driver code
if __name__ == '__main__':
    main()
