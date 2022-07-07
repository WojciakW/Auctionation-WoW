# Auctionation

A Python-Django web app for World of Warcraft Classic live auction house statistics.

Author: Wojcech Wójciak (wojciech.wojciak22@gmail.com)

All data is provided by Blizzard's WoW Classic API.

### Key features:
- Automated 1 hour cycle-based database management, including:
  - fetching current auctions data from Blizzard API,
  - calculating statistics,
  - archiving data.
- Possibility to view every single item data on every realm, faction side, that is:
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
