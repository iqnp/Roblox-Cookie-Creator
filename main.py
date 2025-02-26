import os
import platform

class menu:
    def __init__(self):
        pass

    def main(self):
        # Clear the screen based on the OS
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')  # For Linux and macOS

        # Set terminal title based on the OS
        if platform.system() == "Windows":
            os.system(f'title Roblox Aio ^| Twiddle Menu')
        else:
            # No equivalent for title command on Linux/macOS by default
            pass

        pystyle.Write.Print(""" 
                                            ╦═╗┌─┐┌┐ ┬  ┌─┐─┐ ┬  ┌─┐┬┌─┐
                                            ╠╦╝│ │├┴┐│  │ │┌┴┬┘  ├─┤││ │
                                            ╩╚═└─┘└─┘┴─┘└─┘┴ └─  ┴ ┴┴└─┘""", pystyle.Colors.purple_to_blue, interval=0)
        
        print("\n\n")

        print(f'                                              {Fore.RED}[{Fore.RESET} {Fore.BLUE}1{Fore.RESET} {Fore.RED}]{Fore.RESET} Account Creator')
        print(f'                                              {Fore.RED}[{Fore.RESET} {Fore.BLUE}2{Fore.RESET} {Fore.RED}]{Fore.RESET} Friend User')

        print("\n\n\n")
        choice = int(input(f"{Fore.GREEN} [ {Fore.CYAN}?{Fore.GREEN} ] Enter Choice {Fore.GREEN}> {Fore.WHITE}"))  

        if choice == 1:
            os.system('cls' if platform.system() == "Windows" else 'clear')
            pystyle.Write.Print(""" 
                                            ╔═╗┌─┐┌┐┌┌─┐┬─┐┌─┐┌┬┐┌─┐┬─┐
                                            ║ ╦├┤ │││├┤ ├┬┘├─┤ │ │ │├┬┘
                                            ╚═╝└─┘┘└┘└─┘┴└─┴ ┴ ┴ └─┘┴└─""", pystyle.Colors.purple_to_blue, interval=0)
            print("")
            threads = input(f"{Fore.GREEN}[{Fore.CYAN} ? {Fore.GREEN}] Accounts To Create {Fore.CYAN}> {Fore.WHITE}")

            for i in range(int(threads)):
                x = threading.Thread(target=aio().Generate)
                x.start()

            for i in range(int(threads)):
                x.join()
            time.sleep(2.2)
            input(f"{Fore.RED}[{Fore.RESET}{Fore.BLUE}Cookie Creator{Fore.RESET}{Fore.RED}]{Fore.RESET} Completed tasks! Press Enter To Return To The Menu {Fore.YELLOW}>{Fore.RESET} ")
            menu().main()

        if choice == 2:
            os.system('cls' if platform.system() == "Windows" else 'clear')
            pystyle.Write.Print(""" 
                                            ╔═╗┬─┐┬┌─┐┌┐┌┌┬┐
                                            ╠╣ ├┬┘│├┤ │││ ││
                                            ╚  ┴└─┴└─┘┘└┘─┴┘""", pystyle.Colors.purple_to_blue, interval=0)
            print("")
            username = input(f"{Fore.GREEN}[{Fore.CYAN} ? {Fore.GREEN}] Username {Fore.CYAN}> {Fore.WHITE}")
            threads = input(f"{Fore.GREEN}[{Fore.CYAN} ? {Fore.GREEN}] Requests to send {Fore.CYAN}> {Fore.WHITE}")

            userID = aio().GetUser(username)

            for i in range(int(threads)):
                x = threading.Thread(target=aio().friend, args=(userID,))
                x.start()

            for i in range(int(threads)):
                x.join()
            time.sleep(2.2)
            input(f"{Fore.RED}[{Fore.RESET}{Fore.BLUE}Friend User{Fore.RESET}{Fore.RED}]{Fore.RESET} Completed tasks! Press Enter To Return To The Menu {Fore.YELLOW}>{Fore.RESET} ")
            menu().main()
