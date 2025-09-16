# 1. db must be at the top level to be shared across functions and sessions.
db = []

# 2. Functions must be at the top level to be importable by other files.
def regFunc(name, age, email, phone, occupation, maritalStatus, gender):
    # 3. Validate inputs BEFORE adding to the database.
    if not all([name, age, email, phone, occupation, maritalStatus, gender]):
        return {
            'status': 'fail',
            'msg': 'All fields are required.',
            'error': 'Missing one or more fields',
            'data': None
        }

    # 4. Only append to db if validation passes.
    db.append({
        'name': name.title().strip(),
        'age': age,
        'email': email.lower().strip(),  # Emails are best stored as lowercase.
        'phone': phone.strip(),
        'occupation': occupation.capitalize().strip(),
        'maritalStatus': maritalStatus.capitalize().strip(),
        'gender': gender.lower().strip()
    })

    return {
        'status': 'success',
        'msg': 'User created successfully',
        'error': None,
        'data': db[-1]
    }


def getFunc():
    """
    Generator function that yields a formatted string for each user.
    """
    for user in db:
        name = user.get('name', 'N/A')
        # 5. Bug Fix: Get gender from the 'gender' key, not 'age'.
        gender = user.get('gender', 'u') 

        if gender == 'male':
            gender_short = 'M'
        elif gender == 'female':
            gender_short = 'F'
        else:
            gender_short = 'U'  # For "Unknown" or other.
        
        # 6. Use 'yield' to return each user one by one, instead of stopping at the first.
        yield f"{name} ({gender_short})"



if __name__ == '__main__':
    # This code will only run when you execute helper.py directly
    print('Inside Helper')
