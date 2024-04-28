# Uni-Flavor-Verse
## CRUD web application for browsing cooking recipes online!
### Description:
It’s your passport to culinary adventures! Whether you’re a seasoned chef or just starting out in the kitchen, FlavorVerse has something for everyone. Browse a wide variety of cooking recipes, save your favorites, and explore flavors from around the world.\
Application was made as an university project using ```Python``` with ```Flask``` for backend, ```PostgreSQL``` as a database and ```[Placeholder]``` for frontend.

### Installation / running the app
The application is based on simple ```docker-compose.yml``` file so it is necessary to have Docker installed on your machine.\
If You have Docker you only need to run the following command:
```console
docker-compose up
```
or if You are on a Linux machine:
```console
sudo docker-compose up
```
## Backend
### Available routes
#### Reading data (*GET*):
```html
/api/przepisy
/api/przepisy/<id>
/api/przepisy/skladniki/<id>
/api/uzytkownicy
/api/uzytkownicy/<id>
/api/skladniki
/api/skladniki/<id>
```
#### Creating new records (*POST*):
```html
/api/przepisy/<id>
/api/przepisy/skladniki/<id>
/api/uzytkownicy/<id>
/api/skladniki/<id>
```
When creating new record via *POST* method, the request needs to have ```Content-type: application/json``` header and the JSON data in the body. New record data have to be in dictionary format with ```"field_name": "value"```.
Only adding records via ```/api/przepisy/skladniki/<id>``` can use array/list of the new records.
#### Updating existing records (*PUT*):
```html
/api/przepisy<id>
/api/uzytkownicy/<id>
/api/skladniki/<id>
```
The data needs to be send in similar way as mentioned in previous section. When updating the record, the data dictionary can have only the changed values, e.g. when changing only *nazwa* field, the body's data should look like this:
```python
{ "nazwa": "nowa nazwa" } #other fields won't be changed
```
#### Deleting existing records (*DELETE*):
```html
/api/przepisy/<id>
/api/uzytkownicy/<id>
/api/skladniki/<id>
```
