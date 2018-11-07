# Approximate Left Join

This function joins two Pandas DataFrames on two columns whose values do not always overlap. The way they are joined is approximate and is based on the closeness of the values in the columns where the join happens.

The joining is executed by finding the _closest value_ of the joining column of the left DataFrame that _precedes_ the value of the joining column of the right DataFrame.

If the values are the same, the preceding value of the right DataFrame is taken.

## Example

Here is an example where the two following DataFrames are approximately joined over the columns A and D:

Left DataFrame:

|      | A    | B    | C    |
| ---- | ---- | ---- | ---- |
| 0    | 7    | 5    | 1    |
| 1    | 8    | 7    | 8    |
| 2    | 2    | 9    | 7    |

Right DataFrame:

|      | D    | E    |
| ---- | ---- | ---- |
| 0    | 7    | 7    |
| 1    | 9    | 8    |
| 2    | 4    | 2    |

Approximate Left Join DataFrame:

|      | A     | B    | C    | D       | E    |
| ---- | ----- | ---- | ---- | ------- | ---- |
| 0    | **7** | 5    | 1    | **4**   | 2    |
| 1    | **8** | 7    | 8    | **7**   | 7    |
| 2    | **2** | 9    | 7    | **NaN** | NaN  |



Here is a visual representation of the approximate left join:

![](Resources/drawing.png)

## How This is Useful

This may be useful, for example, when joining two time series with non-overlapping times, such that the information of the right series is known before the information of the left time series.

## Usage Example

```python
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
```

