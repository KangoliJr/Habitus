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
    "username": "james",
    "email": "james@gmail.com",
    "password": "Mr.JamesTom@123",
    "first_name": "James",
    "last_name": "Tom",
    "date_of_birth": "1990-05-15",
    "age": 35,
    "gender": "male",
    "phone_number": "0712345678",
    "country": "CANADA"
}
MANAGE USER PROFILE
Edit profile
Method Get
http://127.0.0.1:8000/accounts/api/profiles/<id>/
{
    "first_name": "John",
    "country": "USA"
}

CHANGE PASSWORD
Method Post
http://127.0.0.1:8000/accounts/api/change-password/

{
    "old_password": "Mr.JamesTom@123",
    "new_password": "Mr.JamesTom@12345"
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
1 Creating a new house
http://127.0.0.1:8000/airbnb/api/houses/

{
    "name": "Luxury House in the Maldives",
    "description": "A beautiful house with a great view.",
    "price": 15000.00,
    "furnishing_style": "Fully_Furnished",
    "bedroom": "4_bedroom",
    "bathroom": "3_bathroom",
    "location": "Nairobi",
    "rules": "No parties allowed.",
    "amenities": "Wi-Fi, Pool, Gym"
}
2 adding images to the particular house
http://127.0.0.1:8000/airbnb/api/houses/<house_id>/images/

3 Update a House 
PATCH
http://127.0.0.1:8000/airbnb/api/houses/<house_id>/
{
    "price": 16000.00,
    "amenities": "Wi-Fi, Pool, Gym, Smart TV"
}

4 Delete a house
 http://127.0.0.1:8000/airbnb/api/houses/<house_id>/


5 Making a booking
http://127.0.0.1:8000/airbnb/api/houses/<house_id>/bookings/

{
    "checkin": "2025-10-01",
    "checkout": "2025-10-05"
    "house": "2"
}

6 Deleting a booking
http://127.0.0.1:8000/airbnb/api/bookings/<booking id>/
{
    "checkin": "2025-10-01",
    "checkout": "2025-10-05",
    "house": "2"
}

7 Get the house
GET
 http://127.0.0.1:8000/airbnb/api/houses/<house id>/
 {
    "checkin": "2025-10-01",
    "checkout": "2025-10-05",
    "house": "2"
 }


**RENTAL HOUSE**
Ld
1 Create a rental house
Method POST
http://127.0.0.1:8000/rental/api/houses/

{
    "name": "Waterfalls Apartment",
    "description": "4-bedroom apartment with a great view.",
    "monthly_rent": 12000.00,
    "security_deposit": 2400.00,
    "furnishing_style": "Semi_Furnished",
    "bedroom": "4_bedroom",
    "bathroom": "3_bathroom",
    "location": "Lavington",
    "rules": "No smoking.",
    "amenities": "Wi-Fi, Balcony, Parking",
    "is_available": true
}

2 Add an image
Method Post
http://127.0.0.1:8000/rental/api/houses/<house_id>/images/


Tenant
4 List houses
Method GET
http://127.0.0.1:8000/rental/api/houses/

5 submit rental application
Method Post
http://127.0.0.1:8000/rental/api/houses/<house_id>/applications/
{
    "move_in_date": "2025-10-01",
    "lease_duration_months": 12
    "house_id": "6"
}

6 view applications
Method GET
http://127.0.0.1:8000/rental/api/applications/

7 view lease agreement
Method GET
http://127.0.0.1:8000/rental/api/agreements/<agreement_id>/


**OWNED HOME**
1 create a house
Method Post
http://127.0.0.1:8000/owned-home/api/houses/
{
    "name": "Luxury Home Estate",
    "description": "A beautiful 3-bedroom house with a garden.",
    "price": 650000.00,
    "furnishing_style": "Fully_Furnished",
    "bedroom": "5_bedroom",
    "bathroom": "4_bathroom",
    "location": "Karen",
    "rules": "No pets.",
    "amenities": "Swimming Pool, Garage"
}

2 Add image
Method Post
http://127.0.0.1:8000/owned-home/api/houses/<house_id>/images/

3 view the house units
Method Ger
http://127.0.0.1:8000/owned-home/api/houses/

buyer
4 List the houses available
Method Get
 http://127.0.0.1:8000/owned-home/api/houses/

 5 submit purchaese
 Method Post
 http://127.0.0.1:8000/owned-home/api/houses/<house_id>/purchases/

 6 View the purchases
 Method Get
 http://127.0.0.1:8000/owned-home/api/houses/<house_id>/purchases/
