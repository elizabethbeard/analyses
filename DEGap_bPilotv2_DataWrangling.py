#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 16:50:27 2019

@author: lizbeard
"""
''' script to parse through DEGap bPilotv2 subject files and then concatenate
them into the relevant csv's ''' 

#libraries
import pandas as pd

#directories
datadir = '/Users/lizbeard/Documents/TU_2018-2019/DEGap/data/bPilotv2_logs'
savedir = '/Volumes/GoogleDrive/Team Drives/DEGap/data'

#tasks
tasks = ['ebdm', 'dbdm']

#subjs
subjs = range(201,226)
badsubjs = [203, 204,220]

#make a loop to go through the main task csvs and add them to a master dataframe
for task in tasks:
    
    dfBig= pd.DataFrame()
    
    for subj in subjs:
        print('Working on DE',subj,' task: ',task)
#        had to subset df_run2 because the subjects had to re-run run2
        if subj not in badsubjs:
#            add sub block for subjs 205,212 bc they only had a single run of 
#            ebdm/dbdm (oops)
            if subj == 205 and task == 'dbdm':
                df_run2 = pd.read_csv('%s/DE%s/DE%s_%s_run_2.csv' % 
                                      (datadir, subj, subj, task))
                df_run2['subj'] = subj
                df_run2['run'] = 2
                           
                dfBig = pd.concat([dfBig,df_run2], sort=False)

            elif subj == 212 and task == 'ebdm':
                df_run1 = pd.read_csv('%s/DE%s/DE%s_%s_run_1.csv' % 
                                      (datadir, subj, subj, task))
                df_run1['subj'] = subj
                df_run1['run'] = 1
                
                dfBig = pd.concat([dfBig,df_run1], sort=False)
                
            else:
                df_run1 = pd.read_csv('%s/DE%s/DE%s_%s_run_1.csv' % 
                                      (datadir, subj, subj, task))
                df_run1['subj'] = subj
                df_run1['run'] = 1
                
                df_run2 = pd.read_csv('%s/DE%s/DE%s_%s_run_2.csv' % 
                                      (datadir, subj, subj, task))
                df_run2['subj'] = subj
                df_run2['run'] = 2
    
                dfBig = pd.concat([dfBig,df_run1, df_run2], sort=False)
    
#        save out the big file
    dfBig.to_csv('%s/%s_bPilotv2_20190212.csv' % (savedir,task), 
                     na_rep='NA', index=False)
 
''' FIGURE THIS PART OUT TOMORROW '''       
#make a loop to go through the ebdm sampling csvs and add them to a master dataframe
# remove extraneous variables
# add more if you want later
del df_run1, df_run2, dfBig, subj, task, tasks

dfBig = pd.DataFrame()

for subj in subjs:
    if subj not in badsubjs:
        if subj == 212:
            df_run2 = pd.read_csv('%s/DE%s/DE%s_ebdm_samplingdata_run_2.csv' % 
                              (datadir, subj, subj))
            df_run2['subj'] = subj
            df_run2['run'] = 2
            
            runs = [df_run2]
            
        else:

            df_run1 = pd.read_csv('%s/DE%s/DE%s_ebdm_samplingdata_run_1.csv' % 
                                  (datadir, subj, subj))
            df_run1['subj'] = subj
            df_run1['run'] = 1
            df_run2 = pd.read_csv('%s/DE%s/DE%s_ebdm_samplingdata_run_2.csv' % 
                                  (datadir, subj, subj))
            df_run2['subj'] = subj
            df_run2['run'] = 2
            
            runs = [df_run1,df_run2]
        
        '''instead of calculating the subjects seen probabilties from the larger 
        data file, I decided to  calculate them within their individual
        data frames and *then* concatenate them -- this seems to be slow from a
        computational/memory usage standpoint but hey it works'''
        for run in runs:
            print('Workong in DE',subj,' run', run)
            
            run['seen_p1_1'] = 0
            run['seen_p2_1'] = 0                    
            run['seen_o1_1'] = 0                
            run['seen_o2_1'] = 0
            run['seen_p1_2'] = 0
            run['seen_p2_2'] = 0                 
            run['seen_o1_2'] = 0               
            run['seen_o2_2'] = 0
            
            trials = list(range(1,19))  
            
            for trial in trials:
                print('Evaluating trial ', trial,'in run ', 
                      run, 'for subject ', subj)
                trial_data = run.loc[run['Trial']==trial]
                
                resp1total = list(trial_data['Resp']).count(1)
                resp2total = list(trial_data['Resp']).count(2)
                totalresp = resp1total+resp2total
                
                out1 = list(trial_data['Outcome'].loc[trial_data['Resp']==1])
                unique1 = list(set(out1))
                
                if len(unique1) == 0:
                    trial_data['seen_p1_1'] = 'NA'
                    trial_data['seen_p2_1'] = 'NA'                                   
                    trial_data['seen_o1_1'] = 'NA'
                    trial_data['seen_o2_1'] = 'NA'
                    
                    run.loc[run['Trial']==trial, ['seen_p1_1']] = trial_data['seen_p1_1']
                    run.loc[run['Trial']==trial, ['seen_p2_1']] = trial_data['seen_p2_1']
                    run.loc[run['Trial']==trial, ['seen_o1_1']] = trial_data['seen_o1_1']
                    run.loc[run['Trial']==trial, ['seen_o2_1']] = trial_data['seen_o2_1']
                
                elif len(unique1) == 2:
                    x1 = out1.count(unique1[0])
                    x2 = out1.count(unique1[1])
                    
                    seen_p1_1 = x1/resp1total 
                    seen_p2_1 = x2/resp1total
                    seen_o1_1 = unique1[0]
                    seen_o2_1 = unique1[1]
                
                    trial_data['seen_p1_1'] = seen_p1_1
                    trial_data['seen_p2_1'] = seen_p2_1                                   
                    trial_data['seen_o1_1'] = seen_o1_1
                    trial_data['seen_o2_1'] = seen_o2_1
                    
                    run.loc[run['Trial']==trial, ['seen_p1_1']] = trial_data['seen_p1_1']
                    run.loc[run['Trial']==trial, ['seen_p2_1']] = trial_data['seen_p2_1']
                    run.loc[run['Trial']==trial, ['seen_o1_1']] = trial_data['seen_o1_1']
                    run.loc[run['Trial']==trial, ['seen_o2_1']] = trial_data['seen_o2_1']
                    
                    
                else:
                    x = out1.count(unique1)
                    seen_p1_1 = x/resp1total
                    seen_p2_1 = 0
                    seen_o1_1 = unique1[0]
                    seen_o2_1 = 0
                    
                    trial_data['seen_p1_1'] = seen_p1_1
                    trial_data['seen_p2_1'] = seen_p2_1                                   
                    trial_data['seen_o1_1'] = seen_o1_1
                    trial_data['seen_o2_1'] = seen_o2_1
                    
                    run.loc[run['Trial']==trial, ['seen_p1_1']] = trial_data['seen_p1_1']
                    run.loc[run['Trial']==trial, ['seen_p2_1']] = trial_data['seen_p2_1']
                    run.loc[run['Trial']==trial, ['seen_o1_1']] = trial_data['seen_o1_1']
                    run.loc[run['Trial']==trial, ['seen_o2_1']] = trial_data['seen_o2_1']
                    
                
                out2 = list(trial_data['Outcome'].loc[trial_data['Resp']==2])
                unique2 = list(set(out2))
                
                if len(unique2) == 0:
                    trial_data['seen_p1_2'] = 'NA'
                    trial_data['seen_p2_2'] = 'NA'                    
                    trial_data['seen_o1_2'] = 'NA'                
                    trial_data['seen_o2_2'] = 'NA'
                    
                    run.loc[run['Trial']==trial, ['seen_p1_2']] = trial_data['seen_p1_2']
                    run.loc[run['Trial']==trial, ['seen_p2_2']] = trial_data['seen_p2_2']
                    run.loc[run['Trial']==trial, ['seen_o1_2']] = trial_data['seen_o1_2']
                    run.loc[run['Trial']==trial, ['seen_o2_2']] = trial_data['seen_o2_2']
                    
                elif len(unique2) == 2:
                    y1 = out2.count(unique2[0])
                    y2 = out2.count(unique2[1])
                    
                    seen_p1_2 = y1/resp2total 
                    seen_p2_2 = y2/resp2total
                    seen_o1_2 = unique2[0]
                    seen_o2_2 = unique2[1]
                
                    trial_data['seen_p1_2'] = seen_p1_2
                    trial_data['seen_p2_2'] = seen_p2_2                    
                    trial_data['seen_o1_2'] = seen_o1_2                
                    trial_data['seen_o2_2'] = seen_o2_2
                    
                    run.loc[run['Trial']==trial, ['seen_p1_2']] = trial_data['seen_p1_2']
                    run.loc[run['Trial']==trial, ['seen_p2_2']] = trial_data['seen_p2_2']
                    run.loc[run['Trial']==trial, ['seen_o1_2']] = trial_data['seen_o1_2']
                    run.loc[run['Trial']==trial, ['seen_o2_2']] = trial_data['seen_o2_2']
                    
                else:
                    y = out2.count(unique2)
                    seen_p1_2 = y/resp2total
                    seen_p2_2 = 0
                    seen_o1_2 = unique2[0]
                    seen_o2_2 = 0
                    
                    trial_data['seen_p1_2'] = seen_p1_2
                    trial_data['seen_p2_2'] = seen_p2_2                    
                    trial_data['seen_o1_2'] = seen_o1_2                
                    trial_data['seen_o2_2'] = seen_o2_2
                    
                    run.loc[run['Trial']==trial, ['seen_p1_2']] = trial_data['seen_p1_2']
                    run.loc[run['Trial']==trial, ['seen_p2_2']] = trial_data['seen_p2_2']
                    run.loc[run['Trial']==trial, ['seen_o1_2']] = trial_data['seen_o1_2']
                    run.loc[run['Trial']==trial, ['seen_o2_2']] = trial_data['seen_o2_2']
        
        dfBig = pd.concat([dfBig,df_run1, df_run2], sort=False)                                            
    
#save out the big file to the Google Drive and to my local folder
dfBig.to_csv('%s/ebdm_samplingdata_bPilotv2_20190206.csv' % (savedir),
             na_rep='NA', index=False)
