from helper import regFunc, getFunc


def main():
    regOn = True

    while regOn:
        name = input('Enter your name: ')
        age = input('Enter your age: ')
        gender = input('Enter your gender: ')
        maritalStatus = input('Enter your marital status: ')
        email = input('Enter your email: ')
        phone = input('Enter your phone: ')
        occupation = input('Enter your occupation: ')

        if name and age and email and phone and occupation and maritalStatus and gender:
            response = regFunc(name, age, email, phone, occupation,maritalStatus, gender)
            print(f"{response['status']}: {response['msg']}")
            regOn = False

    # Get all users
    for user in getFunc():
        print(user)
 
    

if __name__ == '__main__':
    main()