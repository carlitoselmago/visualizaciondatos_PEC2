import pandas as pd
import os
import shutil
import kagglehub

import numpy as np



dest_folder="temp"

def cargar_dataset(archivo,sufijo=''):
    df = pd.read_csv(os.path.join(dest_folder, archivo+sufijo+'.csv'))
    return df