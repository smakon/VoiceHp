import speech_recognition as sr
import playsound
from gtts import gTTS
import configparser
import os
import pyautogui as pg
import psutil
import time


config = configparser.ConfigParser()


config.read('example.ini', encoding="utf-8")
default_ = config['DEFAULT']
cmd_count = 0
print(f"Я {default_['bot_n']}")
command_name = " "


# TODO:
# Придумать расшифровку Марк: Могучий абстрактный рукоблуд конченный:
#

def open_program(name):
    pg.press("win")
    pg.typewrite(name)
    pg.press("enter")
    return 0

def close_program(name):
    for process in (process for process in psutil.process_iter() if process.name() == name + ".exe"):
        process.kill()
    return 0



def crete_command(name,name_prog,bool):
    global cmd_count
    config.read("example.ini",encoding="utf-8")
    cmd_count +=1
    if bool == True:
        cmd_count += int(config['DEFAULT']['cmd_count_save_open'])
        config['COMMANDS_OPEN_' + str(cmd_count-1)] = {'cmd_name': name,
                                                   'prog_name': name_prog
                                                   }
        with open("example.ini", 'a+', encoding='utf8') as file:
            config.write(file)

        config['DEFAULT']['cmd_count_save_open'] = str(cmd_count)
        with open("example.ini", 'w', encoding='utf8') as file:
            config.write(file)
    elif bool == False:
        cmd_count += int(config['DEFAULT']['cmd_count_save_kill'])
        config['COMMANDS_KILL_' + str(cmd_count-1)] = {'cmd_name': name,
                                                   'prog_name': name_prog
                                                   }
        with open("example.ini", 'a+', encoding='utf8') as file:
            config.write(file)

        config['DEFAULT']['cmd_count_save_kill'] = str(cmd_count)
        with open("example.ini", 'w', encoding='utf8') as file:
            config.write(file)
    elif bool == None:
        cmd_count += int(config['DEFAULT']['cmd_count_save_say'])
        config['COMMANDS_SAY_' + str(cmd_count - 1)] = {'cmd_name': name,
                                                        'prog_name': name_prog}
        with open("example.ini", 'a+', encoding='utf8') as file:
            config.write(file)

        config['DEFAULT']['cmd_count_save_say'] = str(cmd_count)
        with open("example.ini", 'w', encoding='utf8') as file:
            config.write(file)
# crete_command("как дела","хорошо",None)

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Скажите вашу команду: ")
        audio = r.listen(source)
        try:
            our_speech = r.recognize_google(audio, language="ru")
            print("Вы сказали: " + our_speech.lower())
            return our_speech
        except sr.UnknownValueError:
            return "ошибка"
        except sr.RequestError:
            return "ошибка"


def do_this_command(message):
    message = message.lower()
    if f"привет {default_['bot_n']}" in message:
        say_message("привет")
    elif f"пока {default_['bot_n']}" in message:
        say_message("пока!")
        exit()
    elif f"{default_['bot_n']} открой" in message:
        cmd_name_open = message[len(list(map(str,default_['bot_n']))) + 8:100]
        l = list()

        for i in range(int(config['DEFAULT']['cmd_count_save_open'])):
            config.read('example.ini',encoding='utf8')
            l.append(config[f'COMMANDS_OPEN_{i}']['cmd_name'])
        if cmd_name_open in l:
            for i in range(int(config['DEFAULT']['cmd_count_save_open'])):
                if config[f'COMMANDS_OPEN_{i}']['cmd_name'] == cmd_name_open:
                    say_message("открываю")
                    time.sleep(1)
                    open_program(config[f'COMMANDS_OPEN_{i}']['prog_name'])
                    time.sleep(1)
                    say_message(f"открыт")
        else:
            print("Command not found")
    elif f"{default_['bot_n']} закрой" in message:
        cmd_name_kill = message[len(list(map(str,default_['bot_n']))) + 8:100]
        l = list()
        for i in range(int(config['DEFAULT']['cmd_count_save_kill'])):
            config.read('example.ini',encoding='utf8')
            l.append(config[f'COMMANDS_KILL_{i}']['cmd_name'])
        if cmd_name_kill in l:
            for i in range(int(config['DEFAULT']['cmd_count_save_kill'])):
                if config[f'COMMANDS_KILL_{i}']['cmd_name'] == cmd_name_kill:
                    say_message("закрываю")
                    time.sleep(1)
                    close_program(config[f'COMMANDS_KILL_{i}']['prog_name'])
                    time.sleep(1)
                    say_message(f"закрыт")
        else:
            print("Command not found")
    else:
        pass

    l = list()
    for i in range(int(config['DEFAULT']['cmd_count_save_say'])):
        config.read('example.ini', encoding='utf8')
        l.append(config[f'COMMANDS_SAY_{i}']['cmd_name'])

    if message in l:
        cmd_name_say = message

        for i in range(int(config['DEFAULT']["cmd_count_save_say"])):
            if config[f'COMMANDS_SAY_{i}']['cmd_name'] == cmd_name_say:
                try:
                    say_message(str(config[f'COMMANDS_SAY_{i}']['prog_name']))
                except:
                    print(str(config[f'COMMANDS_SAY_{i}']['prog_name']))
    else:
        pass
def say_message(message):
    global command_name
    message = message.lower()
    command_name = message
    print("1: " + command_name)
    file_voice_name = f"{command_name}.mp3"
    if os.path.isfile(command_name + ".mp3"):
        playsound.playsound(command_name + ".mp3")
        print("Голосовой ассистент: " + message)
    else:
        voice = gTTS(message, lang="ru")
        voice.save(file_voice_name)
        playsound.playsound(command_name + ".mp3")
        print("Голосовой ассистент: " + message)


if __name__ == '__main__':
    while True:
        command = listen_command()
        do_this_command(command)
