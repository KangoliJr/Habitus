Habitus project is a real estate project. It is house hunting easier application that makes house searching easier and easier to find your desired home.
it consists of 4 crucial apps to ensure a proper flexibility. The first app is the accounts which acts a the central hub for access that configures registration and login. The second app is the airbnb. The app is used to offer airbnb services; it involves the host and the customer who intends to book an airbnbn house. The third app is the rental app. The app offers rental services. It involves the landlord and the tenant. A tenant can be able to seasrch for a rental home where he/she desires to be live and also offer one to be a landlord if they want to rent out a house. The fourth app is the owned_home app. This app offer buying and selling of your properties. It enables one to search for a permanent house that would one want to settle in or sell it to a potential buyer. This four app ensures flexibility to navigate from one app to another.


API End points

AIrbnb
airbnb/api/(API root)
(GET/POST)airbnb/api/houses/
GET/airbnb/api/houses/<id>/
(PATCH/PUT)/airbnb/api/houses/<id>/
DELETE/airbnb/api/houses/<id>/

Accounts
accounts/api/(API root)
GET/accounts/api/users/
GET/accounts/api/users/me
GET/accounts/api/profiles/
(POST/PATCH/PUT)/accounts/api/profiles/<id> 
PATCH/accounts/api/profiles/upgrade-role
GET/accounts/api/token/
POST/accounts/api/token/refresh/
GET/accounts/api/register/
POST accounts/api/register/

Rental
GET /rental/api/(API root)
GET /rental/api/houses/
GET /rental/api/applications/
GET /rental/api/agreements/

Owned_home
(POST/GET)owned-home/api/houses/
(GET/PUT/DELETE)owned-home/api/houses/{id}/
(GET/POST)owned-home/api/purchases/



POSTMAN API TETSING
**ACCOUNTS**
LOGIN
http://127.0.0.1:8000/accounts/api/token/

{
    "username": "jojo",
    "password": "Mrs.Jojo@123"

}

REGISTRATION

http://127.0.0.1:8000/accounts/api/register/
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-05-15",
    "age": 35,
    "gender": "male",
    "phone_number": "0712345678",
    "country": "USA"
}
MANAGE USER PROFILE
http://127.0.0.1:8000/accounts/api/profiles/<id>/
{
    "first_name": "John",
    "country": "USA"
}

CHANGE PASSWORD
http://127.0.0.1:8000/accounts/api/change-password/

{
    "old_password": "Mrs.Jojo@1234",
    "new_password": "Mrs.Jojo@12345"
}

UPGRADE USER ROLE
http://127.0.0.1:8000/accounts/api/upgrade-role/

{
    "role_to_upgrade": "host"
}
{
    "role_to_upgrade": "buyer"
}
{
    "role_to_upgrade": "landlord"
}


**AIRBNB**
