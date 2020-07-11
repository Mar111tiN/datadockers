from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display
from multiprocessing import Pool, Pipe
import openpyxl
import xlrd
import os
import re
import sys
from datetime import datetime
from os import system as shell
import subprocess
import pandas as pd
import numpy as np


# for Excel support


pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 200)
InteractiveShell.ast_node_interactivity = "all"
