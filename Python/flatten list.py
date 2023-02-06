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

# =============================================================================
# Benchmark using timeit
# =============================================================================

import pandas as pd
import timeit

# # test setup
# test = [[1,2,3], [4,5,6], [7,8,9]]

# func_time = []
# for fun in func_list:
#     print("Method:", fun.__name__)
#     print("Result:", fun(test))
    
#     time = timeit.timeit(
#         "fun(test)",
#         setup = "from __main__ import fun, test",
#         number = 10**6
#     )
    
#     func_time.append(time)
#     print("Time:", time, "\n")

list_size = [2]
while list_size[-1] <= 10**2:
    list_size.append(2**(len(list_size) + 1)) # list of sublist size as squares of 2
    
sublist = [[1,2,3,4,5]] # test sublist
list_df = []
num_exec = 10**6 # number of executions for timeit function

for size in list_size:
    print("Size:", size)
    test = sublist * size # converts test sublist into specified size
    
    func_time = []
    for fun in func_list:
        print(fun.__name__) # function name
        time = timeit.timeit(
            "fun(test)",
            setup = "from __main__ import fun, test",
            number = num_exec
        )
        
        func_time.append(time)
    
    # convert to np array
    res_array = np.array([
        [size] * len(func_list),
        [func_list[i].__name__ for i in range(len(func_list))],
        func_time
    ]).T 
    
    # convert to pd dataframe
    res_df = pd.DataFrame(res_array)
    list_df.append(res_df)
    print("\n")

df = pd.concat(list_df, ignore_index = True)
df.columns = ['input_size', 'method', 'time']
df = df.astype({'input_size': int, 'method': 'category', 'time': float})

from plotnine import *

(ggplot(df)
 + geom_line(aes('input_size', 'time', group = 'method', color = 'method'))
 + labs(x = 'input size', y = 'time (microseconds)') 
)