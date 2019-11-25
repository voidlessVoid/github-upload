#!/usr/bin/env python

import os
import time
import pandas as pd
import numpy as np
import math
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
directory_1 = os.path.dirname(os.path.abspath(__file__))+'/'
'''
seaborn breaks tkinter...why?
'''

#in_path = '/Users/mbohnke/Documents/PhD/1_data/Neptune_MB/Sr_NBS987-5ppb_samples_20190628-112212/'
#out_path = '/Users/mbohnke/Documents/'
#last_opz = '063'

def nep_processing(in_filepath,out_filepath, l_opz, element):


    path = in_filepath
    exp_files = []
    exp_files_S = []

    cols = ['Cycle','Time','82Kr','83Kr','84Sr','85Rb','86Sr','87Sr','88Sr']
    cols2 = ['Cycle',	'Time',	'82Kr',	'83Kr',	'84Sr',	'85Rb',	'86Sr'	,'87Sr'	,'88Sr'	,'84Sr/86Sr (1)'	,'87Sr/86Sr (2)'	,'88Sr/86Sr (3)'	,'88Sr/86Sr (4)'	,'87Sr/86Sr (5)',	'84Sr/86Sr (6)']
    cols_S = ['***','Cup', 'L3', 'C', 'H3', 'H3 | L3', 'C | L3', 'H3 | L3.1', 'C | L3.1', 'H3 | C', 'L3 | H3', 'L3 | C', 'Run_num', 'ID','number', 'Unnamed: 12']
    sulphur = False
    last_opz = l_opz
    exact_33_mass = None



    '''
    sulphur processing
    '''

    if element == 'S':
        #get all exp files in path given by GUI
        for file in os.listdir(path):
            try:
                if file.endswith('.exp'):
                    exp_files_S.append(str(file))
            except:
                print('no files found')
        #sort exp files and divide in opz and standard/sample lists
        exp_files_S = sorted(exp_files_S)
        opz_files_S = [x for x in exp_files_S if 'OPZ' in x and last_opz not in x]  # kick out last opz exp file
        opz_volts_S = pd.DataFrame()
        opz_volts_S['count'] = None

        sample_std_S_files = [x for x in exp_files_S if x not in opz_files_S and last_opz not in x]
        sample_std_S_volts = pd.DataFrame()
        sample_std_S_volts_odd = pd.DataFrame()
        sample_std_S_volts_even = pd.DataFrame()

        counter_opz = 1
        counter_sample_std = 0

        for i in sample_std_S_files:
            counter_sample_std += 1
            df2 = pd.read_csv(path + i, delimiter="\t")
            Run_num1 = df2.iloc[5,0]
            Run_num2 = [int(x) for x in Run_num1.split() if x.isdigit()]
            #get row number of 'Cup' to skiprows from there
            skip = np.where(df2['Unnamed: 1']=='Cup')
            df = pd.read_csv(path+i, skiprows = int(skip[0])+1, delimiter = "\t")
            volts_S_sample = pd.DataFrame(df.loc[3,:])

            volts_T_S_sample = volts_S_sample.transpose()
            volts_T_S_sample['number'] = counter_sample_std
            volts_T_S_sample['Run_num'] = Run_num2
            volts_T_S_sample['ID'] = i
            sample_std_S_volts = sample_std_S_volts.append(volts_T_S_sample,sort=True)


        sample_std_S_volts = sample_std_S_volts.sort_values('Run_num')
        count2 = 0
        for i in range(len(sample_std_S_volts['Run_num'])):
            if count2%2 == 0:
                sample_std_S_volts_even = sample_std_S_volts_even.append(sample_std_S_volts.iloc[i],sort=True)
            else:
                sample_std_S_volts_odd = sample_std_S_volts_odd.append(sample_std_S_volts.iloc[i],sort=True)
            count2 += 1


        sample_std_S_volts_even = sample_std_S_volts_even.sort_values('Run_num')
        sample_std_S_volts_even = sample_std_S_volts_even.reindex(columns= cols_S)
        for c in cols_S:
            try:
                sample_std_S_volts_even[c] = pd.to_numeric(sample_std_S_volts_even[c])
            except:
                None

        sample_std_S_volts_odd = sample_std_S_volts_odd.sort_values('Run_num')
        sample_std_S_volts_odd = sample_std_S_volts_odd.reindex(columns= cols_S)
        for c in cols_S:
            try:
                sample_std_S_volts_odd[c] = pd.to_numeric(sample_std_S_volts_odd[c])
            except:
                None

        sample_std_S_volts_odd.reset_index(inplace=True)
        sample_std_S_volts_even.reset_index(inplace=True)
        sample_std_S_volts_odd['d_34S'] = None
        sample_std_S_volts_odd['d_34S_2'] = None
        sample_std_S_volts_odd['d_33S'] = None
        sample_std_S_volts_odd['d_33S_2'] = None
        sample_std_S_volts_odd['D_33S'] = None
        sample_std_S_volts_odd['D_33S_2'] = None



        for i in range(len(sample_std_S_volts_odd)):
            sample_std_S_volts_odd.loc[i,'d_34S']= (sample_std_S_volts_odd.loc[i,'H3 | L3']/(0.5*(sample_std_S_volts_even.loc[i,'H3 | L3'] + sample_std_S_volts_even.loc[i+1,'H3 | L3']))-1)*1000

            try:
                sample_std_S_volts_odd.loc[i,'d_34S_2'] = ((0.5*(sample_std_S_volts_odd.loc[i,'H3 | L3']+sample_std_S_volts_odd.loc[i+1,'H3 | L3']))/(0.5*(sample_std_S_volts_even.loc[i,'H3 | L3']+sample_std_S_volts_even.loc[i+2,'H3 | L3']))-1)*1000
            except: #if last row -> out of bounds error. so i set it to 9999999
                sample_std_S_volts_odd.loc[i,'d_34S_2'] = 9999999
            sample_std_S_volts_odd.loc[i,'d_33S'] = (sample_std_S_volts_odd.loc[i,'C | L3']/(0.5*(sample_std_S_volts_even.loc[i,'C | L3'] + sample_std_S_volts_even.loc[i+1,'C | L3']))-1)*1000
            try:
                sample_std_S_volts_odd.loc[i,'d_33S_2'] = ((0.5*(sample_std_S_volts_odd.loc[i,'C | L3']+sample_std_S_volts_odd.loc[i+1,'C | L3']))/(0.5*(sample_std_S_volts_even.loc[i,'C | L3']+sample_std_S_volts_even.loc[i+2,'C | L3']))-1)*1000
            except: #if last row -> out of bounds error. so i set it to 9999999
                sample_std_S_volts_odd.loc[i,'d_33S_2'] = 9999999

            sample_std_S_volts_odd.loc[i,'D_33S'] = (math.log(sample_std_S_volts_odd.loc[i,'d_33S']/1000+1)-0.515 * math.log(sample_std_S_volts_odd.loc[i,'d_34S']/1000+1))*1000
            sample_std_S_volts_odd.loc[i,'D_33S_2'] = (math.log(sample_std_S_volts_odd.loc[i,'d_33S_2']/1000+1)-0.515 * math.log(sample_std_S_volts_odd.loc[i,'d_34S_2']/1000+1))*1000


        for i in opz_files_S:

            df = pd.read_csv(path + i,delimiter="\t")
            time = df.iloc[9,0]
            time_1 = time[15:22]
            if counter_opz == 1:
                exact_33_mass = df.iloc[15,3]
            #get row number of 'Time' to skiprows from there
            skip = np.where(df['Unnamed: 1']=='Time')
            df = pd.read_csv(path + i,skiprows=int(skip[0])+1, delimiter="\t")

            volts_S = pd.DataFrame(df.loc[22, :])
            volts_T_S = volts_S.transpose()
            volts_T_S.loc[22,'Unnamed: 5'] = time_1
            volts_T_S.loc[22,'Cycle'] = i
            volts_T_S.loc[22,'count'] = counter_opz




            opz_volts_S = opz_volts_S.append(volts_T_S,sort=True)
            counter_opz += 2
        cols_num_S = ['32S',exact_33_mass,'34S']
        for c in cols_num_S:
            opz_volts_S[c] = pd.to_numeric(opz_volts_S[c])

        opz_volts_S['34/32'] = opz_volts_S['34S'] / opz_volts_S['32S']
        opz_volts_S['33/32'] = opz_volts_S[exact_33_mass] / opz_volts_S['32S']

        # plotting signal opz intensity
        opz_volts_S.plot(kind='scatter', x='count', y='32S')
        axes = plt.gca()
        max_val_y = opz_volts_S['32S'].max()
        min_val_y = opz_volts_S['32S'].min()
        axes.set_ylim([min_val_y-0.01, max_val_y + 0.01])
        plt.savefig(directory_1+'GUI_images/opz_graph_S.png')

        # plotting 33/32 vs 34/32
        opz_volts_S.plot(kind='scatter', x='34/32', y='33/32')
        axes = plt.gca()
        max_val_y, min_val_y = opz_volts_S['33/32'].max(),opz_volts_S['33/32'].min()
        max_val_x, min_val_x = opz_volts_S['34/32'].max(),opz_volts_S['34/32'].min()

        axes.set_ylim([min_val_y - 0.0001, max_val_y + 0.0001])
        axes.set_xlim([min_val_x - 0.0001, max_val_x + 0.0001])
        plt.savefig(directory_1 + 'GUI_images/opz_ratio_plot.png')



        writer = pd.ExcelWriter(out_filepath + 'output_S.xlsx')
        sample_std_S_volts_even.to_excel(writer, 'standards')
        sample_std_S_volts_odd.to_excel(writer, 'samples')
        opz_volts_S.to_excel(writer, 'opz_S')
        writer.save()
        """
        strontium processing
        """
    else:
        for file in os.listdir(path):
            try:
                if file.endswith('.exp'):
                    exp_files.append(str(file))
            except:
                print('no files found')

        exp_files = sorted(exp_files)
        opz_files = [x for x in exp_files if 'OPZ' in x and str(last_opz) not in x]#kick out last opz exp file
        NBS_files = [x for x in exp_files if 'NBS' in x]
        samples_std_files = [x for x in exp_files if x not in opz_files and str(last_opz) not in x]
        samples_std_files = sorted(samples_std_files)

        opz_volts = pd.DataFrame()
        sample_std_volts = pd.DataFrame()#columns=cols2)
        count= 0 #counts how many samples lost signal during the measurement
        for i in samples_std_files:
            df = pd.read_csv(path+i,delimiter="\t")
            try:
                sd = df.iloc[83,8]
            except:
                print('error: ' ,i)
            print(i , float(sd))
            if float(sd)<3: #if relative standard deviation of 88Sr (proxy for signal intensity) is higher than 3 % signal was not stable and average has to be recalculated
                summary= pd.DataFrame(df.iloc[76:86,:])
                summary.loc[76,'Neptune Analysis Data Report'] = i
                #print(summary.shape)
                Sr87_mean = summary.iloc[4,10]
                Sr87_stdErr = summary.iloc[6,10]
                Sr87_stdDev = summary.iloc[8,10]
                Sr88_mean = summary.iloc[4,8]

                summary['Sr88_mean'] = None
                summary['Sr87_mean'] = None
                summary['Sr87_stdErr'] = None
                summary['Sr87_stdDev'] = None
                summary.loc[77,'Sr88_mean']= Sr88_mean
                summary.loc[77,'Sr87_mean']= Sr87_mean
                summary.loc[77,'Sr87_stdErr']= Sr87_stdErr
                summary.loc[77,'Sr87_stdDev']= Sr87_stdDev
                sample_std_volts= sample_std_volts.append(summary)
                print(sd, '\n')
            else:
                summary = pd.DataFrame(df.iloc[14:86, :])
                summary.loc[14, 'Neptune Analysis Data Report'] = i
                summary.loc[77, 'Neptune Analysis Data Report'] = 'sd>3%'
                #print(summary.shape)
                sample_std_volts = sample_std_volts.append(summary)
                print('sd>3%')
                print(sd, '\n')
                count += 1

        cols_num = ['Sr87_mean','Sr87_stdDev', 'Sr87_stdErr','Sr88_mean']
        for skip in cols_num:
            sample_std_volts[skip] = pd.to_numeric(sample_std_volts[skip])
        opz_count= 0
        for i in opz_files:

            try:
                skip = np.where(df['Unnamed: 1'] == 'Time')
                df = pd.read_csv(path+i,skiprows=int(skip[0])+1,delimiter= "\t")
                #print(df.columns)
                opz_count += 1
                signal = df.iloc[22,8]

                volts = pd.DataFrame(df.loc[:, '88Sr'])
                volts.loc[28] = i
                volts['opz_mean_88Sr']= None
                volts['count']= None

                volts.loc[28,'opz_mean_88Sr']=signal
                volts.loc[28,'count']=opz_count

                opz_volts = opz_volts.append(volts)

            except:
                df = pd.read_csv(path + i, delimiter="\t")
                opz_volts = opz_volts.append(df)
                print('error', opz_files)
                opz_count += 1
        opz_volts['opz_mean_88Sr'] = pd.to_numeric(opz_volts['opz_mean_88Sr'])
        opz_volts['count'] = pd.to_numeric(opz_volts['count'])

        #plotting signal opz intensity
        opz_volts.plot(kind = 'scatter', x='count',y='opz_mean_88Sr')
        axes = plt.gca()
        max_val_y = opz_volts['opz_mean_88Sr'].max()
        axes.set_ylim([0, max_val_y+0.001])
        plt.savefig(directory_1+'GUI_images/opz_graph.png')


        #sample_std_volts = sample_std_volts.reindex(cols2,axis=1)
        writer = pd.ExcelWriter(out_filepath +'neptune_output.xlsx')
        sample_std_volts.to_excel(writer, 'samples')
        opz_volts.to_excel(writer, 'opz')
        writer.save()

#nep_processing(in_path,out_path,last_opz)