import re
import pandas as pd

#slot = pd.read_excel("demo.xlsx", sheet_name=0)
slot = pd.read_csv("demo2_blank.csv", sep="\t",index_col = False)
df1= pd.DataFrame(slot )
#regex_subject_code = [A-Z]{3}[0-9]{4}
slot2 = pd.read_csv("demo_blank.csv", sep="\t",index_col = False)
df2= pd.DataFrame(slot2 )


REGEX_SLOT = '([A-Z]{3}[0-9]{4})-(.*)-(.*)-(.*)'  # (1:CODE)-(2:TYPE)-(3:SLOT)-(4:VENUE)
WEEK_DAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI']

THEORY_START = ('08:00 	09:00 	10:00 	11:00 	12:00 	- 	14:00 	15:00 	16:00 	17:00 	18:00   19:00').split()


Day_slot= {}
all_slots=[]
Day_slot2= {}
all_slots2=[]

p=0
day='sun'
with open('Manager2.csv', 'r') as tt:
    for line in tt:
        #print(line)
        line=line.lstrip()
        if line.startswith('User Image'):
            print("################### New User")
            print(len(all_slots))

            # LAB
            if (all_slots != [] and len(all_slots)==60):
                print(len(all_slots))
                Day_slot[name] = all_slots
                print("###########           Adding to df (lab): " + name)
                df1[name] = all_slots
                all_slots=[]
            else:
                print(len(all_slots))
                all_slots=[]
            name1= line
            name = name1.split(' ')[2][0:9]
            print(name)
            #if(all_slots!=[]):
            #    Day_slot[name] = slots


            # THEORY
            if (all_slots2 != [] and len(all_slots2)==60):
                Day_slot2[name] = all_slots2
                #print(len(all_slots2))
                print("###########           Adding to df (theory): " + name)
                df2[name] = all_slots2
                #print(df2)
                all_slots2=[]
            else:
                all_slots2=[]
            name12= line
            name2 = name12.split(' ')[2][0:9]

        # Theory Row
        if (line.startswith(tuple(WEEK_DAYS))):
            p=1
            if(line.startswith('WED')):
                day='WED'
            else:
                day='notWED'


            #print(line)
            #slots = []
            words = line.split('\t')
            for i in range(len(words)):
                word= words[i]
                x= re.findall(r'(.*-*[A-Z]{3}[0-9]{4}-.*-.*)', word)
                #print(x)
                word=word.strip()
                if(x==[] and word not in WEEK_DAYS and word != "Theory" and word != '-' and word !=' '):
                    #slots.extend('0')
                    all_slots2.extend('0')
            
                else:
                    #print(x)
                    #slots.extend(x)
                    all_slots2.extend(x)
            continue
  
        # Lab Row
        if (p == 1):
            p=0
            pass
        else:
            continue
        
        #print(line)
        #slots = []
        words = line.split('\t')
        t=0
        for i in range(len(words)):
            t+=1
            word= words[i]
            x= re.findall(r'(.*-*[A-Z]{3}[0-9]{4}-.*-.*)', word)
            word=word.strip()
            if(x==[] and word not in WEEK_DAYS and word!="Lab" and word != '-' and word != "Lunch" and word !=' '):
                #slots.extend('0')
                all_slots.extend('0')
                #print("000000000000")
            elif(day=='WED' and word == 'Lunch'):
                #slots.extend('0')
                all_slots.extend('0')
                #slots.extend('0')
                all_slots.extend('0')
                #print("000000000000_WED_LUNCH")

            elif(t == 6 or t==13):
                #print(x)
                all_slots.pop()  
                all_slots.extend(x)
                all_slots.extend(x)  

            elif(t==7 or t==14):
                all_slots.extend('0')

            else:
                #print(x)
                #slots.extend(x)
                all_slots.extend(x)


#print(Day_slot)
#print(all_slots)
#print(df1)

#df= pd.DataFrame(all_slots)

if (all_slots != [] and len(all_slots)==60):
    print(len(all_slots))
    Day_slot[name] = all_slots
    print("###########           Adding to df end (lab) : " + name)
    df1[name] = all_slots
    all_slots=[]

# if (all_slots2 != [] and len(all_slots2)==60):
#     print(len(all_slots2))
#     Day_slot2[name] = all_slots2
#     print("###########           Adding to df end (theory): " + name)
#     df2[name] = all_slots2
#     all_slots2=[]

name2 = name12.split(' ')[1][5:]
name = name1.split(' ')[1][5:]

#print(name)
#df1[name]= all_slots

# Lab
print(df1)
df1.to_csv("demo2.csv",index=False, sep="\t")

# Theory
print(df2)
df2.to_csv("demo.csv",index=False, sep="\t")
