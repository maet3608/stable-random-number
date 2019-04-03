# Stable random number generator

Unfortunately the pseudo random number generators in Python do not produce the same 
numbers sequence on Python 2.x versus 3.x. This is sometimes problematic, e.g. unit testing. 
This code provides a stable random number generator that is independent of the Python version.

The code is based on https://en.wikipedia.org/wiki/Mersenne_Twister.
