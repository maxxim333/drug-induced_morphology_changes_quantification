#https://forum.image.sc/t/measureneurons/14290
# #Hi,

#There are three types of points in this “branchpoint” image (from cellprofiler.org/CPmanual/Me … urons.html 22):

#[quote]NumberTrunks: The number of trunks. Trunks are branchpoints that lie within the seed objects
#NumberNonTrunkBranches: The number of non-trunk branches. Branches are the branchpoints that lie outside the seed objects.
#NumberBranchEnds: The number of branch end-points, i.e, termini.[/quote]

#Perhaps by your method (Morph > endpoints) starting with only the branchpoint image you are counting NumberTrunks also? You didn’t say which way the numbers skew, so this is just a guess.


import matplotlib.pyplot as plt

import pandas as pd
import csv
from csv import reader
import numpy as np
from scipy import stats
from collections import Counter


#Welsch t-test was used based on https://www.statology.org/welchs-t-test/ and https://www.statology.org/welch-t-test-python/

# skip first line i.e. read header first and then iterate over each row od csv as a list

number_of_wells=72
number_of_images=number_of_wells*9 #We always have 9 photos per well
with open('/Users/maxxim333/Desktop/herrington/05_jul/cell_profiler_output_4/MyExpt_Image.csv') as file:
    csv_reader = reader(file)
    header = next(csv_reader)

    if header != None:
        #Define pertinent arrays
        mean_num_branch_end_array=[]
        mean_non_trunk_branches=[]
        mean_num_trunks=[]
        mean_total_skeleton_lenght=[]
        
        for row in csv_reader:
        # Append values from csv to the array
            mean_num_branch_end_array.append(float(row[22]))
            mean_non_trunk_branches.append(float(row[23]))
            mean_num_trunks.append(float(row[24]))
            mean_total_skeleton_lenght.append(float(row[25]))
    
    #print(mean_num_branch_end_array)
    #print(newarr)
    #print(np.mean((mean_num_branch_end_array)))
    #print(np.mean(newarr, axis=1), np.std(newarr, axis=1))



significant=[]

#mean_num_trunks=np.array(mean_num_trunks)
#print(mean_num_trunks[np.r_[51:54,99:102]])

#Welch's t-test function outputs the p-value of the t-test
def ttest(array, title):
    array = np.array_split(array, number_of_wells) #Split array in n parts. N will be equal to the number of wells. Consequently, each "part" will have 9 values
    array=np.array(array)
    #control = (array[np.r_[51:54,99:102,147:150,195:198]]).reshape(-1)
    control = (array[51:54]).reshape(-1)
    means_control=np.mean(control)
    standart_control=np.std(control)


    means=[]
    standart_deviations=[]
    results=[]
    pvalues=[]

    labels=[]
    for i in range(0,int(number_of_wells)):
        labels.append('Well_'+str(i+1))



    for element in range(0,(number_of_wells),1):

        treated=array[element]


        results.append(stats.ttest_ind(control, treated, equal_var = False))


        means.append(np.mean(treated))
        standart_deviations.append(np.std(treated))
        pvalues.append((round(results[-1][-1],2)))

        if round(results[-1][-1],2) <=0.05:
            if np.mean(treated) >= means_control:
                significant.append(element)


    means.insert(0,means_control)
    standart_deviations.insert(0,standart_control)
    pvalues.insert(0,0)
    labels.insert(0,'Control')

    significant.append(0)

    del means[52:55]#, means[97:100], means[142:145], means[187:190]
    del standart_deviations[52:55]#, standart_deviations[97:100], standart_deviations[142:145], standart_deviations[187:190]
    del pvalues[52:55]#, pvalues[97:100], pvalues[142:145], pvalues[187:190]
    del labels[52:55]#, labels[97:100], labels[142:145], labels[187:190]




    fig, ax = plt.subplots()

    bar_x = labels
    bar_height = means
    bar_tick_label = labels
    bar_label = pvalues

    bar_plot = plt.bar(bar_x, bar_height, yerr=standart_deviations, tick_label=bar_tick_label)



    def autolabel(rects):
        for idx, rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., max(means),
                    bar_label[idx],
                    ha='center', va='bottom', rotation=45, fontsize=6)

    plt.xticks(rotation=45)

    autolabel(bar_plot)
    plt.title(title)

    #plt.show()

ttest(mean_num_branch_end_array, 'Mean number of branch ends')
ttest(mean_non_trunk_branches, 'Mean number of branches')
ttest(mean_num_trunks, 'Mean number of trunks')
ttest(mean_total_skeleton_lenght, 'Total lenght of neurites')



#Only significant
a = dict(Counter(significant))
print(a.values())
print(a)           #or print(a) in python-3.x

dic2=dict(sorted(a.items(),key= lambda x:x[1]))

print(dic2)


significant=np.unique(significant)




def ttestsignificant(array, title):
    array = np.array_split(array, number_of_wells) #Split array in n parts. N will be equal to the number of wells. Consequently, each "part" will have 9 values
    array=np.array(array)
    #control = (array[np.r_[51:54,99:102,147:150,195:198]]).reshape(-1)
    control = (array[np.r_[51:54]]).reshape(-1)
    means_control=np.mean(control)
    standart_control=np.std(control)


    means=[]
    standart_deviations=[]
    results=[]
    pvalues=[]

    labels=[]
    for i in range(0,int(number_of_wells)):
        labels.append('Well_'+str(i+1))



    for element in range(0,(number_of_wells),1):

        treated=array[element]


        results.append(stats.ttest_ind(control, treated, equal_var = False))


        means.append(np.mean(treated))
        standart_deviations.append(np.std(treated))
        pvalues.append((round(results[-1][-1],2)))



    means.insert(0,means_control)
    standart_deviations.insert(0,standart_control)
    pvalues.insert(0,0)
    labels.insert(0,'Control')


    del means[52:55]#, means[97:100], means[142:145], means[187:190]
    del standart_deviations[52:55]#, standart_deviations[97:100], standart_deviations[142:145], standart_deviations[187:190]
    del pvalues[52:55]#, pvalues[97:100], pvalues[142:145], pvalues[187:190]
    del labels[52:55]#, labels[97:100], labels[142:145], labels[187:190]




    fig, ax = plt.subplots()

    bar_x = []
    bar_height = []
    bar_tick_label = []
    bar_label = []
    new_st=[]


    for j in range(0,int(number_of_wells+1-12)):
        #print(labels[j])
        if j in significant:
            if j==0:
                bar_x.append(labels[j])
                bar_height.append(means[j])
                bar_tick_label.append(labels[j])
                bar_label.append(pvalues[j])
                new_st.append(standart_deviations[j])
            elif j>0 and j<52:
                bar_x.append(labels[j+1])
                bar_height.append(means[j+1])
                bar_tick_label.append(labels[j+1])
                bar_label.append(pvalues[j+1])
                new_st.append(standart_deviations[j+1])
            elif j>=52 and j<100:
                bar_x.append(labels[j-2])
                bar_height.append(means[j-2])
                bar_tick_label.append(labels[j-2])
                bar_label.append(pvalues[j-2])
                new_st.append(standart_deviations[j-2])
            elif j >= 100 and j < 148:
                bar_x.append(labels[j - 5])
                bar_height.append(means[j - 5])
                bar_tick_label.append(labels[j - 5])
                bar_label.append(pvalues[j - 5])
                new_st.append(standart_deviations[j - 5])
            elif j>=148 and j<196:
                bar_x.append(labels[j - 8])
                bar_height.append(means[j - 8])
                bar_tick_label.append(labels[j - 8])
                bar_label.append(pvalues[j - 8])
                new_st.append(standart_deviations[j - 8])


    bar_plot = plt.bar(bar_x, bar_height, yerr=new_st, tick_label=bar_tick_label)



    def autolabel(rects):
        for idx, rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., max(means),
                    bar_label[idx],
                    ha='center', va='bottom', rotation=45, fontsize=6)

    plt.xticks(rotation=45)

    autolabel(bar_plot)
    plt.title(title)

    plt.show()

#ttestsignificant(mean_num_branch_end_array, 'Mean number of branch ends')
#ttestsignificant(mean_non_trunk_branches, 'Mean number of branches')
#ttestsignificant(mean_num_trunks, 'Mean number of trunks')
ttestsignificant(mean_total_skeleton_lenght, 'Total lenght of neurites')