import os
import sys
from flask import Flask,render_template, url_for,redirect, session, request
from flask import request,jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import mysql.connector
from datetime import timedelta
import datetime




app = Flask(__name__)
bcrypt = Bcrypt(app)


#mongodb
client = MongoClient("mongodb://127.0.0.1:27017")
mydb = client['CovidSEA']
mycol = mydb['Covid19SEAdata']
app = Flask('2103proj')

#mariadb
mydb = mysql.connector.connect(host="localhost",
                                   user="root",
                                   password="0415",
                                   database="covid_sea_proj")


# displays fifth page
@app.route("/fifthpage")
def fifthpage():
    mycursor = mydb.cursor()
    mycursor2 = mydb.cursor()
    
    # Number of ICU and Hospitalized patients out of all new cases
    mycursor.execute(
        "select c.country_name, d.date, h.hosp_patients, n.new_cases from country c, date d, cases_and_death n, hospital_admission h where c.country_id = n.country_id and c.country_id = h.country_id and d.date_id = h.date_id and d.date_id = n.date_id and d.date_id = h.date_id")
    result = mycursor.fetchall()

    mycursor2.execute("SELECT SUM(c.total_deaths) FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
    result2 = mycursor2.fetchall()

    totaldeaths = []
    for row4 in result2:
            totaldeaths.append(str(row4[0]))

    # Covid-19 Cases for each SEA country to date
    ICUDates = list()
    SingaporeICUDict = {}
    BruneiICUDict = {}
    MyanmarICUDict = {}
    MalaysiaICUDict = {}
    CambodiaICUDict = {}
    PhillipinesICUDict = {}
    VietnamICUDict = {}
    TimorICUDict = {}
    ThailandICUDict = {}
    LaosICUDict = {}
    IndonesiaICUDict = {}
    SEAICUDict = {}
    WeeklyVal = list()
    SEAWeeklyVal = {}
    SingaporeWeeklyVal = {}
    BruneiWeeklyVal = {}
    MyanmarWeeklyVal = {}
    MalaysiaWeeklyVal = {}
    CambodiaWeeklyVal = {}
    PhilippinesWeeklyVal = {}
    VietnamWeeklyVal = {}
    TimorWeeklyVal = {}
    ThailandWeeklyVal = {}
    LaosWeeklyVal = {}
    IndonesiaWeeklyVal = {}
    for row in result:
        day = row[1].day
        month = row[1].month
        year = row[1].year
        isoDate = datetime.datetime(year,month,day).isocalendar()
        firstDay = datetime.date.fromisocalendar(isoDate.year, isoDate.week, 7)
        if str(isoDate.week)+ str(row[1].year) in WeeklyVal:
            SEAWeeklyVal[str(firstDay)] += row[3]
        else:
            SEAWeeklyVal[str(firstDay)] = row[3]
            WeeklyVal.append(str(isoDate.week)+
                             str(row[1].year))
        if row[1] in ICUDates:
            # SEAHosp[str(row[1])] += row[2]
            SEAICUDict[str(row[1])] += row[3]
        else:
            ICUDates.append(row[1])
            # SEAHosp[str(row[1])] = row[2]
            SEAICUDict[str(row[1])] = row[3]
        if row[0] == "Singapore":
            SingaporeICUDict[str(row[1])] = row[3]
            if str(firstDay) in SingaporeWeeklyVal:
                SingaporeWeeklyVal[str(firstDay)] += row[3]
            else:
                SingaporeWeeklyVal[str(firstDay)] = row[3]

        elif row[0] == "Brunei":
            BruneiICUDict[str(row[1])] = row[3]
            if str(firstDay) in BruneiWeeklyVal:
                BruneiWeeklyVal[str(firstDay)] += row[3]
            else:
                BruneiWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Myanmar":
            MyanmarICUDict[str(row[1])] = row[3]
            if str(firstDay) in MyanmarWeeklyVal:
                MyanmarWeeklyVal[str(firstDay)] += row[3]
            else:
                MyanmarWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Malaysia":
            MalaysiaICUDict[str(row[1])] = row[3]
            if str(firstDay) in MalaysiaWeeklyVal:
                MalaysiaWeeklyVal[str(firstDay)] += row[3]
            else:
                MalaysiaWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Cambodia":
            CambodiaICUDict[str(row[1])] = row[3]
            if str(firstDay) in CambodiaWeeklyVal:
                CambodiaWeeklyVal[str(firstDay)] += row[3]
            else:
                CambodiaWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Philippines":
            PhillipinesICUDict[str(row[1])] = row[3]
            if str(firstDay) in PhilippinesWeeklyVal:
                PhilippinesWeeklyVal[str(firstDay)] += row[3]
            else:
                PhilippinesWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Vietnam":
            VietnamICUDict[str(row[1])] = row[3]
            if str(firstDay) in VietnamWeeklyVal:
                VietnamWeeklyVal[str(firstDay)] += row[3]
            else:
                VietnamWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Timor":
            TimorICUDict[str(row[1])] = row[3]
            if str(firstDay) in TimorWeeklyVal:
                TimorWeeklyVal[str(firstDay)] += row[3]
            else:
                TimorWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Thailand":
            ThailandICUDict[str(row[1])] = row[3]
            if str(firstDay) in ThailandWeeklyVal:
                ThailandWeeklyVal[str(firstDay)] += row[3]
            else:
                ThailandWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Laos":
            LaosICUDict[str(row[1])] = row[3]
            if str(firstDay) in LaosWeeklyVal:
                LaosWeeklyVal[str(firstDay)] += row[3]
            else:
                LaosWeeklyVal[str(firstDay)] = row[3]
        elif row[0] == "Indonesia":
            IndonesiaICUDict[str(row[1])] = row[3]
            if str(firstDay) in IndonesiaWeeklyVal:
                IndonesiaWeeklyVal[str(firstDay)] += row[3]
            else:
                IndonesiaWeeklyVal[str(firstDay)] = row[3]
    return render_template("fifthpage.html",
                           SingaporeICUDict=SingaporeICUDict,
                           BruneiICUDict=BruneiICUDict, MyanmarICUDict=MyanmarICUDict,
                           MalaysiaICUDict=MalaysiaICUDict,
                           CambodiaICUDict=CambodiaICUDict, PhillipinesICUDict=PhillipinesICUDict,
                           VietnamICUDict=VietnamICUDict, TimorICUDict=TimorICUDict,
                           ThailandICUDict=ThailandICUDict, LaosICUDict=LaosICUDict,
                           IndonesiaICUDict=IndonesiaICUDict, SEAICUDict=SEAICUDict,
                           SEAWeeklyVal = SEAWeeklyVal,SingaporeWeeklyVal=SingaporeWeeklyVal,
                           BruneiWeeklyVal=BruneiWeeklyVal, MyanmarWeeklyVal=MyanmarWeeklyVal,
                           MalaysiaWeeklyVal=MalaysiaWeeklyVal,
                           CambodiaWeeklyVal=CambodiaWeeklyVal, PhilippinesWeeklyVal=PhilippinesWeeklyVal,
                           VietnamWeeklyVal=VietnamWeeklyVal, TimorWeeklyVal=TimorWeeklyVal,
                           ThailandWeeklyVal=ThailandWeeklyVal, LaosWeeklyVal=LaosWeeklyVal,
                           IndonesiaWeeklyVal=IndonesiaWeeklyVal, totaldeaths = totaldeaths
                           )


#displays fourth page
@app.route("/fourthpage")
def fourthpage():
 

    mycursor = mydb.cursor()
    mycursor2 = mydb.cursor()
    mycursor3 = mydb.cursor()
    # mycursor3 = mydb.cursor()
    # mycursor4 = mydb.cursor()

    # Daily Confirmed Cases
    mycursor.execute(
        "SELECT t.country_name, c.new_cases, d.date FROM cases_and_death c ,date d, country t WHERE t.country_id = c.country_id and c.date_id = d.date_id")
    result = mycursor.fetchall()

    # Daily Confirmed Deaths
    mycursor2.execute(
        "SELECT t.country_name, c.new_deaths, d.date FROM cases_and_death c ,date d, country t WHERE t.country_id = c.country_id and c.date_id = d.date_id")
    result2 = mycursor2.fetchall()

    mycursor3.execute("SELECT SUM(c.total_deaths) FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
    result3 = mycursor3.fetchall()
        #total deaths to date label
    totaldeaths = []
    for row4 in result3:
            totaldeaths.append(str(row4[0]))


    # Covid-19 Cases for each SEA country to date
    Coviddates = list()
    SingaporeDict = {}
    BruneiDict = {}
    MyanmarDict = {}
    MalaysiaDict = {}
    CambodiaDict = {}
    PhillipinesDict = {}
    VietnamDict = {}
    TimorDict = {}
    ThailandDict = {}
    LaosDict = {}
    IndonesiaDict = {}
    SEADict = {}
    deathDates = list()
    SingaporeDeaths = {}
    BruneiDeaths = {}
    MyanmarDeaths = {}
    MalaysiaDeaths = {}
    CambodiaDeaths = {}
    PhillipinesDeaths = {}
    VietnamDeaths = {}
    TimorDeaths = {}
    ThailandDeaths = {}
    LaosDeaths = {}
    IndonesiaDeaths = {}
    SEADeaths = {}
    for row in result:
        if row[2] in Coviddates:
            SEADict[str(row[2])] += row[1]
        else:
            Coviddates.append(row[2])
            SEADict[str(row[2])] = row[1]
        if row[0] == "Singapore":
            SingaporeDict[str(row[2])] = row[1]
        elif row[0]=="Brunei":
            BruneiDict[str(row[2])] = row[1]
        elif row[0]=="Myanmar":
            MyanmarDict[str(row[2])] = row[1]
        elif row[0]=="Malaysia":
            MalaysiaDict[str(row[2])] = row[1]
        elif row[0]=="Cambodia":
            CambodiaDict[str(row[2])] = row[1]
        elif row[0]=="Philippines":
            PhillipinesDict[str(row[2])] = row[1]
        elif row[0]=="Vietnam":
            VietnamDict[str(row[2])] = row[1]
        elif row[0]=="Timor":
            TimorDict[str(row[2])] = row[1]
        elif row[0]=="Thailand":
            ThailandDict[str(row[2])] = row[1]
        elif row[0]=="Laos":
            LaosDict[str(row[2])] = row[1]
        elif row[0]=="Indonesia":
            IndonesiaDict[str(row[2])] = row[1]

    for row in result2:
        if row[2] in deathDates:
            SEADeaths[str(row[2])] += row[1]
        else:
            deathDates.append(row[2])
            SEADeaths[str(row[2])] = row[1]
        if row[0] == "Singapore":
            SingaporeDeaths[str(row[2])] = row[1]
        elif row[0]=="Brunei":
            BruneiDeaths[str(row[2])] = row[1]
        elif row[0]=="Myanmar":
            MyanmarDeaths[str(row[2])] = row[1]
        elif row[0]=="Malaysia":
            MalaysiaDeaths[str(row[2])] = row[1]
        elif row[0]=="Cambodia":
            CambodiaDeaths[str(row[2])] = row[1]
        elif row[0]=="Philippines":
            PhillipinesDeaths[str(row[2])] = row[1]
        elif row[0]=="Vietnam":
            VietnamDeaths[str(row[2])] = row[1]
        elif row[0]=="Timor":
            TimorDeaths[str(row[2])] = row[1]
        elif row[0]=="Thailand":
            ThailandDeaths[str(row[2])] = row[1]
        elif row[0]=="Laos":
            LaosDeaths[str(row[2])] = row[1]
        elif row[0]=="Indonesia":
            IndonesiaDeaths[str(row[2])] = row[1]

    return render_template("fourthpage.html", SingaporeDict=SingaporeDict,
                           BruneiDict=BruneiDict, MyanmarDict=MyanmarDict, MalaysiaDict=MalaysiaDict,
                           CambodiaDict=CambodiaDict,PhillipinesDict=PhillipinesDict, VietnamDict=VietnamDict,
                           TimorDict=TimorDict, ThailandDict=ThailandDict, LaosDict=LaosDict,
                           IndonesiaDict=IndonesiaDict, SEADict=SEADict,
                           SingaporeDeaths=SingaporeDeaths,
                           BruneiDeaths=BruneiDeaths, MyanmarDeaths=MyanmarDeaths, MalaysiaDeaths=MalaysiaDeaths,
                           CambodiaDeaths=CambodiaDeaths, PhillipinesDeaths=PhillipinesDeaths,
                           VietnamDeaths=VietnamDeaths,TimorDeaths=TimorDeaths,
                           ThailandDeaths=ThailandDeaths, LaosDeaths=LaosDeaths,
                           IndonesiaDeaths=IndonesiaDeaths, SEADeaths=SEADeaths,totaldeaths=totaldeaths
                           )


#displays third page
@app.route("/thirdpage")

def thirdpage():
   mycursor = mydb.cursor()
   mycursor2 = mydb.cursor()
   mycursor3 = mydb.cursor()
   mycursor4 = mydb.cursor()

  #Percentage of population vaccinated for each SEA country to date
   mycursor.execute("SELECT DISTINCT c.country_name,p.persons_fully_vaccinated, ci.population FROM country_information ci, country c, vaccination p , date d WHERE c.country_id = ci.country_id AND p.country_id = c.country_id AND d.date IN (SELECT MAX(date) FROM date)")
   result = mycursor.fetchall()

  #SUM Total confirmed cases
   mycursor2.execute("SELECT SUM(c.total_cases) FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
   result2 = mycursor2.fetchall()

    #SUM of Total number of people vaccinated in each SEA country to date
   mycursor3.execute("SELECT SUM(persons_fully_vaccinated), MAX(date) FROM vaccination, date")
   result3 = mycursor3.fetchall()



    #SUM total deaths to date. 
   mycursor4.execute("SELECT SUM(c.total_deaths) FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
   result4 = mycursor4.fetchall() 
  
  #Percentage of population vaccinated for each SEA country to date
   populationvaccinated = list()
   
   for row in result:
        populationvaccinated.append(row)


  #total confirmed cases
   confirmedcases = []
   for row2 in result2:
       confirmedcases.append(str(row2[0]))

    #total vaccinated in SEA
   vaccinatedSEA = []
   for row3 in result3:
        vaccinatedSEA.append(str(row3[0]))

     #total deaths to date label
   totaldeaths = []
   for row4 in result4:
        totaldeaths.append(str(row4[0]))


   return render_template("thirdpage.html" ,totaldeaths=totaldeaths, 
       vaccinatedSEA=vaccinatedSEA, confirmedcases=confirmedcases, populationvaccinated=populationvaccinated)



#display 2nd page
@app.route("/secondpage")
def secondpage():
   mycursor = mydb.cursor()
   mycursor1 = mydb.cursor()
   mycursor2 = mydb.cursor()
   mycursor3 = mydb.cursor()
   mycursor4 = mydb.cursor()

    #Percentage of cases and death within population to date
   mycursor.execute("SELECT DISTINCT cc.country_name, c.total_deaths, c.total_cases, ci.population, d.date FROM cases_and_death c, date d, country cc, country_information ci WHERE ci.country_id = c.country_id AND cc.country_id = c.country_id AND c.date_id = d.date_id AND d.date IN (SELECT max(date) FROM date)")
   result = mycursor.fetchall()

        #Total number of people vaccinated in each SEA country to date
   mycursor1.execute("SELECT c.country_name, p.persons_fully_vaccinated FROM country c, vaccination p WHERE c.country_id = p.country_id")
   result1 = mycursor1.fetchall()

    #SUM Total confirmed cases
   mycursor2.execute("SELECT SUM(c.total_cases) FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
   result2 = mycursor2.fetchall()

    #SUM of Total number of people vaccinated in each SEA country to date
   mycursor3.execute("SELECT SUM(persons_fully_vaccinated), MAX(date) FROM vaccination, date")
   result3 = mycursor3.fetchall()

    #SUM total deaths to date. 
   mycursor4.execute("SELECT SUM(c.total_deaths) FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
   result4 = mycursor4.fetchall() 
    
   #total confirmed cases
   confirmedcases = []
   for row2 in result2:
       confirmedcases.append(str(row2[0]))

    #total vaccinated in SEA
   vaccinatedSEA = []
   for row3 in result3:
        vaccinatedSEA.append(str(row3[0]))

     #total deaths to date label
   totaldeaths = []
   for row4 in result4:
        totaldeaths.append(str(row4[0]))


  #Total number of people vaccinated in each SEA country to date
   totalvaccine= list()
   
   for row1 in result1:
        totalvaccine.append(row1)

    
  #Percentage of cases and death within population to date
   casesanddeathpopulation = list()
   for row in result:
        casesanddeathpopulation.append(row)

   return render_template("secondpage.html" , casesanddeathpopulation =  casesanddeathpopulation, totalvaccine=totalvaccine,totaldeaths=totaldeaths, 
       vaccinatedSEA=vaccinatedSEA, confirmedcases=confirmedcases)


#create account
@app.route("/createaccount" , methods=['POST', 'GET'])
def createaccount():
        msg=''
        if request.method == 'POST' and 'username' in request.form and 'password'  in request.form:
              # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            pw_hash = bcrypt.generate_password_hash(password)
            
            cursor = mydb.cursor()

            cursor.execute('INSERT INTO accounts VALUES (%s, %s)', (username, pw_hash))
            mydb.commit()            
            msg = 'You have successfully registered!'
            return redirect("login")
        return render_template("createaccount.html", msg=msg , )

#update account password
@app.route("/updatepassword" , methods=['POST', 'GET'])
def updatepassword():
        msg=''
        if request.method == 'POST' and 'newpassword' in request.form:
            username = session.get('username', None)
            password = request.form['newpassword']
            hashpass = bcrypt.generate_password_hash(password)
            print(password)
            cursor = mydb.cursor()
            cursor.execute('UPDATE accounts set password = %s where username = %s', (hashpass, username))
            mydb.commit()
            msg = 'You have successfully updated password!'
            return redirect("login")
        return render_template("updatepassword.html", msg=msg)

#delete account
@app.route("/deleteaccount" , methods=['POST', 'GET'])
def deleteaccount():
        msg=''
        if request.method == 'POST' and session.get('username'):
            username = session.get('username', None)
            print(username)
            cursor = mydb.cursor()
            cursor.execute('DELETE FROM accounts where username = "'+username+'"')
            mydb.commit()
            msg = 'You have successfully deleted account!'
            return redirect("login")
        return render_template("deleteaccount.html", msg=msg)


#onload page
@app.route("/")
def default():


    return render_template('login.html')

#handles login form request 
@app.route("/login" , methods=['POST', 'GET'])
def login():
    msg =''
    #if form send request store form in username and password variable
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        # cursor = mydb.cursor()
        cursor1 = mydb.cursor()
        
        # cursor.execute('SELECT * FROM accounts where username=%s AND password =%s', (username, password))
        cursor1.execute('SELECT password FROM accounts where username="'+username+'"')
        record1 = cursor1.fetchone()
        
        # record = cursor.fetchone()
        
        #if record exists in database, direct to index page. 
        if record1 and bcrypt.check_password_hash(record1[0],password): 

            #if account exists in database go to index.html
          return redirect( url_for('index' , username=username))
        else:
         msg = 'incorrect password/username'
          

    return render_template('login.html', msg=msg)



#display index.html 
#created this so that when click on pagenation , it will link back to index.html
@app.route("/index")
def index():


 
    mycursor = mydb.cursor()
    mycursor1 = mydb.cursor()
    mycursor2 = mydb.cursor()

    mycursor5 = mydb.cursor()
    mycursor6 = mydb.cursor()


    
    #SUM Total confirmed cases
    mycursor6.execute("SELECT SUM(c.total_cases) FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
    result6 = mycursor6.fetchall()

    #SUM of Total number of people vaccinated in each SEA country to date
    mycursor5.execute("SELECT SUM(persons_fully_vaccinated), MAX(date) FROM vaccination, date")
    result5 = mycursor5.fetchall()



    #SUM total deaths to date. 
    mycursor2.execute("SELECT SUM(c.total_deaths) FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
    result2 = mycursor2.fetchall()
    

    #total deaths to total case query 
    mycursor1.execute("SELECT cc.country_name, c.total_cases, c.total_deaths FROM cases_and_death c, country cc, date d WHERE cc.country_id = c.country_id and c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
    result1 = mycursor1.fetchall()

    # # Fetching Data From mysql to my python progame
    #total confirmed cases to date query 
    mycursor.execute("SELECT c.total_cases,date FROM cases_and_death c, date d WHERE c.date_id = d.date_id and d.date IN (SELECT max(date) FROM date)")
    result = mycursor.fetchall()

    #Sum of total confirmed cases
    confirmedcases = []
    for row7 in result6:
       confirmedcases.append(str(row7[0]))




    #total vaccinated in SEA
    vaccinatedSEA = []
    for row6 in result5:
        vaccinatedSEA.append(str(row6[0]))

    #total deaths to date label
    totaldeaths = []
    for row2 in result2:
        totaldeaths.append(str(row2[0]))

    #labels for total death and total case
    labelstotaldeathandtotalcase = list()
    #for each row in the sql statement append it into label's list. 
    for row1 in result1:
      labelstotaldeathandtotalcase.append(row1)
 


   #declare the labels you want to display in the graph
    labels = list()
    #for each row in the sql statement append it into label's list. 
    for row in result:
      labels.append(row)

    #declare the values you want to display in the graph 
    values = list()
    i = 0
    
    #for each row in sql statement , append it to value's list
    for row in result:
       values.append(row[i])
    print(values)
   

    username = request.args.get('username', None)
    session['username'] = username;
    # Connecting to mysql database
    return render_template("index.html", values=values , labels=labels, labelstotaldeathandtotalcase=labelstotaldeathandtotalcase, totaldeaths=totaldeaths, 
       vaccinatedSEA=vaccinatedSEA, confirmedcases=confirmedcases, username = username
   
    )
@app.route('/viewprofile')
def viewprofile():

    #username session
    # username = request.args.get('username', None)
    username = session.get('username', None)
    return render_template("viewprofile.html", username = username)
    


#mongo db 
@app.route('/showData')
def showData():
    showDataList = []
    for i in mycol.find({},{"total_deaths":19265.0}):
        showDataList.append(i)
  
    return jsonify(showDataList)


# mongo db
# @app.route('/showData', methods=['GET'])
# def index():
    # cur.execute("select t.total_cases from cases_and_death t, date d where d.date_id = t.date_id and date = '19/9/2022'")
    # data = cur.fetchall()
    # # return render_template('maria.html', values=data)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)




