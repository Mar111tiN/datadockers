# Minimal Jupyter Notebook

+ built-ins:
    * pandas as pd
    * numpy as np
    * xlrd and and openpyxl for excel support
+ imports:
    * os, re, sys, datetime
    * Pool, Pipe, subprocess, os.system as shell
+ improved visibility
    * wide-screen mode
    * column limit off
    * colwidth 200


### Based on Jupyter Docker Stacks with modifications focused on size and simplicity

visit their documentation for more great content
* [Jupyter Docker Stacks on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)

An alpine version is also available based on [alpine-miniconda3](https://hub.docker.com/r/frolvlad/alpine-miniconda3) with even smaller size

+ build the alpine version from Dockerfile-alpine