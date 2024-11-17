from mcdreforged.api.all import PluginServerInterface, Info
from auto_cleaner_re import common
from auto_cleaner_re.common import server_inst, item_counter, tr
import re


def tag_player_items(server: PluginServerInterface, info: Info):
    death_split = info.content.split(" ")
    player = death_split[0]
    server.execute(
        f"execute at {player} run execute as @e[type=item,distance=..{common.config.ignore_distance}] run tag @s add player_death"
    )


def clean_items(ignore_player_items: bool = True):

    command = "kill @e[type=item]"
    if ignore_player_items:
        command = "kill @e[type=item,tag=!player_death]"

    global item_counter
    item_counter = True
    server_inst.execute(command)


def cleaned_items(server: PluginServerInterface, info: Info):
    if info.is_user:
        return
    content = info.content
    global item_counter

    if item_counter:
        match = re.search(r"Killed (\d+) entities", content)

        if match:
            killed_count = match.group(1)
            server.broadcast(tr("cleaned_items", killed_count))
            item_counter = False
            return
        elif "No entity was found" in content:
            server.broadcast(tr("cleaned_items", "0"))
            item_counter = False
            return
