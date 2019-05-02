import pandas as pd
from pprint import pprint
from functools import reduce
import re



WEEK_DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI']
TIME_LIST=[8,9,10,11,12,13,14,15,16,17,18,19]
finance_members2 = ['17BCE0851', '17BCE0354', '17BEE0150']

free_stu = {}
free_stu2 = {}
free_stu3 = {}
dict_Reg_Name={}

#############    Update dict_Reg_Name
with open('Manager2.csv', 'r') as tt:
    for line in tt:
        if line.startswith("\"2018/12") or line.startswith("\"2019"):
            pass
        else:
            continue
        print(line)
        words = line.split(',')
        if words[1][1:-1] not in dict_Reg_Name.keys():
            dict_Reg_Name[words[1][1:-1]]= words[2][1:-1]
print(dict_Reg_Name)
print(len(dict_Reg_Name))


####### preprocess free_slot files
def replace_to_tab(file1, file2):
        c=""
        f = open(file1,'r')
        for lines in f:
                c+=lines.replace(',','\t')
        f.close()

        f2 = open(file2,'w')
        f2.write(c)
        f2.close()

replace_to_tab('demo.csv','demox.csv')      #theory_slots
replace_to_tab('demo2.csv','demox2.csv')    #lab_slots


##### Read files
slot = pd.read_csv("demox.csv", sep="\t",index_col = False)
df_theory = pd.DataFrame(slot)
slotx2 = pd.read_csv("demox2.csv", sep="\t",index_col = False)
df_lab = pd.DataFrame(slotx2)

final_dict = {}
for day in range(0,5):
        dict_freeTime_reg1 = {}         #theory
        dict_freeTime_reg2 = {}         #lab
        dict_reg_freeTime = {}            #theory + lab
        for i in TIME_LIST:
                free_stu[i]= []
                free_stu2[i]= []        
                free_stu3[i]= []


        ############-------------- THEORY FREE SLOT

        df1= df_theory.loc[df_theory['Day'] == day]
        l=list(df1)
        #print(l)
        for i in range(2,len(l)):
                reg= l[i]
                df2 = df1[['Time',reg]]
                #print("Yes")
                #print(df2[reg])
                listtime = df2.loc[df2[reg].astype(object)=='0']['Time'].tolist()
                for j in listtime:
                        free_stu[j].append(dict_Reg_Name[reg])
                dict_freeTime_reg1[reg] = listtime

        #print(dict_freeTime_reg1)


        #############-------------  LAB FREE SLOT

        df1= df_lab.loc[df_lab['Day'] == day]
        l=list(df1)
        for i in range(2,len(l)):
                reg= l[i]
                #print(reg + " : " + dict_Reg_Name[reg])
                df2 = df1[['Time',reg]]
                listtime = df2.loc[df2[reg].astype(object)=='0']['Time'].tolist()
                #print(listtime)
                for j in listtime:
                        #print(j)
                        free_stu2[j].append(dict_Reg_Name[reg])
                        
                dict_freeTime_reg2[reg] = listtime

        #print(dict_freeTime_reg2)

        ################-------------- LAB + THEORY FREE people at specific time
        for j in free_stu:
                for i in free_stu[j]:
                        if (i in free_stu2[j]):
                                free_stu3[j].append(i.title())
        print()
        print()
        print("##################################################################################")
        print(WEEK_DAYS[day])
        print("##################################################################################")
        print()
        pprint(free_stu3)     
         
         
        ###############----------   LAB + THEORY FREE slot of each person
        for regno in dict_freeTime_reg1:
                for i in dict_freeTime_reg1[regno]:
                        if(i in dict_freeTime_reg2[regno]):
                                if regno not in dict_reg_freeTime:
                                        dict_reg_freeTime[regno] = []

                                dict_reg_freeTime[regno].append(str(i))

        # Name : Free slots
        print()
        print(WEEK_DAYS[day])      
        print()
        for k in dict_reg_freeTime:
                print(dict_Reg_Name[k] + " : ",end="")
                print(dict_reg_freeTime[k])


        ###############------------ Find common free slot of students:
        newDict = {}
        for regno in dict_reg_freeTime:
                if regno in finance_members2:
                        newDict[regno] = dict_reg_freeTime[regno]
        print(sorted(list(reduce(set.intersection, [set(item) for item in list(newDict.values()) ]))))





#pprint(final_dict)
        
