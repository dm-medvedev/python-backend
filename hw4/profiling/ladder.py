import argparse
import cProfile, pstats, io
from memory_profiler import profile
from contextlib import redirect_stdout
from functools import wraps


PROFILE_PTH = 'profile.txt'


def time_profile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        res = func(*args, **kwargs)
        pr.disable()
        buff = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=buff).sort_stats(sortby)
        ps.print_stats()
        with open(PROFILE_PTH, 'w') as f:
            f.write(buff.getvalue())
        return res
    return wrapper


def mem_profile(func):
    func = profile(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        with open(PROFILE_PTH,'w') as f:
            with redirect_stdout(f):
                res = func(*args, **kwargs)
        return res
    return wrapper


def parse_args():
    parser = argparse.ArgumentParser(description="Climb the ladder!")
    parser.add_argument('-n', required=True, type=int,
                        help='number of ladders')
    parser.add_argument('--non_optimal', action='store_true',
                        help='solve it with not optimal way')
    parser.add_argument('-profile', choices=['memory', 'time'],
                        default=None, help='choose profiler, default'
                        ' is no profiler at all')
    args = parser.parse_args()
    if args.n < 0:
        raise ValueError('number of ladders should be positive!')
    return args


def optimal_step(prev, prevprev):
    return prev + prevprev


def optimal(n: int):
    cnt, prev, prevprev = 0, 1, 0
    for i in range(n):
        cnt = optimal_step(prev, prevprev)
        prevprev, prev = prev, cnt
    return cnt


def non_optimal_step(i, n):
        fin = 0
        for c in f"{i:b}":
            fin+=int(c)+1
            if fin>n:
                break
        cond1 = fin < n and (n-len(f"{i:b}"))>=(n-fin)
        cond2 = fin == n
        return int(cond1 | cond2)


def non_optimal(n: int):
    cnt = 0
    for i in range(2**n):
        # считаем куда приводит такая комбинация 1 и 2
        cnt += non_optimal_step(i, n)
    return cnt


if __name__ == '__main__':
    args = parse_args()
    func = non_optimal if args.non_optimal else optimal
    if args.profile == 'time':
        func = time_profile(func)
    elif args.profile == 'memory':
        func = mem_profile(func)
    print(func(args.n))
