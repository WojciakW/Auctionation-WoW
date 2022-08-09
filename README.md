# Auctionation-WoW

A Python-Django web app for World of Warcraft Classic live auction house statistics.

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
- PostgreSQL database,
- Bootstrap,
- Vanilla JS (API fetching),
- Chart.js (graphs display)


### Gallery
![1](https://github.com/WojciakW/Auctionation/tree/master/readme_res/1.png)
![2](https://github.com/WojciakW/Auctionation/tree/master/readme_res/2.png)
![3](https://github.com/WojciakW/Auctionation/tree/master/readme_res/3.png)
![4](https://github.com/WojciakW/Auctionation/tree/master/readme_res/4.png)
![5](https://github.com/WojciakW/Auctionation/tree/master/readme_res/5.png)