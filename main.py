import spacy
import json

import random

from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer

import sqlite3

import warnings
warnings.filterwarnings("ignore")

nlp = spacy.load('en')

#doc = nlp(u'balance')

strings = [ u'What is my current balance',
            u'What is my balance',
            u'Tell me my balance',
            u'How much balance do I have',
            u'How much money I have',
            u'Check balance',
            u'Give my last transactions details',
            u'Give my account statement',
            u'Give me my mini statement',
            u'Generate my mini statement',
            u'Generate my account statement',
            u'Tell me my last transactions details']

##for string in strings:
##    print(doc.similarity(nlp(string)))


##create a dictionary according to documentation of the rasa_nlu and dump the values of it in json file
##write the strings in json format
##have to edit the json file manually later,as all enteries will not be correct

##data = []
##for i in range(6):
##    data.append({})
##    data[i]["text"] = strings[i]
##    data[i]["intent"] = "check_balance"
##    check = ["balance","money"]
##    for c in check:
##        if strings[i].find(c) == -1:
##            continue
##        start = strings[i].find(c)
##        end = start + len(c)
##        value = c
##        
##    data[i]["entities"] = [{"start":start,
##                            "end":end,
##                            "value":value,
##                            "entity":"balance"
##                            }
##                           ]
##
##for i in range(6,len(strings)):
##    data.append({})
##    data[i]["text"] = strings[i]
##    data[i]["intent"] = "account_statement"
##    check = ["transactions","statement"]
##    for c in check:
##        if strings[i].find(c) == -1:
##            continue
##        start = strings[i].find(c)
##        end = start + len(c)
##        value = c
##        
##    data[i]["entities"] = [{"start":start,
##                            "end":end,
##                            "value":value,
##                            "entity":"statement"
##                            }
##                           ]

##with open("training_data2.json",'w') as fp:
##    for d in data:
##        json.dump(d,fp)

def train():
    pipeline = "tensorflow_embedding"

    args = {"pipeline":pipeline}
    config = RasaNLUModelConfig(args)
    trainer = Trainer(config)

    training_data = load_data("training_data2.json")
    interpreter = trainer.train(training_data)
    return interpreter
#print(json.dumps(data[1], indent=2))

#print(interpreter.parse(strings[1]))

interpreter = train()

conn = sqlite3.connect('banks.db')
c = conn.cursor()

##for i in range(len(strings)):
##    data = interpreter.parse(strings[i])
##    for ent in data["intent"]:
##        Class = ent["name"]
##    print(data["intent"]["name"])
##    print(data)
##params = {}

##for ent in data["intent"]:
    ##Class = ent["name"]
    ##params[ent["entity"]] = ent["value"]

##print(params)

def response(message):
    data = interpreter.parse(message)
    #print(data)
    if(len(data["entities"])==0):
        Class = data["intent"]["name"]
    #print(data)
        #print(Class)
        if Class == 'check_balance':
            query = "SELECT Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 1"
            c.execute(query)
            responses = ["Your balance is Rs.{}" ,"You have Rs.{} in your account"]
            results = c.fetchall()
            #print(results)
            #index = min(len(results),len(responses)-1)
            print("Bot: "+random.choice(responses).format(list(*results)[0]))

        if Class == 'account_statement':
            query = "SELECT TimeStamp,Type,Amount,Location,Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 5"
            c.execute(query)
            results = c.fetchall()
            balance = results[0][4]
            n = len(results)
            for i in range(n):
                print str(results[i][0])+" "+str(results[i][1])+" "+str(results[i][2])+" "+str(results[i][3])
            print "Current balance is Rs.",balance
        #print(results)
        if Class == 'about_bot':
            print "Bot: " + random.choice(["My name is Giannini-The Bank Bot","You can call me Giannini-The Bank Bot"])

        if Class == 'work_bot':
            print "Bot: " + random.choice(["I am here to help you. I can fetch your account and transaction details","I am here to assist you by providing easier access to your account details"])

        if Class == 'greet':
            print "Bot: " + random.choice(["Hi! there","Hello! There","Hi","Hello"])

    else:
        dic = data["entities"][0]
        if(dic["confidence"]<0.5):
            print("Sorry, I didn't understand the question :(")
        else:
            Class = dic["entity"]
            if Class == 'money':
                query = "SELECT Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 1"
                c.execute(query)
                responses = ["Your balance is Rs.{}" ,"You have Rs.{} in your account"]
                results = c.fetchall()
                #print(results)
                index = min(len(results),len(responses)-1)
                print("Bot: "+random.choice(responses).format(list(*results)[0]))
            elif Class == 'statement':
                query = "SELECT TimeStamp,Type,Amount,Location,Balance FROM Bank ORDER BY TimeStamp DESC LIMIT 5"
                c.execute(query)
                results = c.fetchall()
                balance = results[0][4]
                n = len(results)
                for i in range(n):
                    print str(results[i][0])+" "+str(results[i][1])+" "+str(results[i][2])+" "+str(results[i][3])
                print "Current balance is Rs.",balance
        #print(results)
            elif Class == 'about_bot':
                print "Bot: " + random.choice(["My name is Giannini-The Bank Bot","You can call me Giannini-The Bank Bot"])
            elif Class == 'work_bot':
                print "Bot: " + random.choice(["I am here to help you. I can fetch your account and transaction details","I am here to assist you by providing easier access to your account details"])
            elif Class == 'greet':
                print "Bot: " + random.choice(["Hi! there","Hello! There","Hi","Hello"])
            else:
                print "Bot: " + random.choice(["Sorry, I didn't understand the question :(","I don't know the answer for this"])
##for i in range(len(strings)):
##    print(i)
##    response(strings[i])
##esponse(u'hey')