import os
import sys
from flask import Flask,render_template, url_for,redirect, session, request
from flask import request,jsonify
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import mysql.connector
from datetime import timedelta
import datetime
import json
import os


app = Flask(__name__)




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




#onload page
@app.route("/")
def default():


    return render_template('index.html')



#display index.html 
#created this so that when click on pagenation , it will link back to index.html
@app.route("/index")
def index():
    # Load the JSON data
    with open('./hadoop_analysis/Results/Energy.json') as f:
        data = json.load(f)

    # Access the values for the two companies
    anadarko_two_star = data['Anadarko-Petroleum']['two_star_reviews']
    apache_two_star = data['Apache']['two_star_reviews']
    anadarko_five_star_percent = data['Anadarko-Petroleum']['percent_five_star']
    apache_five_star_percent = data['Apache']['percent_five_star']

    # Calculate the sum of two_star_reviews and the average of percent_five_star
    two_star_sum = anadarko_two_star + apache_two_star
    five_star_average = (anadarko_five_star_percent + apache_five_star_percent) / 2
  
    return render_template("index.html", two_star_sum=two_star_sum, five_star_average=five_star_average)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)




