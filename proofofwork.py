#!/usr/bin/env python
from ctypes import *
from multiprocessing import Process, connection, Manager, cpu_count, Event
import sys, logging, os, time
logger = logging.getLogger(__name__)

#location to load shared object
libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), './target/release/libproofofwork.so')

def _wrap_crack_pow(prefix, libpow, k, thread_id, ret, done):
    logger.debug("%s._crack_pow(%r)", __name__, locals())
    #python3 handles bytes weird
    bytes_args = (prefix, "utf-8") if sys.version_info >= (3,0) else (prefix,)
    #run the foreign library
    #assumptions: 
    # - the starting location (thread_id<<k) is still in 64bits
    # - the prefix is utf-8 encoded and not wide-chars or something like that
    r = libpow.crack_pow(bytes(*bytes_args),len(prefix),k,thread_id<<k)
    #fill the return dictionary
    ret[thread_id] = r
    #notify the main thread we're complete
    done.set()
    
def solve_pow(prefix, k):
    logger.debug("%s.solve_pow(%r)", __name__, locals())
    #load libproofofwork
    libpow = cdll.LoadLibrary(libpath)
    #specify the input arguments
    libpow.crack_pow.argtypes = [
        c_char_p, c_size_t, c_ubyte, c_ulonglong
    ]
    #and the return type
    libpow.restype = c_ulonglong
    #location to remember each process
    children = []
    #setup a thread-safe return dictionary
    returns = Manager().dict()
    #How a thread will notify when complete
    done = Event()
    #Number of cpu many threads
    for pid in range(cpu_count()):
        #create a process
        args = (prefix, libpow, k, pid, returns, done)
        p = Process(target=_wrap_crack_pow, args=args)
        logger.debug("Starting thread: _crack_pow%r", args)
        p.start()
        #keep track of the process object
        children.append(p)
    #wait for a process to finish
    logger.debug("Waiting on children.")
    start = time.time()
    done.wait()
    logger.debug("Finished after %d seconds", time.time()-start)
    #kill all the children
    for p in children:
        p.terminate()
    #return any of the completed values
    return next(iter(returns.values()))

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)8s:%(filename)s:%(funcName)s:%(lineno)04d:%(message)s")
    logger.setLevel(logging.DEBUG)
    #test
    logger.info("%016x",solve_pow("e2ZgIzlOpe", 26))
