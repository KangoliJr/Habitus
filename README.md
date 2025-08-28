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
