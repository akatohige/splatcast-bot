import time
import schedule
from spla_api import StageScheduler
from datetime import datetime
from discordwebhook import Discord

def get_fest_post_embeds(fest_dict):
    is_tricolor = fest_dict["is_tricolor"]

    embeds = [
        {
            "title": "フェスマッチ",
            "fields": 
            [
                {
                    "name": "ルール",
                    "value": fest_dict["rule"]["name"],
                },
                {
                    "name": "Stage1",
                    "value": fest_dict["stages"][0]["name"],
                    "inline": True,
                },
                {
                    "name": "Stage2",
                    "value": fest_dict["stages"][1]["name"],
                    "inline": True,
                },
            ],
            "thumbnail": {"url": fest_dict["stages"][0]["image"]},
            "image": {"url": fest_dict["stages"][1]["image"]},
        },
    ]

    if is_tricolor:
        embed = {
            "title": "フェスマッチ",
            "fields": [
                {
                    "name": "ルール",
                    "value": "トリカラバトル",
                },
                {
                    "name": "Stage",
                    "value": fest_dict["tricolor_stage"]["name"],
                    "inline": True,
                },
            ],
            "image": {"url": fest_dict["tricolor_stage"]["image"]},
        }
        embeds.append(embed)
        
    return embeds

def get_post_embeds(regular_dict, bankara_challenge_dict, bankara_open_dict):
    embeds = [
        {
            "title": "レギュラーマッチ",
            "fields": 
            [
                {
                    "name": "ルール",
                    "value": regular_dict["rule"]["name"],
                },
                {
                    "name": "Stage1",
                    "value": regular_dict["stages"][0]["name"],
                    "inline": True,
                },
                {
                    "name": "Stage2",
                    "value": regular_dict["stages"][1]["name"],
                    "inline": True,
                },
            ],
            "thumbnail": {"url": regular_dict["stages"][0]["image"]},
            "image": {"url": regular_dict["stages"][1]["image"]},
        },
        {
            "title": "バンカラマッチ(チャレンジ)",
            "fields": [
                {
                    "name": "ルール",
                    "value": bankara_challenge_dict["rule"]["name"],
                },
                {
                    "name": "Stage1",
                    "value": bankara_challenge_dict["stages"][0]["name"],
                    "inline": True,
                },
                {
                    "name": "Stage2",
                    "value": bankara_challenge_dict["stages"][1]["name"],
                    "inline": True,
                },
            ],
            "thumbnail": {"url": bankara_challenge_dict["stages"][0]["image"]},
            "image": {"url": bankara_challenge_dict["stages"][1]["image"]},
        },
        {
            "title": "バンカラマッチ(オープン)",
            "fields": [
                {
                    "name": "ルール",
                    "value": bankara_open_dict["rule"]["name"],
                },
                {
                    "name": "Stage1",
                    "value": bankara_open_dict["stages"][0]["name"],
                    "inline": True,
                },
                {
                    "name": "Stage2",
                    "value": bankara_open_dict["stages"][1]["name"],
                    "inline": True,
                },
            ],
            "thumbnail": {"url": bankara_open_dict["stages"][0]["image"]},
            "image": {"url": bankara_open_dict["stages"][1]["image"]},
        },
    ]
    return embeds

def post(discord, scheduler):
    # Get the next stage info.
    scheduler.update()
    schedule_dict = scheduler.get_stage(index=1)
    if schedule_dict is None:
        print("ERROR: Spla3 API is down.")
        return

    # Get the time of the next stage.
    start_time = datetime.fromisoformat(schedule_dict["regular"]["start_time"])
    end_time = datetime.fromisoformat(schedule_dict["regular"]["end_time"])
    content = "Next Stage! \r" + start_time.strftime("%H:%M") + " ~ " + end_time.strftime("%H:%M")

    is_fest = schedule_dict["fest"]["is_fest"]
    if is_fest:
        embeds = get_fest_post_embeds(fest_dict=schedule_dict["fest"])
    else:
        embeds = get_post_embeds(regular_dict=schedule_dict["regular"], bankara_challenge_dict=schedule_dict["bankara_challenge"], bankara_open_dict=schedule_dict["bankara_open"])

    # Post
    discord.post(content=content, embeds=embeds)

def job(discord, scheduler):
    now = datetime.now()
    if now.hour % 2 == 1:
        post(discord=discord, scheduler=scheduler)

def main():
    webhooks_url = ""
    with open("webhook_url.txt", "r") as f:
        webhooks_url = f.read()

    if not webhooks_url:
        print("ERROR: Webhook URL is not specified.")
        return

    discord = Discord(url=webhooks_url)
    stage_scheduler = StageScheduler()

    schedule.every().hour.at(":55").do(job, discord=discord, scheduler=stage_scheduler)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()