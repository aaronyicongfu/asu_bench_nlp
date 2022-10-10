# Visualization of the AMPL-NLP Benchmark Results
This repository contains the raw log files and scripts to visualize the
nonlinear programming [AMPL-NLP benchmark](http://plato.asu.edu/ftp/ampl-nlp).

## Version of the benchmark used
01-18-2022

## Command I used to download all log files
```
lftp -c 'mirror --parallel=100 http://plato.asu.edu/ftp/ampl-nlp_logs/ ;exit'
```