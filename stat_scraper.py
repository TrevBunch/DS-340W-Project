# --- CONFIG ---
# Option A: hardcode names here
rookie_names = [
    # "Caleb Williams", "Marvin Harrison Jr.", "Jayden Daniels",
    # add/remove as needed
    "Emeka Egbuka"
]

# Option B: read names from a CSV with a column called "Name"
csv_path = ""  # e.g., "rookies.csv" (leave empty to skip)

# Headless browser?
HEADLESS = False

# ----------------

import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Read from CSV if provided
if csv_path.strip() != "":
    df_in = pd.read_csv(csv_path)
    if "Name" in df_in.columns:
        rookie_names = [str(x).strip() for x in df_in["Name"].tolist() if str(x).strip() != ""]

# Basic guard so we don't run an empty loop
rookie_names = [n for n in rookie_names if n]

# Set up Chrome
chrome_options = Options()
if HEADLESS:
    chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1400,900")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 5)

results = []

for name in rookie_names:
    # 1) Search on PFR
    q = name.replace(" ", "+")
    search_url = f"https://www.pro-football-reference.com/search/search.fcgi?search={q}"
    driver.get(search_url)
    time.sleep(0.7)

    current_url = driver.current_url
    is_player_page = "pro-football-reference.com/players/" in current_url.lower()

    if not is_player_page:
        player_links = driver.find_elements(By.CSS_SELECTOR, "#players .search-item-url, #players a, .search-item a")
        if len(player_links) == 0:
            player_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/players/']")
        if len(player_links) > 0:
            player_links[0].click()
            wait.until(EC.presence_of_element_located((By.ID, "meta")))
            current_url = driver.current_url
            is_player_page = True

    # ---------- STEP 3: go to College Football page (INSIDE THE LOOP) ----------
    college_link_url = ""

    # scroll to bottom to ensure the link is rendered
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.6)

    # primary: exact phrase shown on PFR player pages
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, "College Football at Sports-Reference.com")
    # fallback: match by domain if the anchor text varies
    if len(links) == 0:
        links = driver.find_elements(By.CSS_SELECTOR, "a[href*='sports-reference.com/cfb/players/'], a[href*='sports-reference.com/cfb/schools/']")

    if len(links) > 0:
        college_link = links[0]
        college_link_url = college_link.get_attribute("href")
        # follow the href directly to avoid new-tab behavior
        driver.get(college_link_url)
    else:
        # if no link found, continue to next name
        results.append({"name": name, "college_url": "", "note": "No college link on PFR page"})
        continue

    # ---------- STEP 4: scrape latest-season PASSING from college page ----------
    # wait for either the passing table or the receiving/rushing table to exist
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table#passing_standard, table#receiving_and_rushing, table#rushing_and_receiving")))
    time.sleep(0.4)

    college_url = driver.current_url
    row_out = {"name": name, "college_url": college_url}

    # --- PASSING (table id: passing_standard) ---
    passing_latest = {}
    passing_tables = driver.find_elements(By.ID, "passing_standard")
    if len(passing_tables) > 0:
        t = passing_tables[0]

        # header keys from thead (prefer data-stat)
        ths = t.find_elements(By.CSS_SELECTOR, "thead tr th")
        passing_keys = []
        i = 0
        while i < len(ths):
            key = ths[i].get_attribute("data-stat")
            if key is None or key.strip() == "":
                key = ths[i].text.strip()
            passing_keys.append(key)
            i += 1

        # only real season rows from tbody
        season_rows = []
        rows = t.find_elements(By.CSS_SELECTOR, "tbody tr")
        j = 0
        while j < len(rows):
            row = rows[j]
            year_ths = row.find_elements(By.CSS_SELECTOR, "th[data-stat='year_id']")
            if len(year_ths) > 0:
                txt = year_ths[0].text.strip().lower()
                if "career" not in txt and "school" not in txt and "total" not in txt and txt != "":
                    season_rows.append(row)
            j += 1

        if len(season_rows) > 0:
            last = season_rows[-1]  # most recent season
            cells = last.find_elements(By.CSS_SELECTOR, "th, td")
            vals = []
            k = 0
            while k < len(cells):
                vals.append(cells[k].text.strip())
                k += 1

            m = 0
            while m < min(len(passing_keys), len(vals)):
                passing_latest["pass_" + passing_keys[m]] = vals[m]
                m += 1

    for kk in passing_latest:
        row_out[kk] = passing_latest[kk]

    # (optional) Receiving & Rushing – you can add the same pattern here

    # save this player’s row
    results.append(row_out)

# Close browser
driver.quit()

print(results)

'''
# 5) Save to CSV and display
out_df = pd.DataFrame(results, columns=["name", "pfr_url", "college", "college_links"])
out_df.to_csv("rookies_college_from_pfr.csv", index=False)
print("Saved: rookies_college_from_pfr.csv")
out_df
'''