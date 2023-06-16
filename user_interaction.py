#!/usr/bin/env python3

class User_Interaction:

    #user request choice
    def request_menu(self, choice=None):
        print(); print("-"*40); print()
        #model generates the code according to user description
        print("1.  Generate Raw Code")
        print(f"\tRequest model for code according to a description you provide.")
        #upload script instead of the model generating the code
        print("2.  Load Raw Code Script From File")
        print("3.  Add Argparse")
        print("4.  Exception Handling and Logging")
        print("5.  User Custom Request")
        print(f"\tRequirement: code to be already loaded. A JSON file to request "
              f"the format of the response.")
        print("6.  Run Program With Enter Debug/Logs Loop")
        print(f"\tRun the program and upon errors send the log error captured for the model to amend the code "
              f"accordingly.")
        print("7.  Add Docstrings To Program Code.")
        print("8. Set Menu Sequence")
        print("9. Run All")
        print("10. Exit")

        while True:
            print()
            if choice is None:
                choice = input("Choose your request: ")
            else:
                print("Choose your request: ", choice)

            match choice:
                case _:
                    if choice.isdigit() and 1 <= int(choice) <= 12:
                        return choice
                    else:
                        print(); print(f"\033[41mInvalid Option\033[0m")
                        choice = None

    @staticmethod
    def broken_json_user_action():
        while True:
            user_choice = input("The model's JSON response is broken, re-request? y/n: ")
            match user_choice.lower():
                case 'y':
                    return True
                case 'n':
                    return False
                case _:
                    print("Invalid selection.")
                    continue

    def request_input_from_user(self, mssg):
        return input(mssg)

    @staticmethod
    def user_choice_two_options(mssg, mssg_option1=None, mssg_option2=None, mssg_option3=None, option1="y", option2="n"):
        while True:
            choice = input(mssg)
            if choice.lower() == option1:
                if mssg_option1 is not None:
                    print(mssg_option1)
                break
            elif choice.lower() == option2:
                if mssg_option2 is not None:
                    print(mssg_option2)
                break
            else:
                if mssg_option3 is not None:
                    print(mssg_option3)
                continue
        return choice.lower()


def broken_json_user_action():
    return None
