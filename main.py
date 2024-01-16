import psutil
import win32gui
import time
import win32event
import subprocess
import requests
import threading
import random
import pygetwindow
import os
import json
import pymsgbox
import win32con
import sys

# Discord -> https://discord.gg/f9KSqcepPy
os.system('start https://discord.gg/f9KSqcepPy')

cookies = open('cookies.txt', 'r').read().splitlines()
config = json.loads(open('settings//config.json', 'r').read())

total = 0
hidden = []
start = False

def hideThread():
    global hidden
    while True:
        try:
            for win in pygetwindow.getAllWindows():
                if win.title == 'Roblox':
                    win.minimize()
                    win.hide()
                    hidden.append(win)
                                
            time.sleep(0.1)

        except:
            time.sleep(0.05)



def getAuth(cookie, placeId, dir):
    global total
    with requests.session() as session:

        session.cookies['.ROBLOSECURITY'] = cookie
        session.headers['user-agent'] = 'Roblox/WinInetRobloxApp/0.567.0.5670560'
        
        # Bypasses the Visit Ratelimit
        for x in range(60):
            
            gamePost = session.post(
                'https://gamejoin.roblox.com/v1/join-game',
                json = {
                    'placeId':placeId,
                    'gameJoinAttemptId':None
                }
            )

            if gamePost.json()['joinScriptUrl'] != None:
                total += 1
                print(f'[+] Joining on {gamePost.json()["joinScript"]["UserName"]} in the game. ({total})')
                break

            time.sleep(0.5)

            if x >= 25:
                print('[-] Client failed to join the game.')
                return
        session.headers['x-csrf-token'] = session.post(
            'https://presence.roblox.com/v1/presence/register-app-presence'
        ).headers['x-csrf-token']

        authentication_ticket = session.post(
            'https://auth.roblox.com/v1/authentication-ticket/',
            headers = {
                'referer':f'https://www.roblox.com',
                'origin':'https://www.roblox.com/'
            }
        )


        ticket = authentication_ticket.headers['rbx-authentication-ticket']

        browserSignature = random.randint(1000, 10000000000)
        dir =  dir + r'\\RobloxPlayerBeta.exe'
        # globalS = os.getcwd() + r'\\GlobalBasicSettings_13.xml'
        join_ticket = f'start {dir} --app --fast  -a "https://www.roblox.com/Login/Negotiate.ashx" -t "{ticket}" -j "https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId={browserSignature}&placeId={placeId}&isPartyLeader=false"'
        # subprocess.call([f"{dir}", "--app", "--fast", "-a https://www.roblox.com/Login/Negotiate.ashx", f"-t {ticket}", f"-j https://assetgame.roblox.com/game/PlaceLauncher.ashx?request=RequestGame&browserTrackerId={browserSignature}&placeId={placeId}&isPartyLeader=false"])
        subprocess.getoutput(join_ticket)


def getPidFromApplicationName(target_application):
    for process in psutil.process_iter():
        if target_application.lower() in process.name().lower():
            num_cores = psutil.cpu_count()

            # Set the CPU affinity to the first half of the available CPU cores
            cpu_affinity = list(range(num_cores // 2))
            os.sched_setaffinity(process.pid, cpu_affinity)
        time.sleep(0.05)
    

def hideWindow(application_title):
    hwnd = win32gui.FindWindow(None, application_title)
    win32gui.ShowWindow(hwnd, 0)


def pauseApplication():
    global hidden
    while True:
            for x in hidden:
                # Deactivate the application window to pause it
                win32gui.SendMessage(x._hWnd, win32con.WM_ACTIVATEAPP, 0, 0)
            time.sleep(5)
            for x in hidden:
                # Activate the application window to resume it
                win32gui.SendMessage(x._hWnd, win32con.WM_ACTIVATEAPP, 1, 0)
            time.sleep(3)

def endSession():
    pymsgbox.alert('PRESS ENTER TO CLOSE THE BOTS (YOU CAN DO THIS AT ANY TIME)', 'IMPORTANT')
    input('[ENTER]')
    subprocess.getoutput('taskkill /f /im RobloxPlayerBeta.exe')
    # Fix to normal 
    open(config['RobloxPath'] + r'\\GlobalBasicSettings_13.xml', 'w').write(open('content//nm.xml', 'r').read())
    os.system('taskkill /f /im python.exe')
    sys.exit()


# Creates the ROBLOX multiple instances
instance = win32event.CreateMutex(None, 1, "ROBLOX_singletonMutex")
gameDir = config['versionPath']
pymsgbox.alert('DO NOT CLOSE THIS APPLICATION DURING BOTTING, RESULTS RUIN CLIENT!!!', 'WARNING')
placeId = int(input('PlaceId: '))
threading.Thread(target=hideThread,).start()

# Setting roblox settings
open(config['RobloxPath'] + r'\\GlobalBasicSettings_13.xml', 'w').write(open('content//ml.xml', 'r').read())

threading.Thread(target=endSession,).start()

if config['leaveAfter']['visitBot'] != True:
    threading.Thread(target=pauseApplication,).start()

threads = 0
while True:
    for x in cookies:
        threads += 1
        if config['upc'] == True:
            x = '_|' + x.split('_|')[1]
        threading.Thread(target=getAuth, args=( x, placeId, gameDir),).start()
        if threads >= config['threads']:
            print('Threads exceeded, waiting..')
            if config['leaveAfter']['visitBot']:
                time.sleep(config['leaveAfter']['seconds'])
                subprocess.getoutput('taskkill /f /im RobloxPlayerBeta.exe')

            # time.sleep(30)
            threads = 0

    if config['leaveAfter']['visitBot'] == False:
        time.sleep(config['leaveAfter']['seconds'])
        subprocess.getoutput('taskkill /f /im RobloxPlayerBeta.exe')

    if config['loopThroughCookies'] != True:
        break


