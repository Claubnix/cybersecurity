def sieve_of_eratosthenes(limit=100000000):
    """
    Returns a list of prime numbers below the number "limit"
    """
    is_prime = dict([(i, True) for i in range(limit + 1)])
    p = 2
    while p * p <= limit:
        # If prime[p] is not changed, then it is a prime
        if is_prime[p]:

            # Update all multiples of p
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
        p += 1

    # Create a list with all calculated prime numbers
    primes = []
    for i in range(limit + 1):
        if i in [0, 1]:
            pass
        elif is_prime[i]:
            primes.append(i)
        else:
            pass
    return primes


def main():
    assert (sieve_of_eratosthenes(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                                           73, 79, 83, 89, 97])
    print(sieve_of_eratosthenes())


# Driver code
if __name__ == '__main__':
    main()
