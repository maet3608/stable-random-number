class StableRandom(random.Random):
    """A pseudo random number generator that is stable across
    Python 2.x and 3.x.
    This class is derived from random.Random and supports all
    methods of the base class.

    >>> rand = StableRandom(0)
    >>> rand.random()
    0.5488135024320365

    >>> rand.randint(1, 10)
    6

    >>> lst = [1, 2, 3, 4, 5]
    >>> rand.shuffle(lst)
    >>> lst
    [1, 3, 2, 5, 4]
    """

    def __init__(self, seed=None):
        """
        Initialize random number generator.

        :param None|int seed: Seed. If None the system time is used.
        """
        self.seed(seed)
        self.index = 624
        self.mt = [0] * 624
        self.mt[0] = self._seed
        for i in range(1, 624):
            self.mt[i] = self._int32(
                1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

    def _int32(self, x):
        """Return the 32 least significant bits"""
        return int(0xFFFFFFFF & x)

    def random(self):
        """Return next random number in [0,1["""
        if self.index >= 624:
            self._twist()

        y = self.mt[self.index]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18

        self.index = self.index + 1

        return float(self._int32(y)) / 0xffffffff

    def _randbelow(self, n, **args):
        """Return a random int in the range [0,n)"""
        return int(self.random() * n)

    def _twist(self):
        """Mersenne Twister"""
        for i in range(624):
            y = self._int32((self.mt[i] & 0x80000000) +
                            (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df
        self.index = 0

    def seed(self, seed=None):
        """
        Set seed.

        :param None|int seed: Seed. If None the system time is used.
        """
        import time
        if seed is None:
            seed = int(time.time() * 256)
        self._seed = seed

    def gauss_next(self):
        """
        Return next gaussian random number.

        :return: Random number sampled from gaussian distribution.
        :rtype: float
        """
        x1, x2 = self.random(), self.random()
        return sqrt(-2.0 * log(x1 + 1e-10)) * cos(2.0 * pi * x2)

    def getstate(self):
        """
        Return state of generator.

        :return: Index and Mersenne Twister array.
        :rtype: tuple
        """
        return self.mt[:], self.index

    def setstate(self, state):
        """
        Set state of generator.

        :param tuple state: State to set as produced by getstate()
        """
        self.mt, self.index = state

    def jumpahead(self, n):
        """
        Set state of generator far away from current state.

        :param int n: Distance to jump.
        """
        self.index += n
        self.random()
