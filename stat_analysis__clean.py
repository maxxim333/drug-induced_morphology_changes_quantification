import matplotlib.pyplot as plt
from csv import reader
import numpy as np
from scipy import stats
from collections import Counter

number_of_wells=288 #How many wells are we working with?
number_of_images=number_of_wells*9 #We always have 9 photos per well

#Open CellProfiler output file
with open('/Users/maxxim333/Desktop/herrington/05_jul/MyExpt_Image_all.csv') as file:
    csv_reader = reader(file)
    header = next(csv_reader) #Skip header

    if header != None:
        #Define pertinent arrays
        mean_num_branch_end_array=[]
        mean_non_trunk_branches=[]
        mean_num_trunks=[]
        mean_total_skeleton_lenght=[]
        
        for row in csv_reader:
        # Append values from csv to the array. The relevant columns are 22 to 25.
            mean_num_branch_end_array.append(float(row[22]))
            mean_non_trunk_branches.append(float(row[23]))
            mean_num_trunks.append(float(row[24]))
            mean_total_skeleton_lenght.append(float(row[25]))

#Define array to store only those wells for which at least one of the metrics mean is greater than the corresponding mean of control and p-value <=0.05.
significant=[]

#Define function of Welch's t-test. that outputs the p-value of the t-test
def ttest(array, title):
    array = np.array_split(array, number_of_wells) #Split array in n parts. N will be equal to the number of wells. Consequently, each "part" will have 9 values
    array=np.array(array) #Transform to numpy array
    control = (array[np.r_[51:54,99:102,147:150,195:198]]).reshape(-1) #Define wells that corresponded to negative control (PBS-treated)

    #Calculate mean and standart deviation of control. Every subsequent well will be compared to this.
    means_control=np.mean(control)
    standart_control=np.std(control)

    #Create more relevant arrays
    means=[]
    standart_deviations=[]
    results=[]
    pvalues=[]
    labels=[]

    #Populate the labels array. This will be useful to cross-reference it with our drug list and give meaninfyl labeling
    for i in range(0,int(number_of_wells)):
        labels.append('Well_'+str(i+1))

    #Now we finally iterate over the wells and calculate means and standart deviations (and perform t-test against control)
    for element in range(0,(number_of_wells),1):
        treated=array[element]

        results.append(stats.ttest_ind(control, treated, equal_var = False))
        means.append(np.mean(treated))
        standart_deviations.append(np.std(treated))
        pvalues.append((round(results[-1][-1],2)))

        #This loop populates the "significant" array with the wells we will be most interested in
        if round(results[-1][-1],2) <=0.05:
            if np.mean(treated) >= means_control:
                significant.append(element)

    #Insert the control metrics at the beginning of every array
    means.insert(0,means_control)
    standart_deviations.insert(0,standart_control)
    pvalues.insert(0,0)
    labels.insert(0,'Control')

    significant.append(0) #Zero is the index of control and we want to always include it in the graph, so it will always be "significant" for us


#Run the function
ttest(mean_num_branch_end_array, 'Mean number of branch ends')
ttest(mean_non_trunk_branches, 'Mean number of branches')
ttest(mean_num_trunks, 'Mean number of trunks')
ttest(mean_total_skeleton_lenght, 'Total lenght of neurites')



#Taking a look of which wells are significant and in how many metrics
a = dict(Counter(significant))
dic2=dict(sorted(a.items(),key= lambda x:x[1]))
print(dic2)

significant=np.unique(significant) #Flatten the array so each index will appear only once




#The code until now was just to find the most relevant wells, in order to avoid having a graph with hundreds of bars.
# If we wanted we could stop here and call the plot over the data we have. The next chunk of code will be actually very similar but will only take into account the indices of wells that appear in "significant" array and build a graph with the data
def ttestsignificant(array, title):
    array = np.array_split(array, number_of_wells) #Split array in n parts. N will be equal to the number of wells. Consequently, each "part" will have 9 values
    array=np.array(array)
    control = (array[np.r_[51:54,99:102,147:150,195:198]]).reshape(-1)

    #Calculate mean and standart deviation of control. Every subsequent well will be compared to this.
    means_control=np.mean(control)
    standart_control=np.std(control)

    #Create more relevant arrays
    means=[]
    standart_deviations=[]
    results=[]
    pvalues=[]
    labels=[]

    #Populate the labels array. This will be useful to cross-reference it with our drug list and give meaninfyl labeling
    for i in range(0,int(number_of_wells)):
        labels.append('Well_'+str(i+1))


    #Now we finally iterate over the wells and calculate means and standart deviations (and perform t-test against control)
    for element in range(0,(number_of_wells),1):
        treated=array[element]
        results.append(stats.ttest_ind(control, treated, equal_var = False))
        means.append(np.mean(treated))
        standart_deviations.append(np.std(treated))
        pvalues.append((round(results[-1][-1],2)))


    #Insert control parameters
    means.insert(0,means_control)
    standart_deviations.insert(0,standart_control)
    pvalues.insert(0,0)
    labels.insert(0,'Control')

    #This chunk of code is to remove measurements of wells corresponding to control wells, since they are already included in the "control" array and it would make no sense to compare between controls
    del means[52:55], means[97:100], means[142:145], means[187:190]
    del standart_deviations[52:55], standart_deviations[97:100], standart_deviations[142:145], standart_deviations[187:190]
    del pvalues[52:55], pvalues[97:100], pvalues[142:145], pvalues[187:190]
    del labels[52:55], labels[97:100], labels[142:145], labels[187:190]

    #Generate plot
    fig, ax = plt.subplots()

    bar_x = []
    bar_height = []
    bar_tick_label = []
    bar_label = []
    new_st=[]


    for j in range(0,int(number_of_wells+1-12)): #The indices need to be adjusted now because we have one insertion of control that we didn't have when we were populating "significant" array and a deletion of 3 wells every 52 wells (as we deleted the control wells and inserted their metrics at the beginning of each array)
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



    def autolabel(rects): #This is to add p-value to the graph (on top of the bars)
        for idx, rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., max(means),
                    bar_label[idx],
                    ha='center', va='bottom', rotation=45, fontsize=6)

    plt.xticks(rotation=45)

    autolabel(bar_plot)
    plt.title(title)

    plt.show()

ttestsignificant(mean_num_branch_end_array, 'Mean number of branch ends')
ttestsignificant(mean_non_trunk_branches, 'Mean number of branches')
ttestsignificant(mean_num_trunks, 'Mean number of trunks')
ttestsignificant(mean_total_skeleton_lenght, 'Total lenght of neurites')