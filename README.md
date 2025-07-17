# QRNG_eval

`QRNG.py` generates data with different values of $\mu Td$.

`Stat_test` contains results of NIST, Dieharder, AIS-31 and ENT tests for the above data.

`Plot.ipynb` generates the required plots.

In `two_fold`:

    1. `two_fold_data` generates dataset for two-fold test.
    
    2. `two_fold.py`, `dispersion.py`, `comparison.py` perform two-fold method, dispersion method and direct comparison method, respectively and produce results.
    
    3. `two_fold_result.py` prints the results.
    
   4.  `datafile_2fold_0.zip` is the zipped dataset generated from geometric distribution with mean 2.

   6.  `datafile_2fold_1.zip` and `datafile_2fold_2.zip` are the zipped dataset generated from Poisson distribution with mean 0.5 and 10, respectively.
