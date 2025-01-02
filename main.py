import time, os, random
from source import Browser

ok, fail = 0, 0

def create(gender: int = None, password: str = None):
    global ok, fail
    chrome = Browser()
    # generate new email
    email = chrome.tmail.new_email()
    # register
    gender = int(gender) if gender else random.choice([1, 2])
    register = chrome.register.new(email=email, gender=gender)

    if register == 1:
        on_time_password = chrome.tmail.get_code()
        print('OTP: '+ str(on_time_password))
        register = chrome.register.confirm(code=on_time_password)

        if register == 1:
            ok +=1
            print(f'- Nama     : {chrome.register.user.firstname} {chrome.register.user.lastname} {" "* 20}')
            print(f'- Email    : {email}')
            print(f'- Password : {chrome.register.password}')
            print(f'- Gender   : {gender}')
            print(f'- Cookie   : {chrome.register.cookie()}\n')
        else:
            fail +=1
    else:
        fail +=1

    print(f'./XZero (Code: {register}) Ok: -{ok} Fail: -{fail} {" "*20}', end='\r')
    chrome.quit()

if __name__ == "__main__":
    os.system('clear')
    print(f' _____             _           _   ')
    print(f'|   __|___ ___ ___| |_ ___ ___| |_ ')
    print(f'|   __| .\'|  _| -_| . | . | . | \'_|')
    print(f'|__|  |__,|___|___|___|___|___|_,_| Zero!')
    print()
    print(f'〈1〉 Create Account.')
    print(f'〈2〉 List account')
    print()
    chsr = input('Chose: ')
    print()

    if '1' in chsr:
        passwd = input('Password (default: random) : ')
        gender = input('Gender (default: random)   : ')
        print(gender or None)
        print()

        while True:
            create(gender=gender or None, password=passwd or None)
            


