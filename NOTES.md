# Development plan

- [X] Basic Player Definition
- [X] Basic Deck Definition
- [X] Figure out how to return JSON or html (`render_template`)
- [X] Basic testing
- [X] ruff
- [X] GitHub Actions for tests and linters
- [X] Basic List pages for entities
- [X] Swagger API
- [ ] Local development tool to clear/seed database
- [X] CRUD APIs for Games
- [ ] HTML Page to Create Game
  - Mostly done, just need to implement actual submission, (if desired) deck-creation in-page, and non-deck metadata (who won, turn count, etc.).
- [ ] Load Game-history from file
- [ ] Favicon
...
- [ ] Authentication (will need to link `user` table to `player`)
...
- [ ] Helm chart including an initContainer to create the database if it doesn't exist already
- [ ] GroupId (i.e. so I can host other people's data? That's _probably_ a YAGNI - see if there's demand!)


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

# Things to learn/fix/understand

* ~~How to use an existing Python class as the spec in a Swagger API definition? (See, for instance, `responses.200.content.application/json.schema.id` under `get_player`). Perhaps it's not possible just by name, which would be understandable (the context of a Docstring probably doesn't include the context of imported code) - but, in that case, at least I'd like to be able to specify `definitions`` in a way that is independent of a method.~~
* ~~How to specify the content-type that should be sent with a Swagger request without needing to use `requestBody` (and thus, implying that there _should_ be a body)?~~
  * Fixed by using FastApi instead of Flask
* How to abstract out the standard-definitions of `routers/*` and `sql/crud.py`?
