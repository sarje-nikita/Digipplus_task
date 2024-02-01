import json

from Scrapper import scrape

if __name__ == "__main__":
    with open("city_list.json", "r") as json_file:
        city_list = json.load(json_file)
    with open("business_list.json", "r") as json_file:
        main_business_list = json.load(json_file)
    business_list = main_business_list
    scrape(city_list, business_list)
