# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 06:14:08 2017

@author: jeff
"""
import sys
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    file_in = sys.argv[1]
else:
    file_in = 'test2.txt'
    
base_name = file_in[0:-4]

## set df to maximum region that would ever be used

row_names = map(str, range(250, 750))    # excitation
col_names = map(str, range(250, 750))    # emission

i = 1
n_samples = 1

while i <= n_samples:
    with open(file_in, 'r') as raw_spectra:
        
        print i
        
        use = False
        matrix = pd.DataFrame(columns = col_names, index = row_names, dtype = 'float')
        
        for line in raw_spectra:
            line = line.rstrip()
            
            if line.startswith('EX:'):
                use = True
                line = line.strip('EX: ')
                line = line.split(':EM')
                excite = line[0].rstrip('nm')
                excite = excite.rstrip()
                
            elif use == True:
                if line.startswith('Wavelength'):
                    line = line.split()
                    n_samples = len(line) - 1
                
                elif line.startswith('Results'):
                    use = False
                    break
                
                else:
                    try:
                        line = line.split()
                        emit = line[0]
                        abund = line[i]
                        emit = emit.rstrip()
                        abund = abund.rstrip()
                        
                        if abund == 'OVRFLW':
                            abund = np.nan
                            
                        matrix.loc[emit, excite] = abund
                        print i, excite, emit, abund
                    except IndexError:
                        continue
                
    ## no idea why this is necessary!!
                    
    matrix = matrix[matrix.columns].astype(float)
                    
    ## write dataframe to csv file
                    
    matrix.to_csv(base_name + '_' + str(i) + '.csv')
    
    ## generate a figure
    
    fig = sb.heatmap(matrix, xticklabels = 100, yticklabels = 100, cmap="YlGnBu")
    fig.set(ylabel = 'Emission', xlabel = 'Excitation')
    fig.invert_yaxis()
    fig.get_figure().savefig(base_name + '_' + str(i) + '.png')
    plt.close()
    
    i = i + 1