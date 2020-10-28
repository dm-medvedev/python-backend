import argparse
import cProfile, pstats, io


def parse_args():
    parser = argparse.ArgumentParser(description="Climb the ladder!")
    parser.add_argument('-n', required=True, type=int,
                        help='number of ladders')
    parser.add_argument('--non_optimal', action='store_true',
                        help='solve it with not optimal way')
    parser.add_argument('--profile', action='store_true',
                        help='turn on profiler')
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
    if args.profile:
        pr = cProfile.Profile()
        pr.enable()
    if args.non_optimal:
        print(non_optimal(args.n))
    else:
        print(optimal(args.n))
    if args.profile:
        pr.disable()
        buff = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=buff).sort_stats(sortby)
        ps.print_stats()
        with open('profile.txt', 'w') as f:
            f.write(buff.getvalue())
