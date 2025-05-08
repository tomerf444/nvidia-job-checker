import requests
from bs4 import BeautifulSoup
import json
import os

WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # replace with your webhook
JOB_URL = "https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/jobs?q=student&locationHierarchy1=2fcb99c455831013ea52bbe14cf9326c"
SEEN_JOBS_FILE = "seen_jobs.json"

def fetch_jobs():
    response = requests.get(JOB_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.select("ul[data-automation-id='job-list'] li a")
    return [{"title": job.text.strip(), "link": job["href"]} for job in jobs]

def load_seen_jobs():
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen_jobs(jobs):
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(jobs, f)

def notify_discord(job):
    data = {
        "content": f"🆕 **{job['title']}**\nhttps://nvidia.wd5.myworkdayjobs.com{job['link']}"
    }
    requests.post(WEBHOOK_URL, json=data)

def check_jobs():
    seen = load_seen_jobs()
    seen_titles = [j['title'] for j in seen]
    current_jobs = fetch_jobs()
    new_jobs = [job for job in current_jobs if job["title"] not in seen_titles]
    for job in new_jobs:
        notify_discord(job)
    if new_jobs:
        save_seen_jobs(current_jobs)
    return f"{len(new_jobs)} new jobs found." if new_jobs else "No new jobs."
