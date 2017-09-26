from flask import Flask, render_template
import random

app = Flask(__name__)


#Opens file
f = open('occupations.csv','r')

#Reads and closes file
str = f.read();
f.close()

#Creates list of file lines
li = str.replace('\r',"").split('\n')
linested = []


#Creates nested list of file lines and their commas
for element in li:
    linested.append(element.split(','))
linested.remove(linested[len(linested)-1])

normal_val = len(linested[0])

#Parses through linested and takes care of any falsely spliced commas that are in between quotes
index1 = 0
while index1 < len(linested):
    current = linested[index1]
    if current[0][0] == '"':
        while len(current) > normal_val:
            current[0] = current[0].replace('"','') + ',' + current[1].replace('"','')
            current.remove(current[1])
    index1 += 1


#Creates "header" to initialize dictionary building
liheader = linested[0]
linested.remove(linested[0])
#print liheader
#print linested



#Builds dictionary!
DATA = {}
for sublist in linested:
    lookup = {}
    index = 1
    while index < len(liheader):
        try:
            lookup[liheader[index]]=float(sublist[index])
        except Exception as e:
            lookup[liheader[index]]=sublist[index]
        index += 1
        DATA[sublist[0]] = lookup
        
#print 'This is the dictionary!'
#print DATA


#Random selection
def random_job():
    random_selection = random.uniform(0,99.8)
    #print random_selection
    where_i_am = 0.0
    for key in DATA:
        where_i_am += DATA[key]['Percentage']
        #print where_i_am
        if(where_i_am >= random_selection):
            return key
            break

@app.route('/')
def root():
    print 'Root Accessed'
    return '<center>get a job you bum</center>'

@app.route('/occupations')
def occupations():
    percentages = []
    for key in DATA:
        percentages.append(DATA[key]['Percentage'])
        
    print 'Occupations page accessed'
    return render_template('occupations.html',foo=DATA,job_select=random_job())


    
if __name__ == '__main__':
    app.debug = True
    app.run()
    
        
