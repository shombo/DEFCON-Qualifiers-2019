#!/usr/bin/env python
from ctypes import *
from multiprocessing import Process, connection, Manager, cpu_count, Event
import sys, logging, os, time
logger = logging.getLogger(__name__)

libpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), './target/release/libproofofwork.so')

def _crack_pow(prefix, libpow, k, thread_id, ret, done):
    logger.debug("%s._crack_pow(%r)", __name__, locals())
    bytes_args = (prefix, "utf-8") if sys.version_info >= (3,0) else (prefix,)
    r = libpow.crack_pow(bytes(*bytes_args),len(prefix),k,thread_id<<k)
    ret[thread_id] = r
    done.set()
    
def solve_pow(prefix, k):
    logger.debug("%s.solve_pow(%r)", __name__, locals())

    libpow = cdll.LoadLibrary(libpath)
    libpow.crack_pow.argtypes = [
        c_char_p, c_size_t, c_ubyte, c_ulonglong
    ]
    
    children = []
    returns = Manager().dict()
    done = Event()

    for pid in range(cpu_count()):
        args = (prefix, libpow, k, pid, returns, done)
        p = Process(target=_crack_pow, args=args)
        logger.debug("Starting thread: _crack_pow%r", args)
        p.start()
        children.append(p)
    start = time.time()
    done.wait()
    logger.debug("Finished after %d seconds", time.time()-start)
    for p in children:
        p.terminate()
    return next(iter(returns.values()))

if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)8s:%(filename)s:%(funcName)s:%(lineno)04d:%(message)s")
    logger.setLevel(logging.DEBUG)
    #test
    logger.info("%016x",solve_pow("e2ZgIzlOpe", 26))
