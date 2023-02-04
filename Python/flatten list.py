import numpy as np
import functools
import itertools
import operator

def nested_loops(x):
    result = []
    for sublist in x:
        for item in sublist:
            result.append(item)
    return result

def list_comp(x):
    return [item for sublist in x for item in sublist]

def reduce_concat(x):
    return functools.reduce(operator.concat, x)

def reduce_iconcat(x):
    return functools.reduce(operator.iconcat, x, [])

def np_concat(x):
    return list(np.concatenate(x))

def np_flat(x):
    return list(np.array(x).flat)

def chain_method(x):
    return list(itertools.chain(*x))

def chain_iterable(x):
    return list(itertools.chain.from_iterable(x))

def sum_brackets(x):
    return sum(x, [])

def extend_method(x):
    result = []
    for sublist in x:
        result.extend(sublist)
    return result

func_list = [nested_loops, 
             list_comp, 
             reduce_concat, 
             reduce_iconcat,
             np_concat,
             np_flat,
             chain_method,
             chain_iterable,
             sum_brackets,
             extend_method]

# =============================================================================
# Benchmark using perfplot
# =============================================================================

import perfplot

plot_bench = perfplot.bench(
    setup = lambda n: [list(range(10))] * n, # generate input data
    kernels = func_list,
    n_range = [2**k for k in range(16)],
    labels = [func_list[i].__name__ for i in range(len(func_list))],
    xlabel = 'Input Size'
)

plot_bench.show()
plot_bench.save('flatten list.png', transparent = True)