## Estimated Parameters

These values were produced by running:

- `python solution.py`

## Note on the reported L1 error
The assignment’s model uses parameter values across a time interval **t ∈ [6, 60]**.
Since the CSV (`xy_data.csv`) does not include explicit `t` values, the script does **nearest-point matching**:
- it generates a dense curve using `t ∈ [6, 60]`
- for each CSV point, it matches to the closest generated curve point
- then it computes the reported **mean L1 distance** in `(x,y)` coordinates

So the reported error reflects correspondence via geometric nearest points, not index-to-index ordering.


- θ (deg): 29.999535
- M: 0.030001
- X: 54.998681
- mean L1 (nearest-point matching): 0.013359


