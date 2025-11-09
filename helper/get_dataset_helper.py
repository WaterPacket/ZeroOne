import csv
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from .balls import Ball
def get_runs(ball):
    ball = ball.strip().replace("b", "").replace("l", "").replace("-", "")

    if "w" in ball or "n" in ball or "W" in ball:
        tmp = ball.replace("w", "").replace("n", "").replace("W","")
        runs = int(tmp) if len(tmp) > 0 else 0
    elif ball.isdigit():
        runs = int(ball)
    else:
        runs = 0

    return runs

def get_wicket(ball):
    ball = ball.strip()
    return 1 if "W" in ball else 0

def is_extra_ball(ball):
    return "w" in ball or "n" in ball

def write_to_csv(name, innings, balls):
    with open(f"dataset/{name}-Innings-{innings}.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ballCount", "runs", "wickets"])
        for ball in balls:
            writer.writerow([ball.ballCount, ball.runs, ball.wickets])

class Helper:
    driver = None
    wait = None
    hostname = "https://www.espncricinfo.com"

    # Locators
    expandBtnLocator = (By.XPATH, "//i[contains(@class,'fullscreen')]")
    rowsLocator = (By.XPATH, "//b[contains(text(),'Bowler')]/ancestor::tr")
    ballsLocator = (By.XPATH, ".//div[contains(@class,'ds-flex-wrap')]/div//span")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_hostname(self):
        return self.hostname

    def cancel_popup(self, driver):
        cancel_buttons = driver.find_elements(By.CSS_SELECTOR, "button#wzrk-cancel")
        if len(cancel_buttons) != 0 and cancel_buttons[0].is_displayed():
            cancel_buttons[0].click()

    def expand_table(self, driver):
        self.cancel_popup(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        self.driver.find_element(*self.expandBtnLocator).click()
        time.sleep(2)

    def get_all_balls(self, driver, innings):
        self.cancel_popup(driver)
        delta = 0
        rows = self.driver.find_elements(*self.rowsLocator)
        all_balls = [Ball(0, 0, 0)]
        count = 1
        for row in rows:
            cell = row.find_elements(By.TAG_NAME, "td")[innings]
            balls = cell.find_elements(*self.ballsLocator)
            for ball in balls:
                lastBall = all_balls[count - 1]
                if is_extra_ball(ball.text):
                    delta += get_runs(ball.text)
                else:
                    all_balls.append(Ball(count, lastBall.runs + get_runs(ball.text) + delta, lastBall.wickets + get_wicket(ball.text)))
                    delta = 0
                    count += 1
        return all_balls

    def destroy(self):
        self.driver.quit()

    def get_final_scores(self, driver):
        try:
            self.cancel_popup(driver)
            scores = driver.find_elements(By.CSS_SELECTOR, "div.ds-w-full div.ci-team-score strong")
            team1_score = scores[0].text.split("/")
            team2_score = scores[1].text.split("/")
            return (int(team1_score[0]), int(team1_score[1] if len(team1_score) == 2 else 10),
                    int(team2_score[0]), int(team2_score[1] if len(team2_score) == 2 else 10))
        except Exception as e:
            return 0, 0, 0, 0