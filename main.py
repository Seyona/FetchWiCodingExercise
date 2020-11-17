from fastapi import FastAPI
import uvicorn
from user import User

app = FastAPI()

# Create a dummy user for the mock api calls
userId = 0
data = {'id': userId, 'name': "user", 'transactions': [], 'allTransactions': [], 'allPayers': []}
users = {data['name']: User(**data)}


@app.get("/")
def read_root():
    return {"message": "Fetch WI: Coding Exercise - Backend"}

@app.get("/user/createUser/user_name")
def create_user(user_name: str):
    user_name = str.lower(user_name)
    global userId
    userId += 1
    userData = {'id': userId, 'name': user_name, 'transactions': [], 'allTransactions': [], 'allPayers': []}
    newUser = users.get(userData['name'], None)
    if newUser is not None:
        return "Requested user already exists"

    users[userData['name']] = User(**userData)
    return f'{userData["name"]} created'


"""
Gets the point balance by payer for the specified user
"""
@app.get("/points/balance/{user_name}")
def get_balance(user_name: str):
    user_name = str.lower(user_name)
    user = users.get(user_name, None)

    if user is None:
        return {"message": "Defined user does not exist"}

    sumByPayer = user.sum_transactions_by_payer()
    values = []
    for key in sorted(sumByPayer.keys()):
        value = sumByPayer[key]
        values.append(f'[{key}, {value} points]')

    if not values:
        return "No Payer transactions exist"
    else:
        return ','.join(values)


"""
Adds points for the passed user for the specified payer.
   - Will create a new payer entry for the user if they do not exist.
   - Will not create a user if they do not exist

Returns a message that displays the success or failure of the api
"""
@app.put("/points/add/{user_name}/{payer_name}/{points}")
def add_points(user_name: str, payer_name: str, points: int, date: str):
    user_name = str.lower(user_name)
    payer_name = str.upper(payer_name)

    user = users.get(user_name, None)
    if user is not None:

        errMsg = user.add_transaction(payer_name, points, date)

        if errMsg == "":
            return {"message": f'{points} points added to {user_name} for {payer_name}'}
        else:
            return {"message": errMsg}

    else:
        return {"message": "Passed user is not defined"}


"""
Deducts points from the specified user's point total 

Returns a list of payers and how many points were deducted from each
"""
@app.patch("/points/deduct/{user_name}/{points}")
def deduct_points(user_name: str, points: int):
    user_name = str.lower(user_name)
    user = users.get(user_name, None)

    deducted = user.deduct_points_from_payers(points)
    values = []
    for key in sorted(deducted.keys()):
        value = deducted[key]
        values.append(f'[{key}, {value} points, now]')
    return ','.join(values)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)