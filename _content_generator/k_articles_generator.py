import csv
import re
from datetime import datetime
from os import listdir
from os.path import isfile, join

input_path = "input/"
output_path = "output/"
output_chro_name = "chronological-bibliography"
year_list = []
year_dic = {}
now = datetime.now()
current_year = now.year
current_month = now.month
current_day = now.day
current_hour = now.hour
current_minute = now.minute
current_second = now.second
one_page_by_authors = ""

def clean_content_val(data):
    data = re.sub(r"<", "&lt;", data)
    data = re.sub(r">", "&gt;", data)
    data = re.sub(r"【", "<i>", data)
    data = re.sub(r"】", "</i>", data)
    data = re.sub(r"《", "<sup>", data)
    data = re.sub(r"》", "</sup>", data)
    data = re.sub(r"{", "<sub>", data)
    data = re.sub(r"}", "</sub>", data)
    return data

def create_blog_head(title):
    return (
    "---\n"
    "layout: post\n"
    f"title: \"{title}\"\n"
    f"date: {current_year}-{current_month}-{current_day} {current_hour}:{current_minute}:{current_second} +0800\n"
    "description: \n"
    "img: \n"
    "---\n")

def write_author_list(article_author, author_writings_list):
    global one_page_by_authors
    blog_head = create_blog_head(article_author)
    output_list = [blog_head] + author_writings_list
    one_page_by_authors += f"**{article_author}**\n\n"
    output_string = ""
    output_filename = f"{output_path}{current_year}-{current_month}-{current_day}-{article_author}.markdown"
    with open(output_filename, "w", encoding="utf-8") as f:
        for outputline in output_list:
            output_string += outputline + "\n\n"
        f.write(output_string)
    for author_writings in author_writings_list:
        one_page_by_authors += author_writings + "\n\n"

def write_chronology(year_list, year_dic):
    blog_head = create_blog_head("Chronological Bibliography")
    with open(f"{output_path}{current_year}-{current_month}-{current_day}-{output_chro_name}.markdown", "w", encoding="utf-8") as f:
        f.write(blog_head + "\n\n")
        for year_item in year_list:
            year_item_with_style = f"# {year_item}"
            f.write(year_item_with_style + "\n\n")
            current_year_bibli_list = year_dic[year_item]
            current_year_bibli_list.sort()
            for entry_item in current_year_bibli_list:
                f.write(entry_item + "\n\n")

def write_one_page_by_authors():
    global one_page_by_authors
    blog_head = create_blog_head("Name Index on One Page (Alphabetical Order)")
    one_page_by_authors = blog_head + one_page_by_authors
    with open(f"{output_path}{current_year}-{current_month}-{current_day}-Name Index on One Page (Alphabetical Order).markdown", "w", encoding="utf-8") as f:
        f.write(one_page_by_authors)



# read all the csv files from "input/"
input_files = [(input_path + f) for f in listdir(input_path) if isfile(join(input_path, f))]
for input_file in input_files:
    author_writings_list = []
    article_author = ""
    with open(input_file, "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=",", quotechar='"')
        # skip the title
        next(csv_reader)
        for row in csv_reader:
            # remove the lines which only have commas
            if set(row)=={""}:
                continue
            article_author = row[0]
            # some years could be separated by ;
            article_year_list = [i.strip() for i in row[1].split(";")]
            article_title = clean_content_val(row[2])
            # add input data to each author's list
            author_writings_list.append(article_title)
            # to create year list and dictionary
            for article_year in article_year_list:
                if article_year == "":
                    article_year = "zzz_unknown"
                # if it's a year which hasn't been collected
                if article_year not in year_dic:
                    year_list.append(article_year)
                    year_list = list(set(year_list))
                    year_dic[article_year] = [f"{article_title}｜{article_author}"]
                # if it's a year which has been collected
                else:
                    year_dic[article_year].append(f"{article_title}｜{article_author}")
        # write the file for each author
        write_author_list(article_author, author_writings_list)
year_list.sort()
# write chronological bibliography
write_chronology(year_list, year_dic)
write_one_page_by_authors()
print("Done!")
  







            
