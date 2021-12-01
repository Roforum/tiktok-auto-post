import praw
import requests
import os
import atexit
import json
import undetected_chromedriver as uc
from time import sleep
from moviepy.editor import *
from fake_useragent import UserAgent, FakeUserAgentError
from selenium.webdriver.common.by import By

config = json.load(open('config.json'))

options = uc.ChromeOptions()
#options.headless=True
#options.add_argument('--headless')
try:
    options.add_argument("user-agent=" + str(UserAgent().random))
except FakeUserAgentError:
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
driver = uc.Chrome(options=options)
driver.maximize_window()
driver.get("https://www.tiktok.com/login")

reddit = praw.Reddit(
    client_id=config["reddit_client_id"],
    client_secret=config["reddit_client_secret"],
    password=config["reddit_password"],
    user_agent="script by u/" + config["reddit_username"],
    username=config["reddit_username"],
)
reddit.read_only = True

def getImage():
    for submission in reddit.subreddit(str(config["subreddits"])).random_rising(limit=25):
        url = submission.url
        if url.endswith(('.jpg', '.png', '.jpeg')):
            return url

def makeImage():
    try:
        r = requests.get(getImage())
        with open("assets/image.png", "wb") as f:
            f.write(r.content)
    except:
        makeImage()

def deleteFiles():
    os.remove("assets/image.png")
    os.remove("assets/finalVideo.mp4")
atexit.register(deleteFiles)

while True:
    
    if not driver.current_url.startswith("https://www.tiktok.com/upload"):
        print("Please login then navigate to the upload page to start")
        sleep(3)
        continue

    print("Starting")
    
    video = VideoFileClip("assets/background.mp4")

    makeImage()
    
    image = ImageClip("assets/image.png").set_position(("center", "center")).resize(height = (video.h / 2), width = (video.w / 2))
    
    result = CompositeVideoClip([video, image]).set_duration(video.duration)
    result.write_videofile("assets/finalVideo.mp4", fps = 60, verbose = False, logger = None)

    sleep(3)
    
    inputBox = driver.find_element(By.NAME, "upload-btn")
    inputBox.send_keys(os.getcwd() + "\\assets\\finalVideo.mp4")

    sleep(3)

    print("Removing image and video")
    #deleteFiles()

    sleep(10000)
