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

def get_cars(scraping_run_id: str):
    token_url = f"https://api.scrapemequickly.com/get-token?scraping_run_id={scraping_run_id}"
    token = requests.get(token_url).json()["token"]
    print(token)
    
    proxies = {
        "https": "http://pingproxies:scrapemequickly@194.87.135.1:9875"
    }

    url = f"https://api.scrapemequickly.com/cars/test?scraping_run_id={scraping_run_id}&per_page=10&start=0"
    headers = {
    "Authorization": f"Bearer {token}",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
    }
    response = requests.get(url, headers=headers, proxies=proxies)

    content = response.content
    print(content)
    soup = BeautifulSoup(content, 'html.parser')

    
    years = soup.find_all('p', class_="year")#.get_text()[6:]
    print(years)
    prices = soup.find_all('p', class_="price")#.get_text()[8:]
    makes = soup.find_all('h2', class_="text-lg sm:text-base font-bold mt-2 title")#.get_text().split(",")[0]

    return years, prices, makes





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
years, prices, makes = get_cars(scraping_run_id)

print(years)

# print(min(years))
# print(max(years))
# print(mean(prices))
# print(mode(makes))





