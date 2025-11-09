from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from helper.get_dataset_helper import Helper, write_to_csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
helper = Helper(driver)

series_id = 'ipl-2021-1249214'
match_ids = []

rowsLocator = (By.XPATH, "//b[contains(text(),'Bowler')]/ancestor::tr")

driver.get(f'{helper.get_hostname()}/series/{series_id}/match-schedule-fixtures-and-results')
matches = driver.find_elements(By.XPATH, "//div[@class='ds-relative']//a[@title='' and starts-with(@href,'/series')]")
for match in matches:
    match_ids.append(match.get_attribute('href').split('/')[-2])


count = 0
while count < len(match_ids):
    match_id = match_ids[count]
    print(f"Processing match {match_id}")
    match_name = f"Match-{count + 1}"
    driver.get(f"{helper.get_hostname()}/series/{series_id}/{match_id}/match-overs-comparison")
    helper.cancel_popup(driver)
    try:
        helper.expand_table(driver)
        innings_1_final_score, innings_1_final_wickets, innings_2_final_score, innings_2_final_wickets = helper.get_final_scores(driver)

        innings_1_balls = helper.get_all_balls(driver, 1)
        write_to_csv(match_name, 1, innings_1_balls)
        if innings_1_balls[-1].runs != innings_1_final_score or innings_1_balls[-1].wickets != innings_1_final_wickets:
            print(f"Review Innings 1 ({innings_1_balls[-1].runs}/{innings_1_balls[-1].wickets}) vs ({innings_1_final_score}/{innings_1_final_wickets})")

        innings_2_balls = helper.get_all_balls(driver, 2)
        write_to_csv(match_name, 2, innings_2_balls)
        if innings_2_balls[-1].runs != innings_2_final_score or innings_2_balls[-1].wickets != innings_2_final_wickets:
            print(f"Review Innings 1 ({innings_2_balls[-1].runs}/{innings_2_balls[-1].wickets}) vs ({innings_2_final_score}/{innings_2_final_wickets})")

    except Exception as e:
        print(f"Error processing match {match_id}: {e}")
    count += 1
    print("")


helper.destroy()

