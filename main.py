import os
import time
import json
import random
import requests
import threading
import skidbilly as pystyle
from colorama import Fore, Style
from itertools import cycle

# Load configuration
with open('data/config.json') as f:
    config = json.load(f)
    debug       = config['Aio']['Debug']
    use_proxies = config['Generator']['Use Proxies']
    captcha_key = config['Generator'].get('captcha_key', '')

# ---------------------
# Captcha Class (not used; kept for reference)
# ---------------------
class captcha:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.api_key = captcha_key

    def createTask(self, blob):
        try:
            headers = {'Content-Type': 'application/json'}
            payload = {
                "clientKey": self.api_key,
                "task": {
                    "type": "FunCaptchaTaskProxyless",
                    "websiteURL": "https://www.roblox.com/",
                    "websitePublicKey": "A2A14B1D-1AF3-C791-9BBC-EE33CC7A0A6F",
                    "funcaptchaApiJSSubdomain": "https://roblox-api.arkoselabs.com/",
                    "data": f"{{\"blob\":\"{blob}\"}}",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
                }
            }
            r = self.session.post('https://api.example.com/createTask', json=payload, headers=headers, timeout=10)
            return r.json().get('taskId')
        except Exception as e:
            if debug:
                print(f"Captcha createTask error: {e}")
            return None

    def getResult(self, blob):
        # Placeholder: Captcha solving removed by request
        taskId = self.createTask(blob)
        if not taskId:
            return None
        payload = {
            'clientKey': self.api_key,
            'taskId': taskId
        }
        headers = {'Host': '', 'Content-Type': 'application/json'}
        while True:
            time.sleep(1)
            try:
                r = self.session.post('https://api.example.com/getResult', json=payload, headers=headers, timeout=10)
                if r.json().get('status') == "ready":
                    return r.json()['solution']['token']
            except Exception as e:
                if debug:
                    print(f"Captcha getResult error: {e}")
                return None

# ---------------------
# Statistics Class
# ---------------------
class stat:
    created = 0
    err = 0

# ---------------------
# Misc Class for Cookie Handling
# ---------------------
class Misc:
    def __init__(self):
        pass

    def get_cookie():
        try:
            with open('data/cookies.txt', 'r') as f:
                cookies = [line.strip() for line in f if line.strip()]
            return cookies
        except Exception as e:
            if debug:
                print(f"Error reading cookies: {e}")
            return []
     
    cookie = get_cookie()
    ilit_cookies = cycle(cookie)

# ---------------------
# Aio Class for Account Generation & Friend Request
# ---------------------
class aio:
    def __init__(self) -> None:
        self.session = requests.Session()

    def csrf(self):
        try:
            response = self.session.post('https://auth.roblox.com/v2/signup', timeout=10)
            return response.headers.get('x-csrf-token')
        except Exception as e:
            if debug:
                print(f"CSRF error: {e}")
            return None

    def csrfFriend(self, cookie):
        try:
            r = requests.post(
                'https://auth.roblox.com/v2/logout',
                headers={
                    'cookie': f'.ROBLOSECURITY={cookie}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
                },
                timeout=10
            )
            return r.headers.get('x-csrf-token')
        except Exception as e:
            if debug:
                print(f"csrfFriend error: {e}")
            return None

    def GetUser(self, username):
        try:
            r = self.session.get(f'https://api.roblox.com/users/get-by-username?username={username}', timeout=10)
            return r.json().get('Id')
        except Exception as e:
            if debug:
                print(f"GetUser error: {e}")
            return None

    def CheckUser(self, username):
        try:
            headers = {
                'authority': 'auth.roblox.com',
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://www.roblox.com',
                'referer': 'https://www.roblox.com/',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'x-csrf-token': self.csrf(),
            }
            payload = {
                'username': username,
                'context': 'Signup',
                'birthday': '2000-05-07T23:00:00.000Z',
            }
            response = self.session.post('https://auth.roblox.com/v1/usernames/validate', headers=headers, json=payload, timeout=10)
            data = response.json()
            if data.get('code') == 0:
                return username
            else:
                return username + ''.join(random.choices('poiuytrewqlkjhgfdsamnbvcxz0123456789', k=3))
        except Exception as e:
            if debug:
                print(f"CheckUser error: {e}")
            return None

    def get_data(self):
        try:
            payload = {'username': 'randoffmuser837735', 'password': 'oujdwadiaw985'}
            headers = {'x-csrf-token': self.csrf()}
            response = self.session.post('https://auth.roblox.com/v2/signup', json=payload, headers=headers, timeout=10)
            signup = response.json()
            # Parsing the response is fragile; adjust if Roblox changes their response
            try:
                info_str = str(signup).split("fieldData': '")[1].split("'}]")[0]
                info_list = info_str.split(',')
                if len(info_list) < 2:
                    return None
                dxBlob = info_list[1]
                captchaId = info_list[0]
                return {'captcha_id': captchaId, 'blob': dxBlob}
            except Exception as inner_e:
                if debug:
                    print(f"get_data parsing error: {inner_e}")
                return None
        except Exception as e:
            if debug:
                print(f"get_data error: {e}")
            return None

    def Generate(self):
        try:
            # Read proxies if enabled
            proxy_list = []
            try:
                proxy_list = open('data/proxies.txt', 'r').read().splitlines()
            except Exception as e:
                if debug:
                    print(f"Error reading proxies: {e}")
            if use_proxies and proxy_list:
                proxy = random.choice(proxy_list)
                proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            else:
                proxies = None

            # Get a username from file
            try:
                username_raw = random.choice(open('data/usernames.txt', 'r').read().splitlines())
            except Exception as e:
                if debug:
                    print(f"Error reading usernames: {e}")
                return
            username = self.CheckUser(username_raw)
            if username is None:
                return

            password = ''.join(random.choices('QWERTYUIOPASDFGHJKLZXCVBNMpoiuytrewqlkjhgfdsamnbvcxz0123456789', k=13))
            gender = random.randint(1, 2)
            data = self.get_data()
            if data is None:
                return
            captcha_id = data.get('captcha_id')
            blob = data.get('blob')
            # Captcha solving is removed; leave captchaToken empty
            cp_token = ""

            headers = {
                'authority': 'auth.roblox.com',
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json;charset=UTF-8',
                'dnt': '1',
                'origin': 'https://www.roblox.com',
                'referer': 'https://www.roblox.com/',
                'sec-ch-ua': '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'x-csrf-token': self.csrf(),
            }

            payload = {
                'username': username,
                'password': password,
                'birthday': '2000-02-09T23:00:00.000Z',
                'gender': gender,
                'isTosAgreementBoxChecked': True,
                'captchaId': captcha_id,
                'captchaToken': cp_token,
                'agreementIds': [
                    '54d8a8f0-d9c8-4cf3-bd26-0cbf8af0bba3',
                    '848d8d8f-0e33-4176-bcd9-aa4e22ae7905',
                ],
            }

            if use_proxies and proxies:
                response = self.session.post('https://auth.roblox.com/v2/signup', headers=headers, json=payload, proxies=proxies, timeout=10)
            else:
                response = self.session.post('https://auth.roblox.com/v2/signup', headers=headers, json=payload, timeout=10)

            if "userId" in response.text:
                stat.created += 1
                userID = response.json()['userId']
                cookie = response.cookies.get('.ROBLOSECURITY', '')
                print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Style.RESET_ALL} Created Account ({stat.created})")
                print(cookie[0:200])
                # Save results to the specified files
                with open('results/accounts.txt', 'a') as f:
                    f.write(f'{username}:{password}:{userID}:{cookie}\n')
                with open('results/account.txt', 'a') as f:
                    f.write(f'{username}:{password}\n')
                with open('results/withproxy.txt', 'a') as f:
                    f.write(f'{cookie}:{proxy if use_proxies and proxies else "NoProxy"}\n')
                with open('results/cookies.txt', 'a') as f:
                    f.write(f'{cookie}\n')
            else:
                stat.err += 1
                if debug:
                    print(f"{Fore.RED}[ {Fore.GREEN}x {Fore.RED}]{Style.RESET_ALL} Failed to create account. Response: {response.text}")
        except Exception as e:
            if debug:
                print(e)

    def friend(self, userId):
        try:
            cookie = next(Misc.ilit_cookies)
            headers = {
                'authority': 'friends.roblox.com',
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json;charset=utf-8',
                'cookie': f'.ROBLOSECURITY={cookie}',
                'origin': 'https://web.roblox.com',
                'referer': 'https://web.roblox.com/',
                'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                'x-csrf-token': aio.csrfFriend(cookie),
            }
            response = self.session.post(f'https://friends.roblox.com/v1/users/{userId}/request-friendship', headers=headers, timeout=10)
            try:
                if response.json().get('success') == True:
                    print(f"{Fore.BLUE}[ {Fore.GREEN}+ {Fore.BLUE}]{Style.RESET_ALL} Request Sent")
            except:
                pass
            try:
                errors = response.json().get('errors')
                if errors and errors[0].get('code') == 5:
                    print(f"{Fore.BLUE}[ {Fore.RED}x {Fore.BLUE}]{Style.RESET_ALL} Request already sent")
            except:
                pass
        except Exception as e:
            if debug:
                print(e)

# ---------------------
# Menu Class for User Interaction
# ---------------------
class menu:
    def __init__(self):
        pass

    def main(self):
        os.system('cls')
        os.system('title Roblox Aio ^| Twiddle Menu')
        pystyle.Write.Print("""
                                            ╦═╗┌─┐┌┐ ┬  ┌─┐─┐ ┬  ┌─┐┬┌─┐
                                            ╠╦╝│ │├┴┐│  │ │┌┴┬┘  ├─┤││ │
                                            ╩╚═└─┘└─┘┴─┘└─┘┴ └─  ┴ ┴┴└─┘""", pystyle.Colors.purple_to_blue, interval=0)

        print("\n\n")
        print(f'                                              {Fore.RED}[{Fore.RESET} {Fore.BLUE}1{Fore.RESET} {Fore.RED}]{Style.RESET_ALL} Account Creator')
        print(f'                                              {Fore.RED}[{Fore.RESET} {Fore.BLUE}2{Fore.RESET} {Fore.RED}]{Style.RESET_ALL} Friend User')
        print("\n\n\n")
        try:
            choice = int(input(f"{Fore.GREEN}[ {Fore.CYAN}?{Fore.GREEN} ] Enter Choice {Fore.GREEN}> {Fore.WHITE}"))
        except Exception as e:
            if debug:
                print(f"Invalid input: {e}")
            return

        if choice == 1:
            os.system('cls')
            pystyle.Write.Print("""
                                            ╔═╗┌─┐┌┐┌┌─┐┬─┐┌─┐┌┬┐┌─┐┬─┐
                                            ║ ╦├┤ │││├┤ ├┬┘├─┤ │ │ │├┬┘
                                            ╚═╝└─┘┘└┘└─┘┴└─┴ ┴ ┴ └─┘┴└─""", pystyle.Colors.purple_to_blue, interval=0)
            print("")
            threads = input(f"{Fore.GREEN}[{Fore.CYAN}?{Fore.GREEN}] Accounts To Create {Fore.CYAN}> {Fore.WHITE}")
            try:
                threads = int(threads)
            except:
                print(f"{Fore.RED}Invalid number of threads.")
                return

            thread_list = []
            for i in range(threads):
                t = threading.Thread(target=aio().Generate)
                t.start()
                thread_list.append(t)

            for t in thread_list:
                t.join()

            time.sleep(2.2)
            input(f"{Fore.RED}[{Fore.RESET}{Fore.BLUE}Cookie Creator{Fore.RESET}{Fore.RED}]{Style.RESET_ALL} Completed tasks! Press Enter To Return To The Menu {Fore.YELLOW}> {Style.RESET_ALL}")
            menu().main()

        elif choice == 2:
            os.system('cls')
            pystyle.Write.Print("""
                                            ╔═╗┬─┐┬┌─┐┌┐┌┌┬┐
                                            ║ ╦├┬┘│├┤ │││ ││
                                            ╚  ┴└─┴└─┘┘└┘─┴┘""", pystyle.Colors.purple_to_blue, interval=0)
            print("")
            username = input(f"{Fore.GREEN}[{Fore.CYAN}?{Fore.GREEN}] Username {Fore.CYAN}> {Fore.WHITE}")
            threads = input(f"{Fore.GREEN}[{Fore.CYAN}?{Fore.GREEN}] Requests to send {Fore.CYAN}> {Fore.WHITE}")
            try:
                threads = int(threads)
            except:
                print(f"{Fore.RED}Invalid number of threads.")
                return

            userId = aio().GetUser(username)
            if userId is None:
                print(f"{Fore.RED}Could not retrieve user ID for {username}")
                time.sleep(2)
                menu().main()
                return

            thread_list = []
            for i in range(threads):
                t = threading.Thread(target=aio().friend, args=(userId,))
                t.start()
                thread_list.append(t)

            for t in thread_list:
                t.join()

            time.sleep(2.2)
            input(f"{Fore.RED}[{Fore.RESET}{Fore.BLUE}Friend User{Fore.RESET}{Fore.RED}]{Style.RESET_ALL} Completed tasks! Press Enter To Return To The Menu {Fore.YELLOW}> {Style.RESET_ALL}")
            menu().main()

        else:
            print(f"{Fore.RED}[{Fore.RESET}{Fore.RED}x{Fore.RESET}{Fore.RED}] Invalid Input!")
            time.sleep(1.5)
            menu().main()

menu().main()
