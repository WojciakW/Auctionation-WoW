# Auctionation-WoW
## A Python-Django social web app for World of Warcraft Classic live auction house statistics.

Author: Wojciech Wójciak (wojciech.wojciak22@gmail.com)

All data is provided by Blizzard's WoW Classic API.

### Key features:
- Automated 1-hour-cycle database handling:
  - fetching live World of Warcraft auctions data from official Blizzard API,
  - computing various statistics,
  - archiving data.
- Possibility to view every single item data on every official realm, faction side, that is:
  - auctions count,
  - lowest buyout,
  - mean buyout,
  - median buyout,
- Data presented in form of graphs,
- User account base,
- Support for comments on any item stats,
- Various UX, like:
    - one field for item OR auction search,
    - dynamic page rewriting,
    - user Observed items list,


### Technologies used:
- Django 4.0,
- Django REST Framework (API),
- PostgreSQL database,
- Bootstrap,
- Vanilla JS (API fetching),
- Chart.js (graphs display)


### Gallery
![1](https://raw.githubusercontent.com/WojciakW/Auctionation/master/readme_res/1.png)
![2](https://raw.githubusercontent.com/WojciakW/Auctionation/master/readme_res/2.png)
![3](https://raw.githubusercontent.com/WojciakW/Auctionation/master/readme_res/3.png)
![4](https://raw.githubusercontent.com/WojciakW/Auctionation/master/readme_res/4.png)
![5](https://raw.githubusercontent.com/WojciakW/Auctionation/master/readme_res/5.png)

#### Todos:
- Split back-end/front-end (FastAPI + front-end framework? switch SSR to SPA rendering?),
- Rewrite and opmtimize database handling engine (daemon? multithreading?),
