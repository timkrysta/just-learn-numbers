#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import requests
import curses
from io import BytesIO
from pprint import pprint

from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS
from PyInquirer import prompt, Separator

from examples import custom_style_2 as styles
from tui import Color, Icon


_lang = 'nl'
min_number = ""
max_number = ""
widest_range = ['0', '1000000000']
encoding = 'utf-8'
clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


def main():
    start_time = time.time()
    try:
        run_app(_lang)
    except KeyboardInterrupt:
        end()
        print(f"\n{Icon.info}Bye!")
        seconds_of_learning = (time.time() - start_time)
        print(f"{Icon.info}Training lasted: {convert_seconds_into_time_string(seconds_of_learning)} ")
        if seconds_of_learning > (60 * 5):
            good_training_text = "Nice training!"
            print(good_training_text)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


def is_number_in_valid_range(number):
    if number == "":
        return False
    number = int(number)
    if number < 0:
        print(f"{Icon.cross}Number cannot be smaller than 0")
        return False
    elif number > 1000000000:
        print(f"{Icon.cross}Maximum is 1 000 000 000")
        return False
    else:
        return True


def validate_range(range):
    range = range.lower().strip()
    if range == "all":
        return widest_range
    range_array = range.split("-")
    if len(range_array) != 2:
        print(f"{Icon.cross}Invalid range. Type two numbers separated by dash")
        return False
    if not is_number_in_valid_range(range_array[0]):
        print(f"{Icon.cross}First number incorrect\n")
        return False
    if not is_number_in_valid_range(range_array[1]):
        print(f"{Icon.cross}Second number incorrect\n")
        return False
    if int(range_array[1]) < 1:
        print(f"{Icon.cross}Second number cannot be less than 1\n")
        return False
    if range_array[0] == range_array[1]:
        print(f"{Icon.cross}Both numbers cannot be the same\n")
        return False
    else:
        if range_array[0] != 0:
            range_array[0] = range_array[0].lstrip("0")
            if range_array[0] == "": # This will be true if user passed: 000000
                range_array[0] = 0
        range_array[1].lstrip("0") # need to strip not to have 000000437 being passed
        return range_array


def get_number_range_user_wants_to_practise():
    questions = [{
        'type': 'input',
        'name': 'answear',
        'message': f"Type range of numbers you want to train.\n  Examples: 0-100, 1-19, 50-60 or type all for max range: 0-1000000000\n",
    }]
    while True:
        number_range_user_wants_to_practise = prompt(questions, style=styles).get('answear')
        range_array = validate_range(number_range_user_wants_to_practise)
        if range_array:
            break
        else:
            continue
    min_number = range_array[0]
    max_number = range_array[1]
    return {
        'from': range_array[0],
        'to'  : range_array[1]
    }


def my_raw_input(stdscr, row, col, prompt_strings):
    i = 0 # i is counter to display string below string
    for prompt_string in prompt_strings:
        stdscr.addstr(row + i, col, prompt_string)
        i += 1
    stdscr.refresh()
    input_row = row + i + 1
    input = stdscr.getstr(input_row, col, 20) # This returns bytes
    input = input.decode(encoding)
    return input


def play_gtts_audio(text, _lang):
    # get audio from Google's server
    tts = gTTS(text=text, lang=_lang)
    # convert to file-like object
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    # play it
    audio = AudioSegment.from_file(fp, format="mp3")
    play(audio)


def clear_and_refresh_screen(stdscr): # get blank canvas
    stdscr.clear()
    stdscr.refresh()


def initialize_curses_colors():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN,  curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK) # Correct
    curses.init_pair(5, curses.COLOR_RED,   curses.COLOR_BLACK) # Incorrect
    curses.init_pair(6, curses.COLOR_CYAN,  curses.COLOR_BLACK) # Info


def listening_module(stdscr):
    def reRender(stdscr, display_message = False):
        clear_and_refresh_screen(stdscr)
        stdscr.border(0)
        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-2, 1, statusbarstr) # This will return error if screen is smaller than some width
        stdscr.addstr(height-2, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))
        if display_message:
            row = display_message.get('row')
            col = display_message.get('col')
            prompt_string = display_message.get('prompt_string')
            if display_message.get('color') != 0:
                stdscr.attron(curses.color_pair(display_message.get('color')))
                stdscr.attron(curses.A_BOLD)
                stdscr.addstr(row, col, prompt_string)
                stdscr.attroff(curses.color_pair(display_message.get('color')))
                stdscr.attroff(curses.A_BOLD)
                stdscr.addstr(row + 1, col, "Press Enter to continue") # difference between the other reRender method is only this line
            else:
                stdscr.addstr(row, col, prompt_string)
        stdscr.refresh()


    clear()
    clear_and_refresh_screen(stdscr)
    initialize_curses_colors()
    
    range = get_number_range_user_wants_to_practise()
    min_number = range.get('from')
    max_number = range.get('to')
    clear()

    key = 0
    cursor_x = 0
    cursor_y = 0

    # Loop where k is the last character pressed
    while (key != ord('q')):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        title    = "Curses example"[:width-1]
        subtitle = "Python TUI example"[:width-1]
        keystr   = "Last key pressed: {}".format(key)[:width-1]
        statusbarstr = "Press CTRL + c or Type 'q' to exit "
        if key == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title    = int((width // 2) - (len(title) // 2)    - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr   = int((width // 2) - (len(keystr) // 2)   - len(keystr) % 2)
        start_y          = int((height // 2) - 2)
        # NOTE: until here is the same as in the other module

        while True:
            text = str(random.randint(int(min_number), int(max_number)))
            stdscr.keypad(True)
            curses.noecho()
            play_gtts_audio(text, _lang)
            clear()
            reRender(stdscr)
            while True:
                curses.echo()
                response = my_raw_input(stdscr, row = 2, col = 2, prompt_strings = [
                    "Type what you heard:",
                    "",
                    "    <your answear> - to check your answear",
                    "    c              - to check the correct answear",
                    "    Enter          - to continue,",
                ]).strip().lower()

                # Enter pressed
                if response.strip() == "":
                    end()
                    break
                # show the correct answear
                if response.strip().lower() == "c":
                    reRender(stdscr, display_message={
                        "row": 10,
                        "col": 2,
                        "prompt_string": f"Correct answear is: {text}",
                        "color": 6 # info color
                    })
                    continue
                # show the correct answear
                if "".join(response.split()) == text:
                    reRender(stdscr, display_message={
                        "row": 10,
                        "col": 2,
                        "prompt_string": f"Good! That was correct answear! {text}",
                        "color": 4 # green correct color
                    })
                    continue
                if response.strip().lower() == "q":
                    raise KeyboardInterrupt
                else:
                    # show the correct answear
                    reRender(stdscr, display_message={ 
                        "row": 10,
                        "col": 2,
                        "prompt_string": f"Wrong! Your was incorrect. Correct answear is: {text}",
                        "color": 5 # red incorrect color
                    })
                    continue
        stdscr.move(cursor_y, cursor_x)
        # Refresh the screen
        stdscr.refresh()
        # Wait for next input
        key = stdscr.getch()


def speaking_module(stdscr):
    def reRender(stdscr, display_message = False):
        clear_and_refresh_screen(stdscr)
        stdscr.border(0)
        # Render status bar
        stdscr.attron(curses.color_pair(3))
        # This will return error if screen is smaller than some width
        stdscr.addstr(height-2, 1, statusbarstr) 
        stdscr.addstr(height-2, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))
        if display_message:
            row = display_message.get('row')
            col = display_message.get('col')
            prompt_string = display_message.get('prompt_string')
            if display_message.get('color') != 0:
                stdscr.attron(curses.color_pair(display_message.get('color')))
                stdscr.attron(curses.A_BOLD)
                stdscr.addstr(row, col, prompt_string)
                stdscr.attroff(curses.color_pair(display_message.get('color')))
                stdscr.attroff(curses.A_BOLD)
            else:
                stdscr.addstr(row, col, prompt_string)
        stdscr.refresh()


    clear()
    clear_and_refresh_screen(stdscr)
    initialize_curses_colors()

    range = get_number_range_user_wants_to_practise()
    min_number = range.get('from')
    max_number = range.get('to')
    clear()

    key = 0
    cursor_x = 0
    cursor_y = 0

    # Loop where k is the last character pressed
    while (key != ord('q')):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)

        title    = "Curses example"[:width-1]
        subtitle = "Python TUI example"[:width-1]
        keystr   = "Last key pressed: {}".format(key)[:width-1]
        statusbarstr = "Press CTRL + c or Type 'q' to exit "
        if key == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title    = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr   = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y          = int((height // 2) - 2)
        # NOTE: until here is the same as in the other module

        while True:
            text = str(random.randint(int(min_number), int(max_number)))
            stdscr.keypad(True)
            curses.noecho()
            reRender(stdscr, display_message={
                "row": 1,
                "col": 2,
                "prompt_string": f"Say it out loud: {text}",
                "color": 6 # info color
            })
            while True:
                curses.echo()
                response = my_raw_input(stdscr, row = 2, col = 2, prompt_strings = [
                    "Type:",
                    "",
                    "    c              - to check the correct pronunciation",
                    "    Enter          - to continue,",
                ]).strip().lower()

                if response.strip() == "": # Enter pressed
                    end()
                    break
                if response.strip().lower() == "c":
                    # listen to the correct answear
                    play_gtts_audio(text, _lang)

                    reRender(stdscr, display_message={
                        "row": 1,
                        "col": 2,
                        "prompt_string": f"Say it out loud: {text}",
                        "color": 6 # info color
                    })
                    continue
                if response.strip().lower() == "q":
                    raise KeyboardInterrupt
                else:
                    break


def run_app(_lang):
    clear()
    questions = [{
        'type': 'list',
        'name': 'training_type',
        'message': 'Choose a learning module to start',
        'choices': [
            'Listening',
            'Speaking',
        ]
    }]
    training_type = prompt(questions, style=styles).get('training_type')
    if training_type == "Listening": # listening & understanding module
        curses.wrapper(listening_module)
    if training_type == "Speaking": # viewing & speaking module
        curses.wrapper(speaking_module)


def convert_seconds_into_time_string(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    # Alternative: "%d:%02d:%02d"
    return "%dh %2dmin %2dsec" % (hour, minutes, seconds)

def end():
    curses.endwin()
    clear()

if __name__ == '__main__':
    main()