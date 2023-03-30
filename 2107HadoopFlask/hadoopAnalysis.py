import os
import sys
from flask import Flask,render_template, url_for,redirect, session, request
from flask import request,jsonify
from datetime import timedelta
import datetime
import json
import os
from collections import Counter
from wordcloud import WordCloud
from io import BytesIO
import base64
import random



app = Flask(__name__)
RESULTS_DIRECTORY = os.path.join(".", "hadoop_analysis", "Results")
COMPANY_DIRECTORY = os.path.join(".", "data","Company Information" ,"Company_Information.json")

companypath = os.path.join(COMPANY_DIRECTORY)

# appends companies information to data object, using list of companies in an industry
def append_company_info(data, coyinfo,coydata,companies):
    i = 0;
    while i<len(coyinfo):
        if coyinfo[i] in companies:
            data[coyinfo[i]]['information'] = coydata[coyinfo[i]]['employer_description']
            data[coyinfo[i]]['contact'] = coydata[coyinfo[i]]['website']
            data[coyinfo[i]]['founded'] = coydata[coyinfo[i]]['founded']
            data[coyinfo[i]]['hq'] = coydata[coyinfo[i]]['headquarters']
            data[coyinfo[i]]['size'] = coydata[coyinfo[i]]['size']
            data[coyinfo[i]]['type'] = coydata[coyinfo[i]]['type']
            data[coyinfo[i]]['industry'] = coydata[coyinfo[i]]['industry']
            data[coyinfo[i]]['revenue'] = coydata[coyinfo[i]]['revenue']
            data[coyinfo[i]]['mission'] = coydata[coyinfo[i]]['mission']
        i = i + 1;


# global function for home page. 
def get_reviews_data(path, category):
    with open(path) as f:
        data = json.load(f)
    median_reviews = data[category]["median_reviews"]
    total_reviews = data[category]["total_reviews"]
    one_star_reviews = data[category]["percent_one_star"]
    two_star_reviews = data[category]["percent_two_star"]
    three_star_reviews = data[category]["percent_three_star"]
    four_star_reviews = data[category]["percent_four_star"]
    five_star_reviews = data[category]["percent_five_star"]



    onestar_reviews = data[category]["one_star_reviews"]
    twostar_reviews = data[category]["two_star_reviews"]
    threestar_reviews = data[category]["three_star_reviews"]
    fourstar_reviews = data[category]["four_star_reviews"]
    fivestar_reviews = data[category]["five_star_reviews"]
    return {"median_reviews": median_reviews,
            "total_reviews": total_reviews,
            "one_star_reviews": one_star_reviews,
            "two_star_reviews": two_star_reviews,
            "three_star_reviews": three_star_reviews,
            "four_star_reviews": four_star_reviews,
            "five_star_reviews": five_star_reviews,

            "onestar_reviews":  onestar_reviews,
            "twostar_reviews": twostar_reviews,
            "threestar_reviews": threestar_reviews,
            "fourstar_reviews":  fourstar_reviews,
            "fivestar_reviews":  fivestar_reviews
            
            
            
            }





#displays fourth page
@app.route("/fifthpage")
def fifthpage():
 #populate companies to dropdown list.
    path = os.path.join(RESULTS_DIRECTORY, "Communication Services.json")
    comms_data = get_reviews_data(path, "Communication Services")
    financepath = os.path.join(RESULTS_DIRECTORY, "Financials.json")
    finance_data = get_reviews_data(financepath, "Financials")

    return render_template("fifthpage.html", comms_data = comms_data, finance_data=finance_data
        )


#displays fourth page
@app.route("/fourthpage")
def fourthpage():
     #populate companies to dropdown list.
    path = os.path.join(RESULTS_DIRECTORY, "Information Technology.json")
    IT_data = get_reviews_data(path, "Information Technology")
    industrialspath = os.path.join(RESULTS_DIRECTORY, "Industrials.json")
    industrials_data = get_reviews_data(industrialspath, "Industrials")

    return render_template("fourthpage.html", IT_data = IT_data, industrials_data = industrials_data)

#displays third page
@app.route("/thirdpage")
def thirdpage():
     #populate companies to dropdown list.
    path = os.path.join(RESULTS_DIRECTORY, "Materials.json")
    materials_data = get_reviews_data(path, "Materials")
    institutionpath = os.path.join(RESULTS_DIRECTORY, "Institutions.json")
    institution_data = get_reviews_data(institutionpath, "Institutions")

    return render_template("thirdpage.html", materials_data=materials_data, institution_data = institution_data)

#displays second page
@app.route("/secondpage")
def secondpage():
    #populate companies to dropdown list.
    path = os.path.join(RESULTS_DIRECTORY, "Consumer Discretionary.json")
    consumerdiscretionary_data = get_reviews_data(path, "Consumer Discretionary")

    consumerstaplespath = os.path.join(RESULTS_DIRECTORY, "Consumer Staples.json")
    consumerstaples_data = get_reviews_data(consumerstaplespath, "Consumer Staples")

    healthcarepath = os.path.join(RESULTS_DIRECTORY, "Healthcare.json")
    healthcare_data = get_reviews_data(healthcarepath, "Healthcare")

    return render_template("secondpage.html", consumerdiscretionary_data = consumerdiscretionary_data, consumerstaples_data = consumerstaples_data,
                           healthcare_data=healthcare_data
                           )
@app.route("/")
def index():
    path = os.path.join(RESULTS_DIRECTORY, "Airlines.json")
    airline_data = get_reviews_data(path, "Airlines")

    energypath = os.path.join(RESULTS_DIRECTORY, "Energy.json")
    energy_data = get_reviews_data(energypath, "Energy")

    commspath = os.path.join(RESULTS_DIRECTORY, "Communication Services.json")
    comms_data = get_reviews_data(commspath, "Communication Services")


    financepath = os.path.join(RESULTS_DIRECTORY, "Financials.json")
    finance_data = get_reviews_data(financepath, "Financials")


    materialspath = os.path.join(RESULTS_DIRECTORY, "Materials.json")
    materials_data = get_reviews_data(materialspath, "Materials")


    institutionpath = os.path.join(RESULTS_DIRECTORY, "Institutions.json")
    institution_data = get_reviews_data(institutionpath, "Institutions")


    ITpath = os.path.join(RESULTS_DIRECTORY, "Information Technology.json")
    IT_data = get_reviews_data(ITpath, "Information Technology")


    industrialspath = os.path.join(RESULTS_DIRECTORY, "Industrials.json")
    industrials_data = get_reviews_data(industrialspath, "Industrials")


    consumerdiscretionarypath = os.path.join(RESULTS_DIRECTORY, "Consumer Discretionary.json")
    consumerdiscretionary_data = get_reviews_data(consumerdiscretionarypath, "Consumer Discretionary")


    consumerstaplespath = os.path.join(RESULTS_DIRECTORY, "Consumer Staples.json")
    consumerstaples_data = get_reviews_data(consumerstaplespath, "Consumer Staples")

    
    healthcarepath = os.path.join(RESULTS_DIRECTORY, "Healthcare.json")
    healthcare_data = get_reviews_data(healthcarepath, "Healthcare")

    return render_template("index.html", airline_data = airline_data , energy_data = energy_data,
                            comms_data = comms_data, finance_data= finance_data, materials_data= materials_data,
                             institution_data= institution_data,IT_data=IT_data,industrials_data =industrials_data,
                             consumerdiscretionary_data= consumerdiscretionary_data, consumerstaples_data= consumerstaples_data,
                             healthcare_data=  healthcare_data
                           
                             )




@app.route("/energypage")
def energypage():

    path = os.path.join(RESULTS_DIRECTORY, "Energy.json")
    #get energy json data
    with open(path) as f:
        data = json.load(f)
    #get company data
    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)

    #List of company names
    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Energy"]["word_count_dictionary"]

    #----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Energy"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    #---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph 
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list 
    
    for key, value in word_freq.items():
        word_count_list.append((key, value))

    #---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Energy':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
     #---#this is used for plotting the bar graph for one- five star review----------------------------------

  # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)


    return render_template("EnergyPage.html", companies= companies, data=data,  image_data=img_data, word_count_list = word_count_list, 
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,
                      
                           )


@app.route("/airlinespage")
def airlinespage():

    path = os.path.join(RESULTS_DIRECTORY, "Airlines.json")
    # populate companies to dropdown list.
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
        
    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Airlines"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Airlines"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list
    for key, value in word_freq.items():
        word_count_list.append((key, value))

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Airlines':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]

    append_company_info(data, coyinfo,coydata,companies)

    return render_template("AirlinesPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )






@app.route("/communicationservicespage")
def communicationservicespage():

    path = os.path.join(RESULTS_DIRECTORY, "Communication Services.json")
    # populate companies to dropdown list.
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
   

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Communication Services"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Communication Services"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Communication Services':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("CommunicationsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )






@app.route("/financialspage")
def financialsPage():

    path = os.path.join(RESULTS_DIRECTORY, "Financials.json")
    # populate companies to dropdown list.
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
       
    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Financials"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Financials"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Financials':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("FinancialsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )






@app.route("/healthcarepage")
def healthcarepage():
    
    path = os.path.join(RESULTS_DIRECTORY, "Healthcare.json")
    # populate companies to dropdown list.
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
   

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Healthcare"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Healthcare"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Healthcare':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("HealthcarePage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )


@app.route("/industrialspage")
def industrialspage():
    
    path = os.path.join(RESULTS_DIRECTORY, "Industrials.json")
    # populate companies to dropdown list.
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
        

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Industrials"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Industrials"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Industrials':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    i = 0;
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("IndustrialsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )



@app.route("/informationtechnologypage")
def informationtechnologypage():

    path = os.path.join(RESULTS_DIRECTORY, "Information Technology.json")
    # populate companies to dropdown list.
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
        

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Information Technology"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Information Technology"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Information Technology':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("ITPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )


@app.route("/institutionspage")
def institutionspage():
    path = os.path.join(RESULTS_DIRECTORY, "Institutions.json")
    # populate companies to dropdown list.
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
       

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Institutions"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Institutions"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Institutions':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("InstitutionsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )



@app.route("/materialspage")
def materialspage():
    path = os.path.join(RESULTS_DIRECTORY, "Materials.json")
    # populate companies to dropdown list.
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
        

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Materials"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Materials"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Materials':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("MaterialsPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )


@app.route("/consumerdiscretionarypage")
def consumerdiscretionarypage():
   
# populate companies to dropdown list.
    path = os.path.join(RESULTS_DIRECTORY, "Consumer Discretionary.json")
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
       
      

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Consumer Discretionary"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Consumer Discretionary"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Consumer Discretionary':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("ConsumerDiscretionaryPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )



@app.route("/consumerstaplespage")
def consumerstaplespage():
    # populate companies to dropdown list.
    path = os.path.join(RESULTS_DIRECTORY, "Consumer Staples.json")
    with open(path) as f:
        data = json.load(f)

    with open(companypath, encoding="utf-8") as d:
        coydata = json.load(d)
       

    companies = []
    for key in data:
        company_name = data[key]['name']
        companies.append(company_name)

    # Extract word frequencies
    word_freq = data["Consumer Staples"]["word_count_dictionary"]

    # ----------used for plotting the word cloud---------------------------------
    # Sort word frequencies by count and take top 5
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]

    # Sort top words by value in the JSON
    top_words = sorted(top_words, key=lambda x: data["Consumer Staples"]["word_count_dictionary"][x[0]], reverse=True)

    # Generate word cloud image
    wordcloud = WordCloud(width=800, height=800, background_color="white").generate_from_frequencies(dict(top_words))

    # Get the image as bytes and encode it as base64
    img_bytes = BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_data = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
    # ----------used for plotting the word cloud---------------------------------

    # ---#this is used for plotting the bar graph for word count----------------------------------
    # Create an empty list to store the key-value pairs this is used for plotting the bar graph
    word_count_list = []
    # Iterate through the dictionary and append the key-value pairs to the list

    for key, value in word_freq.items():
        word_count_list.append((key, value))
    # ---#this is used for plotting the bar graph for word count ----------------------------------

    # ---#this is used for plotting the bar graph for one - five star review----------------------------------
    # initialize empty list to store one-star reviews
    one_star_reviews = []
    two_star_reviews = []
    three_star_reviews = []
    four_star_reviews = []
    five_star_reviews = []

    # iterate through each company's data, excluding Energy
    for company, company_data in data.items():
        if company != 'Consumer Staples':
            one_star_reviews.append((company, company_data['one_star_reviews']))
            two_star_reviews.append((company, company_data['two_star_reviews']))
            three_star_reviews.append((company, company_data['three_star_reviews']))
            four_star_reviews.append((company, company_data['four_star_reviews']))
            five_star_reviews.append((company, company_data['five_star_reviews']))
    # ---#this is used for plotting the bar graph for one- five star review----------------------------------

    # Extract the company names from the JSON data and store them in a list
    coyinfo = [coy for coy in coydata.keys()]
    append_company_info(data, coyinfo,coydata,companies)

    return render_template("ConsumerStaplesPage.html", companies=companies, data=data, image_data=img_data,
                           word_count_list=word_count_list,
                           one_star_reviews=one_star_reviews,
                           two_star_reviews=two_star_reviews,
                           three_star_reviews=three_star_reviews,
                           four_star_reviews=four_star_reviews,
                           five_star_reviews=five_star_reviews,

                           )

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)




