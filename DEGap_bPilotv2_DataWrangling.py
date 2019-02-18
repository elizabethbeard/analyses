#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 12:45:47 2019

@author: lizbeard
"""
import pandas as pd
import numpy as np

datadir = '/Volumes/GoogleDrive/Team Drives/DEGap/Tasks/bPilotv2/logs'
savedir = '/Volumes/GoogleDrive/Team Drives/DEGap/data'
task = '20190131_ebdm_samplingdata'

subjs = range(201,214)
dfBig = pd.DataFrame()

#make a loop to go through the csvs and add them to a master dataframe
for subj in subjs:
    df_run1 = pd.read_csv('%s/DE%s/DE%s_ebdm_samplingdata_run_1.csv' % (datadir, subj, subj))
    df_run1['subj'] = subj
    df_run1['run'] = 1
    df_run2 = pd.read_csv('%s/DE%s/DE%s_ebdm_samplingdata_run_2.csv' % (datadir, subj, subj))
    df_run2['subj'] = subj
    df_run2['run'] = 2
    
    dfBig = pd.concat([dfBig,df_run1, df_run2], sort=False)
    
dfBig.to_csv('%s/%s_samplingData_20190131.csv' % (savedir,task))

newsubjs = [201,202,205,206,207,208,209,210,211]
task2 = '20190131_ebdm'

for subj in newsubjs:
    df_run1 = pd.read_csv('%s/DE%s/DE%s_ebdm_run_1.csv' % (datadir, subj, subj))
    df_run1['subj'] = subj
    df_run1['run'] = 1
    df_run2 = pd.read_csv('%s/DE%s/DE%s_ebdm_run_2.csv' % (datadir, subj, subj))
    df_run2['subj'] = subj
    df_run2['run'] = 2
    
    dfBig = pd.concat([dfBig,df_run1, df_run2], sort=False)
    
dfBig.to_csv('%s/%s_2.csv' % (savedir,task2))
