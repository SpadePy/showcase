from assets import *
from assets.utils.utility import *


class User:
    def __init__(self, username: str, password: str, license_key: str = None):
        self.username = username
        self.password = password
        self.license_key = license_key

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'license_key': self.license_key
        }

class LoginSystem:
    api = "http://127.0.0.1:5000/api"

    def __init__(self):
        self.session = requests.Session()
        self.ip = None

    def register(self, user: User):
        response = self.session.post(f"{self.api}/register", json=user.to_dict())
        if response.status_code == 201:
            print("Registration successful")
            return True  
        else:
            print(f"error > {response.json().get('error')}")
            time.sleep(4)
            main() 

    def login(self, user: User):
        response = self.session.post(f"{self.api}/login", json=user.to_dict())
        if response.status_code == 200:
            self.ip = response.json().get('ip')
            print("Login successful")
            return True  
        elif response.status_code == 403: 
            os.system("title License Expired")
            os.system("cls")
            print("Your license has expired.")
            print()
            renew = input(gradient("Do you have a new license? [y/n] > ")).lower()
            if renew == 'y':
                new_license_key = input(gradient("New License > "))
                renew_response = self.session.post(f"{self.api}/renew", json={
                    'username': user.username,
                    'new_license_key': new_license_key
                })
                if renew_response.status_code == 200:
                    print("License Updated.")
                    return True  
                else:
                    print(f"Error: {renew_response.json().get('error')}")
            else:
                print("Please get a new license.")
                time.sleep(4)
                main()
        else:
            print(f"Error: {response.json().get('error')}")
            time.sleep(4)
            main()

    def menu(self):
        os.system("cls")
        os.system("title Main Menu")
        spadeprint.printlogo()
        print(gradient(center(f"""
<< 1 >> Something   << 2 >> Something
        """)))

        choice = input(gradient("             Menu@Spade$~ Choice →   "))
        if choice == '1':
            pass
        elif choice == '2':
            pass
        else:
            print(gradient("Invalid Option."))

def main():
    os.system("title Login Or Register")  
    system = LoginSystem()

    while True:
        loginprint.printlogo()
        print(gradient(center(f"""
<< 1 >> Login   << 2 >> Register   << 3 >> Exit
        """)))
        print()
        action = input(gradient("             Login@Spade$~ Choice →   "))

        if action == '1':
            print()
            username = input(gradient(center("Username > ")))
            password = input(gradient(center("Password > ")))
            user = User(username, password)
            time.sleep(2)
            if system.login(user):  
                system.menu()
        elif action == '2':
            print()
            username = input(gradient(center("Username > ")))
            password = input(gradient(center("Password > ")))
            license_key = input(gradient(center("License > ")))
            time.sleep(2)
            user = User(username, password, license_key)
            if system.register(user): 
                system.menu()
        elif action == '3':
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
