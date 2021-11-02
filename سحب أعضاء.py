from time import sleep
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import (PeerFloodError, UserNotMutualContactError ,
                                          UserPrivacyRestrictedError, UserChannelsTooMuchError,
                                          UserBotError, InputUserDeactivatedError)
from telethon.tl.functions.channels import InviteToChannelRequest
import time, os, sys, json,requests
print("""\033[1;92m
                  _         _
                 | |       | |
  _ __ ___   __ _| |__   __| |_   _
| '_ ` _ \ / _` | '_ \ / _` | | | |
| | | | | | (_| | | | | (_| | |_| |
|_| |_| |_|\__,_|_| |_|\__,_|\__, |
                               __/ |
                              |___/   

\033[1;93m\033[1;92mاداة نقل جهات تلجرام\033[1;93m\033[1;91m 
 ---------------------------
 \033[1;91m(\033[1;92m*\033[1;91m) \033[1;97mAUTHOR  : HIT MAN AND KASPER
 \033[1;91m(\033[1;92m*\033[1;91m) \033[1;97mTelegram   : @aarrr
 \033[1;91m(\033[1;92m*\033[1;91m) \033[1;97mGITHUB     : github.com/mahdyababneh282
""")
COLORS = {
    "re": "\u001b[31;1m",
    "gr": "\u001b[32m",
    "ye": "\u001b[33;1m",
}
re = "\u001b[31;1m"
gr = "\u001b[32m"
ye = "\u001b[33;1m"
def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text
if os.path.isfile('ملف مهم.txt'):
    with open('ملف مهم.txt', 'r') as r:
        data = r.readlines()
    api_id = data[0]
    api_hash = data[1]
else:
    api_id = input('Enter api_id: ')
    api_hash = input('Enter api_hash: ')
    with open('ملف مهم.txt', 'w') as a:
        a.write(api_id + '\n' + api_hash)
client = TelegramClient('anon', api_id, api_hash)
async def main():
    async def getmem():
        print('')
        print('')        
        a=0
        for i in channel:
            print(gr+'['+str(a)+']', i.title)
            a += 1
        opt1 = int(input(ye+'اختر رقم المجموعة التي تريد نقل اليها الاعضاء: '))
        my_participants = await client.get_participants(channel[opt1])
        target_group_entity = InputPeerChannel(channel[opt1].id, channel[opt1].access_hash)
        my_participants_id = []
        for my_participant in my_participants:
            my_participants_id.append(my_participant.id)
        with open('معلومات الاعضاء.txt', 'r') as r:
            users = json.load(r)
        count = 1
        i = 0
        for user in users:
            if count%50 == 0:
                print(colorText(wt))
            elif count >= 300:
                await client.disconnect()
                break
            elif i >= 8:
                await client.disconnect()
                break
            count+=1
            time.sleep(1)
            if user['uid'] in my_participants_id:
                print(gr+' موجود بالمجموعة')
                continue
            else:
                try:
                    user_to_add = InputPeerUser(user['uid'], user['access_hash'])
                    add = await client(InviteToChannelRequest(target_group_entity,[user_to_add]))
                    print(gr+'تم اضافة', str(user['uid']))
                    sleep(10)                    
                except PeerFloodError:
                    print(re+"تلجرام حظرك من استخدام الاداة مؤقتا.")
                    i += 1
                except UserPrivacyRestrictedError:
                    print(re+"المطي قافل الجهات")
                    i = 0
                except UserBotError:
                    print(re+"تم اضافة بنجاح.")
                    sleep(10)
                    i = 0
                except InputUserDeactivatedError:
                    print(re+"ماعنده يوزر")
                    i = 0
                except UserChannelsTooMuchError:
                    print(re+"موجود بالمجموعة")
                except UserNotMutualContactError:
                    print(re+'موجود بالمجموعة.')
                    i = 0
                except Exception as e:
                    print(re+"Error:", e)
                    i += 1
                    continue    
    chats = []
    channel = []
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    chats.extend(result.chats)
    for a in chats:
        try:
            if True:
                channel.append(a)
        except:
            continue
    a = 0
    print('')
    print('')
    print(ye+'لا يمكنك النقل الا من المجموعات.')
    for i in channel:
        print(gr+'['+str(a)+']', i.title)
        a += 1
    op = input(ye+'اختر المجموعة التي تريد النقل منها: ')
    if op == '':
        print(ye+'انتظر قليلا...')
        await getmem()
        sys.exit()
    else: 
        pass
    opt = int(op)
    print('')
    print(ye+'[+] جاري استخراج معلومات الاعضاء...')
    target_group = channel[opt]
    all_participants = []
    mem_details = []
    all_participants = await client.get_participants(target_group)
    for user in all_participants:
        try:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                firstname = user.first_name
            else:
                firstname = ""
            if user.last_name:
                lastname = user.last_name
            else:
                lastname = ""
            new_mem = {
                'uid': user.id,
                'username': username,
                'firstname': firstname,
                'lastname': lastname,
                'access_hash': user.access_hash
            }
            mem_details.append(new_mem)
        except ValueError:
            continue    
    with open('معلومات الاعضاء.txt', 'w') as w:
        json.dump(mem_details, w)
    time.sleep(1)
    print(ye+'تم سحب المعلومات.....')
    await getmem()
    await client.disconnect()
with client:
    client.loop.run_until_complete(main())