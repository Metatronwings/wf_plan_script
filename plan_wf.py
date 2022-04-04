from datetime import datetime, timedelta
import json


# --- 一些常量 --- #
GUARANTEE_DRAW_AMOUNT = 250
STAR_SLIVER_GUARANTEE_AMOUNT = 600
DAILY_MISSION_FREE_BEADS_AMOUT = 50

# --- 玩家填写 --- #
FREE_BEADS_AMOUNT = 56635
PAID_BEADS_AMOUNT = 4575
STAR_SLIVER_AMOUNT = 613
SUMMONING_TICKET_10_PULL_AMOUNT = 1
SUMMONING_TICKET_1_PULL_AMOUNT = 40

DAILY_BEADS_SET_REMAIN_DAYS = 11

INPUT = {
    "half_year_gacha": {
        "consumption": {
            "free_beads": 3000
        }
    },
    "swimsuit_1_of_4": {
        "consumption": {
            "star_sliver": STAR_SLIVER_GUARANTEE_AMOUNT
        }
    },
    "swimsuit_2_of_4": {
        "consumption": {
            "free_beads": 22500
        }
    },
    "halloween_gacha_1": {
        "consumption": {
            "free_beads": 7500
        }
    },
    "one_year_pre_gacha": {
        "consumption": {
            "free_beads": 15000
        }
    },
    "one_year_gacha": {
        "consumption": {
            "free_beads": 15000,
            "star_sliver": STAR_SLIVER_GUARANTEE_AMOUNT
        }
    },
    "shenglong_gacha": {
        "consumption": {
            "free_beads": 15000,
        }
    },
    "leiniu_gacha": {
        "consumption": {
            "free_beads": 15000,
        }
    },
    "reimu_gacha": {
        "consumption": {
            "free_beads": 22500,
        }
    }
}

if __name__ == '__main__':
    now = datetime.now()

    with open("config/gacha_timeline.json", encoding="utf-8") as f:
        gacha_timeline = json.load(f)

    with open("config/kakin_income.json", encoding="utf-8") as f:
        kakin_income = json.load(f)

    with open("config/kakin_activity_timeline.json", encoding="utf-8") as f:
        kakin_activity_timeline = json.load(f)

    free_beads = FREE_BEADS_AMOUNT
    paid_beads = PAID_BEADS_AMOUNT
    star_sliver = STAR_SLIVER_AMOUNT

    daily_beads_set_remain_days = DAILY_BEADS_SET_REMAIN_DAYS

    # 默认转化抽数为免费钻
    free_beads = free_beads + 1500 * SUMMONING_TICKET_10_PULL_AMOUNT + 150 * SUMMONING_TICKET_1_PULL_AMOUNT

    for key in gacha_timeline.keys():
        # 首先判断当前日期是否大于当前的卡池，如果是则跳过
        if now > datetime.strptime(gacha_timeline[key]["end_date"], "%Y-%m-%d"):
            continue
        else:
            # 然后对这个时间段进行星导石收入的模拟
            period = datetime.strptime(gacha_timeline[key]["end_date"], "%Y-%m-%d") - now

            # 头尾所以这里 period.days + 1
            for i in range(period.days + 1):
                # 先计算收入
                # 每日任务
                free_beads = free_beads + DAILY_MISSION_FREE_BEADS_AMOUT
                # 月卡
                free_beads = free_beads + kakin_income["daily_beads_set"]["free_beads"]["amount"]
                daily_beads_set_remain_days = daily_beads_set_remain_days - 1
                # 检查当前的月卡是否为 0 天，如为 0 天，则续费
                if daily_beads_set_remain_days == 0:
                    daily_beads_set_remain_days = 30
                    # 卡点买月卡能多收一天免费星导石
                    free_beads = free_beads + kakin_income["daily_beads_set"]["free_beads"]["amount"]
                    # 付费星导石收入
                    paid_beads = paid_beads + kakin_income["daily_beads_set"]["paid_beads"]["amount"]
                # 付费钻
                if 7 <= now.day <= 14:
                    # 购入 25元=500钻 礼包
                    paid_beads = paid_beads + kakin_income["500_paid_beads_set"]["paid_beads"]["amount"]

                # 再计算支出
                # 付费单抽（角色和装备）
                # 这里因为付费单抽和星碎是绑定的，所以在这儿对星碎进行增加计算
                paid_beads = paid_beads - 75
                star_sliver = star_sliver + 3

                now = now + timedelta(days=1)
            # 看一下是不是需要投入的池子
            if INPUT.get(key, None):
                if INPUT[key]["consumption"].get("free_beads", None):
                    free_beads = free_beads - INPUT[key]["consumption"]["free_beads"]
                if INPUT[key]["consumption"].get("star_sliver", None):
                    star_sliver = star_sliver - INPUT[key]["consumption"]["star_sliver"]
            # 看一下当前的日期是不是超得或者必得
            for k in kakin_activity_timeline.keys():
                if now.strftime("%Y-%m-%d") in kakin_activity_timeline[k]["date"]:
                    paid_beads = paid_beads - kakin_activity_timeline[k]["consumption"].get("paid_beads", 0)
                    star_sliver = star_sliver - kakin_activity_timeline[k]["reward"].get("star_sliver", 0)
                    print("当前日期：", now.strftime("%Y-%m-%d"))
                    print("超得或必得：", k)
                    print("------- 分割线 -------")

            # 打印一下当前的池子是什么，当前还有多少资源
            print("当前池子：", key)
            print("免费钻：", free_beads)
            print("付费钻：", paid_beads)
            print("星碎：", star_sliver)
            print("当前日期：", now.strftime("%Y-%m-%d"))
            print("------- 分割线 -------")
