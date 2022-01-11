# Store-Sale

## Overview

This projects is about making an website that allows users to search through multiple stores. The website would let the user register and login to their own account. Once login to their account, the user would be able to query through multiple items and sections like appliance example. They are also able to see all the information about said product. 

---

## Wireframe
![Wireframe](./images/WF1.png) 
![Wireframe](./images/WF2.png)
![Wireframe](./images/WF3.png)


---

## ERD
![ERD](./images/erd.png)

---

## Component Tree
![Component Tree](./images/component_tree.png)

---

## MVP

:white_medium_small_square: Create routes that extracts data from another websites

:white_medium_small_square: Have a backEnd for a user and carts

:white_medium_small_square: optimize search query in frontend for multiple sites

:white_medium_small_square: Display all the products of the search query

:white_medium_small_square: checks if user is logged in then user can then add item to the cart

:white_medium_small_square: create a chart page to see which item has been checked out the most

---

## Routes 
| PATH | ROUTE | Description |
| --- | --- | --- |
| /user | POST | Signup/Create user |
| /user/login | POST | Login user |
| /user | GET | Verify user |
| /cart | Post | adds an Item to a user's cart |
| /cart | GET | gets all user's cart item |
| /cart/:id | DELETE | deletes 1 item from user's cart |
| /cart/checkout | GET | updates the checkout date forEach item |
| /newegg/:product | GET | gets product from another website |
| /steam | GET | gets product from another website |
| /newegg/:product | GET | gets product from another website |

---

## Core Goals 

:one:&nbsp; When I first visit the site, I'm on a home page that can search for various products.

:two:&nbsp; When not logged in, I see links to search, signup & login only. If I were to visit any of these routes manually while logged in, I would get redirected to the home page.

:three:&nbsp; I can create an account, log in, and log out.

:four:&nbsp; When logged in, I see links to home, logout, cart, and chart a user can also add items to cart and checkout. 

:five:&nbsp; The user can search for a specific product. Clicking on any product takes me to its details page.

:six:&nbsp; The cart will show a list of products the user added to cart



---

## Strech Goals

:one:&nbsp; create an admin page.

:two:&nbsp; add more sites to scrape from


