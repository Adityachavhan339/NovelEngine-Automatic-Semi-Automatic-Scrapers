import pandas as pd
import shutil
import os
import requests
from bs4 import BeautifulSoup
import time
import random

print("Starting Data Analysis")
genre = "Fantasy"
genre_url = f"https://freewebnovel.com/genre/{genre}/"
headers = {'User-Agent': 'Mozilla/5.0'}

novel_data = []
print("Starting Data Extraction..")
print("Collecting Data..")
for page_num in range(1,12):
    try:  
       url = genre_url if page_num == 1 else (f"{genre_url}{page_num}")

       print(f"Scrapping Page {page_num}..")
       response = requests.get(url,headers=headers)
       soap = BeautifulSoup(response.text,"lxml")

       raw_novel_data = soap.find_all("div",class_="li")

       for novel in raw_novel_data:
              name = "N/A"
              rating = "N/A"
              chapter = "N/A"

              name_tag = novel.find(class_="tit")
              rating_tag = novel.find(class_="core")
              chapter_tag = novel.find("span",class_="s1")

              if name_tag:
                   name = name_tag.get_text(strip=True)
              if rating_tag:
                   rating = rating_tag.get_text(strip=True)
              if chapter_tag:
                   chapter = chapter_tag.get_text(strip=True)

              novel_data.append({"Name": name,"Rating": rating,"chapter_count": chapter})
       time.sleep(random.uniform(1,4))

    except Exception as e:
          print(e)

print(f"Total Collected Novels {len(novel_data)}")
print("Starting Final Data Organization..")
updated_novel_data = pd.DataFrame(novel_data)

updated_novel_data.to_csv(f"Perfected_Novels_{genre}_Data.csv",index=False)

print("Starting Folder Creation..")
try:
   os.makedirs(f"{genre} Novels",exist_ok=True)
   print(f"Successfully Created Folder {genre} Novels")
except Exception as e:
     print(e)

print("Saving Files..")
print("Moving Files To Safe Folder")
try:
     os.makedirs("Backup_Of_Day",exist_ok=True)
     shutil.copy(f"Perfected_Novels_{genre}_Data.csv","Backup_Of_Day")
     shutil.move(f"Perfected_Novels_{genre}_Data.csv",os.path.join(f"{genre} Novels",f"Perfected_Novels_{genre}_Data.csv"))
     print(f"Operation Successful Saved CSV File At {genre} Novels")
except Exception as e:
     print(e)


data = pd.read_csv(f"{genre} Novels/Perfected_Novels_{genre}_Data.csv")

data["Rating"] = data["Rating"].fillna("Not Rated")

cleaned_data = data.dropna(subset=["Name"])

perfected_data_rating = cleaned_data.sort_values(by=["Rating"],ascending=False)
perfected_data_chapters = cleaned_data.sort_values(by=["chapter_count"],ascending=False)

try:
    os.makedirs(f"Sorted {genre} Novels")
    print("Folder Creation Successful")
except Exception as e:
    print(e)
#I Can Do Like This Too Sorted Novels {Genre}
perfected_data_rating.to_csv(f"Perfected_Rating_{genre}.csv",index=False)
perfected_data_chapters.to_csv(f"Perfected_Chapters_{genre}.csv",index=False)

try:
    shutil.move(f"Perfected_Rating_{genre}.csv",os.path.join(f"Sorted {genre} Novels",f"Perfected_Rating_{genre}.csv"))
    shutil.move(f"Perfected_Chapters_{genre}.csv",os.path.join(f"Sorted {genre} Novels",f"Perfected_Chapters_{genre}.csv"))
    print(f"Operation Successful Saved Perfected File At Sorted {genre} Novels")
except Exception as e:
    print(e)


print("Thank You For Using Our Service Please Leave Us Your Feedback At Github")
