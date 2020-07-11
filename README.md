# datadockers
Collection of docker files for making data science life easier 

+ ### jupyter-base:
bare-bone jupyter notebook as a base for the stack

+ ### jupyter-minimal 
more customized jupyter notebook with several useful features making it the notebook-to-go
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

+ ### jupyter-plot
jupyter notebook image built on jupyter-minimal with matplotlib and seaborn built-in
    + matplotlib as mpl
    + matplotlib.pyplot as plt
    + seaborn.set() as default

### Run
all docker images are started with
+ `docker run -v $(pwd):/home/martin/work -p 8888:8888 martin37szyska/jupyter-base`
+ copy the http://localhost:8888/?token=<TOKEN> to your browser and off you go


### Source
All imaged are based on Jupyter Docker Stacks with modifications focused on size and simplicity

visit their documentation for more great content
* [Jupyter Docker Stacks on ReadTheDocs](http://jupyter-docker-stacks.readthedocs.io/en/latest/index.html)

Alpine versions are also available based on [alpine-miniconda3](https://hub.docker.com/r/frolvlad/alpine-miniconda3) with even smaller size
+ use the `latest-alpine` tag
