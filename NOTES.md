# Development plan

- [X] Basic Game Definition
- [X] Basic Player Definition
- [ ] Basic Deck Definition
- [ ] Basic testing
- [ ] Swagger API
- [ ] Local development tool to clear/seed database
...
- [ ] Authentication (will need to link `user` table to `player`)
...
- [ ] Helm chart including an initContainer to create the database if it doesn't exist already


# Tables

Tables:
* Decks
  * Name
  * Description
  * Owner
  * DecklistId (optional)
* Players (not the same as Users! Can model a Player who is not a User)
* Users
  * Standard auth stuff
* Games
  * Date
  * Location
  * DeckIds (array)
  * WinningDeckId
  * FinalTurnNum
  * Notes

# Database Migrations

https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#create-the-tables

# Authentication

https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login