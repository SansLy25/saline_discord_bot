from os import getenv
import time

import discord
from dotenv import load_dotenv

load_dotenv()

import random


def get_random_emoji():
    emoji_ranges = [
        (0x1F600, 0x1F64F)
    ]

    chosen_range = random.choice(emoji_ranges)
    emoji_code = random.randint(chosen_range[0], chosen_range[1])

    return chr(emoji_code)


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_last_left = {}

    async def on_ready(self):
        print(f'Вошли как {self.user}')

    async def on_voice_state_update(self, member, before, after):
        text_channel_id = int(getenv('TEXT_CHANNEL_ID'))
        text_channel = self.get_channel(text_channel_id)

        if before.channel is None and after.channel is not None:
            last_left_time = self.user_last_left.get(member.id)
            current_time = time.time()

            if last_left_time is None or (current_time - last_left_time) > 300:
                if text_channel is not None:
                    await text_channel.send(
                        f'- {get_random_emoji()}   **{member.display_name}**'
                        f' зашел в голосовой канал **"{after.channel.name.capitalize()}"**')

        if before.channel is not None and after.channel is None:
            self.user_last_left[member.id] = time.time()


intents = discord.Intents.default()
intents.voice_states = True
client = MyClient(intents=intents)

client.run(getenv('BOT_TOKEN'))
