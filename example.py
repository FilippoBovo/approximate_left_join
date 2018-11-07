import numpy as np
import pandas as pd
from approx_left_join import approx_left_join

# Create data

np.random.seed(4)

left = pd.DataFrame(np.random.randint(0, 10, size=(3, 3)),
                    columns=['A', 'B', 'C'])

right = pd.DataFrame(np.random.randint(0, 10, size=(3, 2)),
                     columns=['D', 'E'])

# Approximate left join

print(approx_left_join(left, right, 'A', 'D'))
