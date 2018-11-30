import numpy as np
import pandas as pd
import sys

#first command line argument (optional) defines how many rows of file
#second command line argument (optional) defines file name
size = int(sys.argv[1]) if len(sys.argv) > 1 else 500
filename = sys.argv[2] if len(sys.argv) > 2 else "test-data-5.csv"

a = np.random.randint(-100, 350, size, "int64")
#a = np.random.logistic(1.7, 3, size)
b = np.random.choice(["a", "b", "c", "d", "e", "f"], size, True, np.random.shuffle([1/21, 2/21, 3/21, 5/21, 6/21, 9/21]))
c = np.random.normal(np.random.uniform(-3, 3), 3, size)
d = np.random.gamma(6, np.random.uniform(1,10), size)
#e = np.random.choice(["alpha", "beta", "gamma", "delta"], size, True, [.4, .3, .2, .1])
#f = np.random.normal(np.random.normal(np.random.uniform(-1, 11), np.random.uniform(6, 25)), np.random.uniform(5, 10), size)

data = pd.DataFrame.from_records(zip(a,b,c,d))
data.to_csv(filename, header=False, index=False)