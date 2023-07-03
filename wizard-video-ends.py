"""
This script is for:
Wizard101 but if I hear the word Wizard the video ends.
                   |
                   |
                an npc says
"""

import asyncio
import keyboard
import subprocess
import pyautogui
import math
from colorama import init, Fore, Back, Style
from wizwalker import ClientHandler
from wizwalker.memory import Window, WindowFlags
from wizwalker.memory.memory_objects.camera_controller import ElasticCameraController, CameraController
from wizwalker import Client, utils, Orient, XYZ, Keycode, Hotkey, HotkeyListener, ModifierKeys
import random

# Customize Below:
utils.override_wiz_install_location(r'E:\Kingsisle Entertainment\Wizard101') # Enter your wizard101 path.

init() #for logging

# DO NOT TOUCH ANYTHING IN THE DASHES -----------------------------------------------------

# Dialogue Paths
advance_dialog_path = ['WorldView', 'wndDialogMain', 'btnRight']
decline_quest_path = ['WorldView', 'wndDialogMain', 'btnLeft']
dialog_text_path = ['WorldView', 'wndDialogMain', 'txtArea', 'txtMessage']

async def get_window_from_path(root_window: Window, name_path: list[str]) -> Window:
	# FULL CREDIT TO SIROLAF FOR THIS FUNCTION
	async def _recurse_follow_path(window, path):
		if len(path) == 0:
			return window
		for child in await window.children():
			if await child.name() == path[0]:
				found_window = await _recurse_follow_path(child, path[1:])
				if not found_window is False:
					return found_window

		return False

	return await _recurse_follow_path(root_window, name_path)

async def read_dialogue_text(p: Client) -> str:
    try:
        dialogue_text = await get_window_from_path(p.root_window, dialog_text_path)
        txtmsg = await dialogue_text.maybe_text()
    except:
        txtmsg = ''
    return txtmsg

async def is_dialogue(client: Client):
	# Returns True if not in dialogue.
	return not any([await client.is_in_dialog()])
async def wait_for_dialogue(client: Client, wait_for_not: bool = False, interval: float = 0.25):
    if wait_for_not:
        while await is_dialogue(client):
            await asyncio.sleep(interval)

    else:
        while not await is_dialogue(client):
            await asyncio.sleep(interval)

async def unhook_ww(client: Client, client_camera: CameraController, handler: ClientHandler):
    print(Back.RED + "Disabling Script..." + Back.RESET)
    await handler.close()
    raise KeyboardInterrupt
# DO NOT TOUCH ANYTHING IN THE DASHES -----------------------------------------------------

async def main():
    print(Fore.BLUE + "LAUNCHING | " +
    Fore.GREEN + "Dialogue Reader") # Feel free to change the 3 to any amount of delay before it starts. 
    try:
        handler = ClientHandler()
        client = handler.get_new_clients()[0]
        client_camera = await client.game_client.selected_camera_controller()
        global enabled

        try:
            print(Fore.BLUE + "HOOKING | " +
    Fore.WHITE + "Hooking clients...")
            await client.activate_hooks()
            enabled = True
            # await client.mouse_handler.activate_mouseless() # <-- Dont activate this unless you know what you're doing.
            print(Fore.BLUE + "HOOKING | " +
    Fore.GREEN + "Hooked!")
        except:
            print(Fore.RED + "ERR | " +
    Fore.RED + "Failed to hook clients.")
        Fore.WHITE # Reset console to white.
            
        while enabled:
            await wait_for_dialogue(client, True)
            txt = await read_dialogue_text(client)
            if not txt == "":
                print(Fore.WHITE + f'{txt}')
            else:
                print("Waiting to pick dialogue...")
            if "wizard" in txt.lower():
                words = txt.lower().split(" ")
                index = 0
                for word in words:
                    if word == "wizard":
                        word_num = index
                    index += 1
                print("DETECTED Wizard: closing in " + f'{word_num}')
                await asyncio.sleep(word_num / 2.5)
                pyautogui.hotkey("alt", "f4")
                exit()
            await asyncio.sleep(1) 
        
        await unhook_ww(client, client_camera, handler)
    except:
        await unhook_ww(client, client_camera, handler)
    
if __name__ == "__main__":
    asyncio.run(main())    
