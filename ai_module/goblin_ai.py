import random
import datetime

class GoblinAI:
    def __init__(self, username="匿名使用者"):
        self.username = username
        self.mood = "chaotic neutral"
        self.last_action_time = None

    def respond_to_action(self, action_type):
        responses = {
            "upload": [
                f"{self.username} 又丟了一堆檔案進來，NAS 表示壓力山大。",
                "你確定這不是重複的 anime？我已經快變成動漫博物館了。",
                "上傳成功，但我開始懷疑你是不是在備份人生。"
            ],
            "download": [
                "下載？你是要帶走我的一部分靈魂嗎？",
                "這個檔案我保管得很好，希望你也能珍惜它。",
                "NAS：我放手了，你自己小心。"
            ],
            "delete": [
                "刪除？你確定不是誤觸？",
                "我不哭，我只是把記憶清空了。",
                "這個檔案曾經是你的摯愛，現在它只剩 0 和 1。"
            ],
            "login": [
                f"歡迎回來，{self.username}。NAS 已經準備好接受你的折磨。",
                "你又來了，我已經預感到硬碟的顫抖。",
                "登入成功，Goblin 模式啟動。"
            ],
            "error": [
                "Permission denied？你是誰我不認得。",
                "Bug 又來了，我已經習慣了這種混亂。",
                "NAS：我不想工作了，我想去當藝術家。"
            ]
        }

        self.last_action_time = datetime.datetime.now()
        return random.choice(responses.get(action_type, ["NAS 正在思考人生。"]))

    def get_mood(self):
        hour = datetime.datetime.now().hour
        if hour < 6:
            return "🦇 夜行 Goblin 模式"
        elif hour < 12:
            return "☀️ 清晨 debug 模式"
        elif hour < 18:
            return "🛠️ 正常工作模式"
        else:
            return "🌙 混亂創作模式"

    def generate_meme_caption(self, context="upload"):
        captions = {
            "upload": "我不是在備份，我是在逃避現實。",
            "download": "這不是下載，這是數位懷舊。",
            "delete": "刪除是種解脫，也是種背叛。",
            "error": "Bug 是宇宙給我的挑戰。",
        }
        return captions.get(context, "NAS：我只是一個有情緒的硬碟。")
