import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
import numpy as np 

from tensorflow.keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
pr_model = pickle.load(open('predict_lp_model.sav', 'rb'))
df = pickle.load(open('new_df.sav', 'rb'))
def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list



# def getResponse(ints, intents_json):
#     tag = ints[0]['intent']
# #     if tag=='predict_laptop_price':
# #         ans=predict_price()
# #         ans=ans.reshape(1,-1)
# #         print(int(pr_model.predict(scaler.fit_transform(ans))[0][0]))
#     list_of_intents = intents_json['intents']
#     for i in list_of_intents:
#         if(i['tag']== tag):
#             result = random.choice(i['responses'])
#             break
#     return result

currentQcontext = ""
c_d={'ASUS':0,'Acer':1,'Apple':2,'Dell':3,'HP':4,'Lenovo':5,'MSI':6,'Razer':7}
cn=[0]*8
ram=0
ss=0
st=[0]*3
pt=[]
pd=0
gc=0
wt=0
ops=[0,1,0]
scr=0
lt=[0,0,0,0,0]
ram_d={"4GB RAM":4,"8GB RAM":8,"16GB RAM":16,"24GB RAM":24,"32GB RAM":32}
st_d={'HDD':0,'SSD':1,'HDD+SSD':2}
ss_d={'128': 0, '256': 1, '512': 2, '1024': 3, '256+1024': 4, '128+1024': 5, '512+1024': 6, '256+2048': 7, '512+2048': 8, '2048': 9}
pt_d={"Intel":[0,1],"AMD":[1,0]}
pd_d={'7th Gen i3': 0, 'Ryzen 3': 1, '10th Gen i3': 2, '9th Gen i5': 3, 'Ryzen 5': 4, 'Ryzen 7': 5, '10th Gen i5': 6, '8th Gen i5': 7, '7th Gen i5': 8, '8th Gen i7': 9, '8th Gen i3': 10, '10th Gen i7': 11, '7th Gen i7': 12, '6th Gen i7': 13, '9th Gen i7': 14, '8th Gen i9': 15, '9th Gen i9': 16}
gc_d={'Integrated': 0, '2GB GPU': 1, '4GB GPU': 2, '3GB GPU': 3, 'Dedicated': 4, '6GB GPU': 5, '8GB GPU': 6}
weight_d={"Less than 1 kg":0.9,"1-2 kg":1.5,">2 kg":2.3}
scr_d={"13.3 inches":13.3,"14 inches":14,"15.6 inches":15.6,"17.3 inches":17.3}
# os_d={'DOS':0,'Windows':1,'macOS':2}
lt_d={'Business':0,'Convertible':1,'Gaming':2,'Notebook':3,'Ultrabook':4}
    
userip=[]
look_for_context=False
def chatbot_response(msg):
    global currentQcontext,cn,ram,ss,st,pd,pt,gc,wt,ops,scr,lt,userip,df,look_for_context
    results = predict_class(msg, model)
    print(results)
    if results:
        # loop as long as there are matches to process
        while results:
            for i in intents['intents']:
                # find a tag matching the first result
                if not results:
                    return "Sorry, I didn't understand. Please try again. Thanks"
                if results and i['tag'] == results[0]['intent']:
                    if i['tag']=="predict_laptop_price":
                        look_for_context=True
                        currentQcontext=""
                        userip=[]
                        cn=[0]*8
                        st=[0]*3
                        pt=[]
                        ops=[0,1,0]
                        lt=[0,0,0,0,0]
                    if currentQcontext:
                        print("found: ",currentQcontext)
                        if 'context_filter' in i and i['context_filter']==currentQcontext:
                            if i['tag'] in c_d:
                                cn[c_d[i['tag']]]=1
                            if i['tag'] in ram_d:
                                ram=ram_d[i['tag']]
                            if i['tag'] in st_d:
                                st[st_d[i['tag']]]=1
                            if i['tag'] in ss_d:
                                ss=ss_d[i['tag']]
                            if i['tag'] in pt_d:
                                pt=pt_d[i['tag']]
                            if i['tag'] in pd_d:
                                pd=pd_d[i['tag']]
                            if i['tag'] in gc_d:
                                gc=gc_d[i['tag']]
                            if i['tag'] in weight_d:
                                wt=weight_d[i['tag']]
                            if i['tag'] in scr_d:
                                scr=scr_d[i['tag']]
                            if cn[2]==1:
                                ops[1]=0
                                ops[2]=1
                            if i['tag'] in lt_d:
                                lt[lt_d[i['tag']]]=1
                                
                                
                            if i['context_filter']=="lap_type":
                                currentQcontext=""
                                look_for_context=False
                                userip.append(ram)
                                userip.append(ss)
                                userip.append(pd)
                                userip.append(gc)
                                userip.append(wt)
                                userip.append(scr)
                                userip.extend(cn)
                                userip.extend(st)
                                userip.extend(pt)
                                userip.extend(ops)
                                userip.extend(lt)
                                print(userip)
                                X=df.loc[:,('RAM (GB)','Storage Size (GB)', 'Processor Details',
       'Graphics Card (GB)','Weight (kg)',
       'Screen Size (inches)','Company Name_ASUS',
       'Company Name_Acer', 'Company Name_Apple', 'Company Name_Dell',
       'Company Name_HP', 'Company Name_Lenovo', 'Company Name_MSI',
       'Company Name_Razer', 'Storage Type_HDD', 'Storage Type_SSD',
       'Storage Type_SSD+HDD', 'Processor Company_AMD',
       'Processor Company_Intel', 'OS_DOS', 'OS_Windows', 'OS_macOS',
       'Laptop Type_Business', 'Laptop Type_Convertible', 'Laptop Type_Gaming',
       'Laptop Type_Notebook', 'Laptop Type_Ultrabook')]

                                X.loc[len(X.index)] = userip
                                X=scaler.fit_transform(X)
                                a=X[-1].reshape(1,-1)
                                est_price=int(pr_model.predict(a)[0][0])
                                reply="I guess that would be enough! Give me a second and I'll tell you the estimated price of the laptop with your desried specs\nThe estimated price is INR "+str(est_price)
                                return reply
                                
                            if 'context_set' in i:
                                print("set context to: ",i['context_set'])
                                currentQcontext=i['context_set']
                            return random.choice(i['responses'])
                        else:
                            results.pop(0)
                    if not currentQcontext:
                        if 'context_set' in i and look_for_context:
                            currentQcontext=i['context_set']
                        return random.choice(i['responses'])
    else:
        return "Sorry, I didn't understand. Please try again. Thanks"

                    
