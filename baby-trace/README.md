# Baby Trace

This problem provides a limited interface to angr running a simple binary, which loads the flag into memory.
The user provides an integer, which, after some comparisons, indexes into the flag, and prints that character.
However, it only does this for < 3, so you cant get the whole flag.
Fortunately for us, there is a small section of code that moves a character into a register, and to another section of the stack.
We can step to this section with angr, symbolify (if that's a word) a variable, and then concrete it. This adds a constraint that
eax is the current value that we loaded from the flag. Since we can see the constaints, we can leak a single byte!
