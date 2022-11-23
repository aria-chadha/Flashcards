# Flashcards

Flashcards is a web application used for memory training. Users can create decks with cards that are presented one at a time and select how difficult or easy they found recalling that card. The system tracks your progress by keeping a score along with the last time you reviewed a deck.
It sends daily reminders to refresh your memory and a monthly progress report to keep you up to date. You may also export your data into a '.csv' file for your convenience.


## Installation
### Frontend
You should have a terminal or use command prompt, have Python and pip installed. To run the application:
1. Unzip file named "Frontend" to your desired directory.
2. Go to your terminal and change directory into the unzipped folder. 
3. This step is optional.
> i. You may install a virtual environment with the following command:


>```bash
> python3 -m venv .Flashcards-env
>```

> ii.  Then activate the environment:

>```bash
>source .Flashcards-env/bin/activate
>```

4. Install all requirements:

```bash
pip install -r requirements.txt
```
5. Install redis server:

```bash
bash install_redis.sh

```
6. Final step for frontend, run the flask app with the following command.

```bash
python3 api.py
```

7. For daily and monthly reminders, start celery beat with the following command.

```bash
celery -A scheduler.celery_app beat
```

8. Open another terminal tab, start celery worker with the following command.

```bash
celery -A scheduler.celery_app worker
```


### Backend
You should have a terminal or use command prompt, have Node.js, npm and Vue CLI installed. To run the application:

1. Unzip file named "Backend" to your desired directory.

2. Go to your terminal and change directory into the unzipped. Change directory further to a folder named "Frontend" 

3. Run the following command:

```bash
npm install
`````
4. Run the following command:

```bash
npm run dev
`````

## Usage

* Open your application in your browser at localhost address and go to the login page. 
* You will find a link to register and then login to your account. 
* Create as many decks as you wish and add cards as you go along. 
* Review them and follow your progress!
