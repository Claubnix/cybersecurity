import math


def sieve_of_atkin(limit=100000):
    """
    Returns a list of prime numbers below the number "limit"
    """
    is_prime = dict([(i, False) for i in range(5, limit+1)])
    for x in range(1, int(math.sqrt(limit))+1):
        for y in range(1, int(math.sqrt(limit))+1):
            n = 4*x**2 + y**2
            if (n <= limit) and ((n % 12 == 1) or (n % 12 == 5)):
                is_prime[n] = not is_prime[n]
            n = 3*x**2 + y**2
            if (n <= limit) and (n % 12 == 7):
                is_prime[n] = not is_prime[n]
            n = 3*x**2 - y**2
            if (x > y) and (n <= limit) and (n % 12 == 11):
                is_prime[n] = not is_prime[n]
    for n in range(5, int(math.sqrt(limit))+1):
        if is_prime[n]:
            ik = 1
            while ik * n**2 <= limit:
                is_prime[ik * n**2] = False
                ik += 1

    # Create a list with all calculated prime numbers
    primes = []
    for i in range(limit + 1):
        if i in [0, 1, 4]:
            pass
        elif i in [2, 3] or is_prime[i]:
            primes.append(i)
        else:
            pass

    return primes


def main():
    assert (sieve_of_atkin(100) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
                                    73, 79, 83, 89, 97])
    print(sieve_of_atkin())


# Driver code
if __name__ == '__main__':
    main()
