"Whatsapp Text flirt Analyser"


import numpy as np
import pandas as pd
import time
start = time. time()
_list=[]
dataset=pd.DataFrame()

bool_ = {"Date First": True, "Month First": False}

from dateutil.parser import parse

def is_date(string):
    """Function to check if the string is date or not."""
    try:
        parse(string)
        return True
    except:
        return False


def get_dict(date, time, Name, Text, weekday, hour_of_day):
    """Return dictionary to build DF."""
    return dict(
        date=date,
        time=time,
        Name=Name,
        Text=Text,
        weekday=weekday,
        hour_of_day=hour_of_day)

with open('dk.txt', encoding='utf8') as fp:
        for line in fp:
            #print(line)
            if not line.isspace():
                record = line.strip().split(" - ", 1)
                #print(record)
                if (len(record) == 1):
                    #print(record)
                    #print("inside len(record) == 1")
                    _list.append(
                        get_dict(np.nan, np.nan, np.nan, line, np.nan,
                                 np.nan))
                   
                elif not (is_date(record[0])):
                    #print("inside is_date(record[0])")
                    _list.append(
                        get_dict(np.nan, np.nan, np.nan, line, np.nan,
                                 np.nan))
                else:
                    #print("inside else")
                    date_time = parse(record[0], dayfirst=True)
                    #print(date_time)
                    info = record[1].split(":", 1)
                    #print(info)
                    if len(info) == 1:
                        #print("inside len(info) == 1 ")
                        #print(record)
                        _list.append(
                            get_dict(
                                date_time.date().strftime("%d/%m/%Y"),
                                date_time.time().strftime("%I:%M %p"),
                                np.nan, info[0], date_time.weekday(),
                                date_time.time().strftime("%H")))
                    else:
                        #print("inside else of len(info) == 1")
                        _list.append(
                            get_dict(
                                date_time.date().strftime("%d/%m/%Y"),
                                date_time.time().strftime("%I:%M %p"),
                                info[0], info[1], date_time.weekday(),
                                date_time.time().strftime("%H")))
                dataset = pd.DataFrame(_list)
            



dataset['Text']=dataset['Text'].str.lower()

import emoji
def give_emoji_free_text(text):
    allchars = [str for str in text.decode('utf-8')]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.decode('utf-8').split() if not any(i in str for i in emoji_list)])
    return clean_text

"Replacing media into space so that easily can remove the rows"
dataset['Text'] = dataset['Text'].str.replace('<media omitted>','')
dataset['Text'] = dataset['Text'].str.replace('this message was deleted','')

l,w=dataset.shape
dataset.index=range(l)

"Removed emojis chat text"
for j,text in enumerate(dataset['Text']): 
    dataset['Text'][j]=give_emoji_free_text(text.encode('utf8'))

"To remove empty line which does not comes in isnull value"    

dataset['TW']=dataset['Text'].str.split().str.len()#total number of words in each row

import numpy as np

dataset['TW'].replace(0, np.nan, inplace=True)# Replace 0 word row to nana value

dataset=dataset.dropna(subset=['TW','date','hour_of_day','Name','time','weekday']) # drop nan value row wise

total_word_file=dataset['TW'].sum() # total words in  file
dataset.isna().sum()


[l,h]=dataset.shape
dataset.index=range(l)



"Removing Emojis in Names this method helps when words and eojis are withoutspace"

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

for num, name in enumerate(dataset.Name):
    dataset['Name'][num] = deEmojify(name.lower())
    
"Finding top 3 chats with  words count "    
chater=dataset['Name'].value_counts().head(3).to_dict()   

print("Chaters:",chater)
 
"Finding More"
Talker=dataset['Name'].value_counts().idxmax()
print("More Talktative:", Talker.upper())

Less_Talker=dataset['Name'].value_counts().idxmin()
print("Less Talktative:", Less_Talker.upper())

  
Talker_chat= pd.DataFrame(dataset[dataset.Name==Talker])
Less_chat= pd.DataFrame(dataset[dataset.Name==Less_Talker])  
    
unique_Frequency_Talker= pd.DataFrame(Talker_chat['Text'].str.split(' ', expand =True).stack().value_counts())
unique_Frequency_Lesser= pd.DataFrame(Less_chat['Text'].str.split(' ', expand =True).stack().value_counts())

unique_Frequency_Talker['Usage of word']=(unique_Frequency_Talker[0]/Talker_chat['TW'].sum())*100
unique_Frequency_Lesser['Usage of word']=(unique_Frequency_Lesser[0]/Less_chat['TW'].sum())*100   


flirt_words=['kiss','hug','date', 'cute', 
           'beautiful', 'sexy', 'hot','uma', 'darling',
           'fuck','porn', 'x', 'sex', 'matter', 'nipple', 'virgin', 'sperm',
           'seduce', 'condom']

#Extracting flirt word
Talker_Filter_list=[]

Less_Filter_list=[]

for i in unique_Frequency_Talker.index:
    if i in flirt_words:
        Talker_Filter_list.append(unique_Frequency_Talker[unique_Frequency_Talker.index==i])
        print(Talker,Talker_Filter_list)
try:
        
    Talker_Filter_list=pd.concat(Talker_Filter_list)
except ValueError:
    print("Wonderfull no flirting by {}".format(Talker.upper()))
        
try:
    Talker_Filter_list.columns=['Repeated_count','Frequency_Value']
    Talker_Filter_list['Flirt_Frequency']=(Talker_Filter_list['Repeated_count']/len(flirt_words))*100
    Talker_out=Talker_Filter_list['Flirt_Frequency'].sum()/Talker_Filter_list.shape[0]
    print("Flirting Percentage of{}:".format(Talker.upper()), Talker_out,"%")

except AttributeError:
    pass

for i in unique_Frequency_Lesser.index:
    if i in flirt_words:
        Less_Filter_list.append(unique_Frequency_Lesser[unique_Frequency_Lesser.index==i])
        print(Less_Talker,Less_Filter_list)
try:
    Less_Filter_list= pd.concat(Less_Filter_list)
except ValueError:
    print("Wonderfull no flirting by {}".format(Less_Talker.upper()))
    
try:  
    Less_Filter_list.columns=['Repeated_count','Frequency_Value']
    Less_Filter_list['Flirt_Frequency']=(Less_Filter_list['Repeated_count']/len(flirt_words))*100
    Less_out=Less_Filter_list['Flirt_Frequency'].sum()/Less_Filter_list.shape[0]
    print("Flirting Percentage of{}:".format(Less_Talker.upper()), Less_out,"%")

except AttributeError:
    pass

    
    

end = time. time()
print('Execution Time:',end - start)