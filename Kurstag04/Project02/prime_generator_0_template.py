def algorithm(limit=1000):
    """
    Returns a list of prime numbers below the number "limit"
    """
    primes = []
    for pruefzahl in range(<insert start), <insert stop>):
        prime = True
        <do something>
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
