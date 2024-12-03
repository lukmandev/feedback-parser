from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.sync import TelegramClient
import os
import json
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument, PeerUser, PeerChat, PeerChannel
import time
from datetime import datetime

def inviting(client, channel, users):
    client(InviteToChannelRequest(
        channel=channel,
        users=[users]
    ))

def parse_media(media):
    if media is None:
        return None
        
    media_info = {
        "type": type(media).__name__,
        "file_name": None,
        "mime_type": None,
        "size": None
    }
        
    if isinstance(media, MessageMediaPhoto):
        media_info["type"] = "Photo"
        
    return media_info
    
def parse_sender(sender):
    if sender is None:
        return None
        
    return {
        "id": sender.id,
        "username": sender.username,
        "first_name": sender.first_name,
        "last_name": sender.last_name,
    }

def parsing(client, index: int, id: bool, name: bool):
    output_file='telegram_messages.json'
    messages_data = []
            
    for message in client.iter_messages(index):
        if message.sender is None:
            continue
        if message.sender.id != 5923938082:
            continue

        message_data = {
            "id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "text": message.text,
                    
            "media": parse_media(message.media),

            "sender": parse_sender(message.sender),
        }
                
        messages_data.append(message_data)
            
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(messages_data, f, ensure_ascii=False, indent=2)
    # if name:
    #     with open('usernames.txt', 'r+') as f:
    #         usernames = f.readlines()
    #         for user in all_participants:
    #             if user.username:
    #                 if ('Bot' not in user.username) and ('bot' not in user.username):
    #                     if (('@' + user.username + '\n') not in usernames):
    #                         f.write('@' + user.username + '\n')
    #                     else:
    #                         continue
    #                 else:
    #                     continue
    #             else:
    #                 continue
    # if id:
    #     with open('userids.txt', 'r+') as f:
    #         userids = f.readlines()
    #         for user in all_participants:
    #             if (str(user.id) + '\n') not in userids:
    #                 f.write(str(user.id) + '\n')


def config():
    while True:
        os.system('cls||clear')

        with open('options.txt', 'r+') as f:
            if not f.readlines():
                f.write("NONEID\n"
                        "NONEHASH\n"
                        "True\n"
                        "True\n")
                continue
                
        options = getoptions()
        sessions = []
        for file in os.listdir('.'):
            if file.endswith('.session'):
                sessions.append(file)

        key = str(input((f"1 - Обновить api_id [{options[0].replace('\n', '')}]\n"
                         f"2 - Обновить api_hash [{options[1].replace('\n', '')}]\n"
                         f"3 - Парсить user-id [{options[2].replace('\n', '')}]\n"
                         f"4 - Парсить user-name [{options[3].replace('\n', '')}]\n"
                         f"5 - Добавить аккаунт юзербота[{len(sessions)}]\n"
                          "6 - Сбросить настройки\n"
                          "e - Выход\n"
                          "Ввод: ")
                    ))

        if key == '1':
            os.system('cls||clear')
            options[0] = str(input("Введите API_ID: ")) + "\n"

        elif key == '2':
            os.system('cls||clear')
            options[1] = str(input("Введите API_HASH: ")) + "\n"

        elif key == '3':
            if options[2] == 'True\n':
                options[2] = 'False\n'
            else:
                options[2] = 'True\n'

        elif key == '4':
            if options[3] == 'True\n':
                options[3] = 'False\n'
            else:
                options[3] = 'True\n'
        
        elif key == '5':
            os.system('cls||clear')
            if options[0] == "NONEID\n" or options[1] == "NONEHASH":
                print("Проверьте api_id и api_hash")
                time.sleep(2)
                continue

            print("Аккаунты:\n")
            for i in sessions:
                print(i)

            phone = str(input("Введите номер телефона аккаунта: "))
            client = TelegramClient(phone, int(options[0].replace('\n', '')), 
                                    options[1].replace('\n', '')).start(phone)
            
        elif key == '6':
            os.system('cls||clear')
            answer = input("Вы уверены?\nAPI_ID и API_HASH будут удалены\n"
                           "1 - Удалить\n2 - Назад\n"
                           "Ввод: ")
            if answer == '1':    
                options.clear()
                print("Настройки очищены.")
                time.sleep(2)
            else:
                continue

        elif key == 'e':
            os.system('cls||clear')
            break

        with open('options.txt', 'w') as f:
            f.writelines(options)


def getoptions():
    with open('options.txt', 'r') as f:
        options = f.readlines()
    return options
