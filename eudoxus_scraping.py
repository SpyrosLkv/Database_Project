from tkinter import Y
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import random

from selenium.webdriver.common.keys import Keys
import time

import urllib.request


PATH="C:\Program Files (x86)\chromedriver.exe";
driver = webdriver.Chrome(PATH);
driver.get("https://service.eudoxus.gr/public/departments/courses/1482/2022")
elements = driver.find_elements_by_xpath("//a")


books = []


i = 0
for element in elements:
    element.click()
    book = []
    time.sleep(5)
    #try:
    #    table = WebDriverWait(driver, 10).until(
    #        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "table.search-resultsTable"))
    #    )
    #except:
    #    continue
    try:    
        table = driver.find_element_by_css_selector("table.search-resultsTable")
    except:
        driver.back()
        continue
    rows = table.find_elements_by_tag_name("tr")
    for index, row in enumerate(rows):
        if index in [0,2,3,6]:
            continue;
        cells = row.find_elements_by_tag_name("td")
        for cell in cells:
            text = cell.text
            print(text)
            if ":" in text:
                text = text.split(":")[1]
            while(True):
                if text[0] == ' ':
                    text = text[1:]
                else:
                    break;
            book.append(text);
            # μορφή: [τίτλος, συγγραφείς, ISBN, ,εκδότες]

    button = driver.find_element_by_xpath('//div[@class="gwt-Label search-hyperlink"]')
    button.click()
    time.sleep(1)

    # <img src="https://static.eudoxus.gr/books/preview/https://static.eudoxus.gr/books/60/cover-94644160.jpg" class="gwt-Image search-popup-image">
    img_element = driver.find_element_by_xpath('//img[@class="gwt-Image search-popup-image"]')
    # img_element = driver.find_element_by_css_selector('img.gwt-Image search-popup-image')
    img_src = img_element.get_attribute("src")

    image_url = img_src
    local_filename = "C:/Users/codad/Desktop/GitHub/Database_Project/images/image"+str(i)+".png"
    urllib.request.urlretrieve(image_url,local_filename)

    books.append(book)
    driver.back()
    i +=1
    if i == 450: 
        break;

# μέχρις στιγμής έχω πάρει όλα τα βιβλία και τα στοιχεία τους
# τώρα θα σπάσω τους συγγραφείς σε διαφορετικά ονόματα

for index, book in enumerate(books):
    authors = book[1]

    authors = authors.split(",");
    if type(authors) == str:
        authors = [authors]

    authors_correct = []
    for name in authors:

        while name[0] == " ":
            name = name[1:]
        while name[-1] == " ":
            name = name[:len(name)-2]
        authors_correct.append(name)
    books[index][1] = authors_correct

## Θα ανοίξω το dml και θα βάλω τα Inserts για βιβλία
filename = "dml_of_semester.sql"
file = open(filename, "w", encoding="UTF-8")
file.truncate(0)

filename = "random_summary.txt"
summary_file =open(filename, "r")
summary_text = summary_file.read()
for book in books:
    ISBN = book[2]
    title = book[0]
    publisher = book[3]
    no_of_pages = random.randint(200,1200)
    start = random.randint(0,len(summary_text)-100)
    summary = summary_text[start:start+30]
    summary = summary.replace("\n","")
    language = random.choice(["Ελληνικά","English"])
    query = "INSERT INTO semester_project.Book (ISBN,title,publisher,no_of_pages,summary,`language`) VALUES ( " + str(ISBN) + ",\"" + title + "\",\"" + publisher + "\"," + str(no_of_pages) + ",\"" + summary + "\",\"" + language + "\");\n"
    file.write(query)

## εδώ θα κάνω insert τους authors και τα wrote
list_of_last_names = []
for book in books:
    ISBN = book[2]
    authors = book[1];

    first_name = ""
    last_name = ""

    for author in authors:
        author.lower()
        words = author.split(' ')

        ## if there is only one name
        if type(words)==str:
            if words not in list_of_last_names:
                list_of_last_names.append(words)
                first_name = words
                last_name = "Bateman"
                query = "INSERT INTO semester_project.Authors (first_name,last_name) VALUES ( \"" + first_name + "\",\"" + last_name +"\");\n"
                file.write(query);
            index = list_of_last_names.index(words)+1
            query = "INSERT INTO semester_project.Wrote (author_id,book_ISBN) VALUES ( " + str(index) + "," + str(ISBN) + ");\n"
            file.write(query)
            continue


        words = [words[0],words[-1]]
        if words[0] in list_of_last_names:
            words = words.reverse()
        elif words[1] not in list_of_last_names:
            list_of_last_names.append(words[1])
        
            first_name = words[0]
            last_name = words[1]
            query = "INSERT INTO semester_project.Authors (first_name,last_name) VALUES ( \"" + first_name + "\",\"" + last_name +"\");\n"
            file.write(query);
        index = list_of_last_names.index(words[1])+1
        query = "INSERT INTO semester_project.Wrote (author_id,book_ISBN) VALUES ( " + str(index) + "," + str(ISBN) + ");\n"
        file.write(query)

## insert στα keywords
keywords = ["Προγραμματισμός", "Μαθηματικά", "Μηχανική", "Ηλεκτρομαγνητικά Πεδία", "Ανώτερη Φυσική", "Ενέργεια", "Δίκτυα", "Ανθρωπιστικά"]
for word in keywords:
    query = "INSERT INTO semester_project.Keywords (keyword) VALUES ( \"" + word + "\");\n"
    file.write(query)

## insert στα keywords in book
dromeas = 0
for book in books:
    ISBN = book[2]
    no_of_keys = random.randint(1,3)
    for i in range(1,no_of_keys+1):
        dromeas = (dromeas+1)%len(keywords)
        query = "INSERT INTO semester_project.Keywords_in_book (keyword_id,book_ISBN) VALUES ( \"" + keywords[dromeas] + "\"," + str(ISBN) + ");\n"
        file.write(query)

thematic_categories = ["Romance","Mystery","Thriller","Science Fiction","Fantasy","Historical Fiction","Horror","Biography/Memoir","Self-help","Travel","Business","Education","Poetry"]
for category in thematic_categories:
    query = "INSERT INTO semester_project.Thematic_Category (category) VALUES ( \"" + category + "\");\n"
    file.write(query)

dromeas = 0
for book in books:
    ISBN = book[2]
    no_of_themes = random.randint(1,3)
    for i in range(1,no_of_themes+1):
        dromeas = (dromeas+1)%len(thematic_categories)
        query = "INSERT INTO semester_project.Belongs_in (category_id,book_ISBN) VALUES ( \"" + thematic_categories[dromeas] + "\"," + str(ISBN) + ");\n"
        file.write(query)



file.close();

file = open("all_the_isbn.txt", "w")
for book in books:
    string = str(book[2])+"\n"
    file.write(string)
file.close()
    
    

driver.quit()