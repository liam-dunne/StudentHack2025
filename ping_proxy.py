import requests
import sys
import json
from bs4 import BeautifulSoup
from statistics import mean, mode

def create_team(team_name: str, team_email: str) -> str:
    r = requests.post(
        "https://api.scrapemequickly.com/register",
        data=json.dumps({"team_name": team_name, "team_email": team_email}),
        headers={"Content-Type": "application/json"}
    )

    if r.status_code != 200:
        print(r.json())
        print("Failed to create a team")
        sys.exit(1)

    return r.json()["data"]["team_id"]


def start_scraping_run(team_id: str) -> str:
    r = requests.post(f"https://api.scrapemequickly.com/scraping-run?team_id={team_id}")

    if r.status_code != 200:
        print(r.json())
        print("Failed to start scraping run")
        sys.exit(1)

    return r.json()["data"]["scraping_run_id"]

def get_cars(scraping_run_id: str, start: int):
    global years
    global prices
    global makes


    token_url = f"https://api.scrapemequickly.com/get-token?scraping_run_id={scraping_run_id}"
    token = session.get(token_url).json()["token"]
        
    proxies = ["http://pingproxies:scrapemequickly@194.87.135.1:9875",
               "http://pingproxies:scrapemequickly@194.87.135.2:9875",
               "http://pingproxies:scrapemequickly@194.87.135.3:9875",
               "http://pingproxies:scrapemequickly@194.87.135.4:9875",
               "http://pingproxies:scrapemequickly@194.87.135.5:9875"]
    
    proxy = {
        "https": "http://pingproxies:scrapemequickly@194.87.135.1:9875"
    }

    url = f"https://api.scrapemequickly.com/cars/test?scraping_run_id={scraping_run_id}&per_page=25&start={start}"
    headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    }
    response = requests.get(url, headers=headers, proxies=proxy)

    content = response.json()

    for car in content["data"]:
        years.append(car["year"])
        prices.append(car["price"])
        makes.append(car["make"])
    





def submit(answers: dict, scraping_run_id: str) -> bool:
    r = requests.post(
        f"https://api.scrapemequickly.com/cars/solve?scraping_run_id={scraping_run_id}",
        data=json.dumps(answers),
        headers={"Content-Type": "application/json"}
    )

    if r.status_code != 200:
        print(r.json())
        print("Failed to submit answers")
        return False

    return True

scraping_run_id = start_scraping_run("cc675f0b-1205-11f0-8f44-0242ac120003")

years = []
prices = []
makes = []

start = 0
session = requests.Session()

for i in range(1000):
    get_cars(scraping_run_id, start)
    start += 25
    print(i)



print(min(years))
print(max(years))
print(mean(prices))
print(mode(makes))

answers = {
    "min_year": min(years),
    "max_year": max(years),
    "avg_price": round(mean(prices)),
    "mode_make": mode(makes)
}

submit(answers, scraping_run_id)





