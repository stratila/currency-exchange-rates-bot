**About**

This is the Flask web-application that runs Telegram bot that shows currency exchange rates.

Features:

1. Shows the list of exchange rates
2. Converts currencies
3. Sends currency exchange rates statistic as a graph chart

**How to deploy on Heroku**

1. Clone this repo to local machine
2. Create a virtual environment

    `$ python3 -m venv venv`
    
3. Active a virtual environment
 
      `$ source venv/bin/activate`
 
4. Install requirements

    `$ pip install -r requirements.txt`
    
    If you'll have problems with psycopg2 try this:
    
    1. Install Postgres to your machine
    
    2. `$ export LDFLAGS="-L/usr/local/opt/openssl/lib"`
    
       `$ export CPPFLAGS="-L/usr/local/opt/openssl/include"`

5. Create a Heroku App
    
    1. `$ heroku login`
    
6. Go to the root directory of the app and create heroku app
    
    ```
    $ heroku apps:create ce-bot-stratila
    Creating ⬢ ce-bot-stratila... done
    https://ce-bot-stratila.herokuapp.com/ | https://git.heroku.com/ce-bot-stratila.git
    ```

7. Check the remote repo

    ```
    $ git remote -v
    heroku  https://git.heroku.com/ce-bot-stratila.git (fetch)
    heroku  https://git.heroku.com/ce-bot-stratila.git (push)
    ```

8. Create a database for the app

    ```
    $ heroku addons:add heroku-postgresql:hobby-dev
    Creating heroku-postgresql:hobby-dev on ⬢ ce-bot-stratila... free
    Database has been created and is available
    ! This database is empty. If upgrading, you can transfer
    ! data from another database with pg:copy
    Created postgresql-curly-94018 as DATABASE_URL
   ```

9. Get your database URL
    ```
    % heroku config:get DATABASE_URL   
    postgres://pjanyx...73ba93689856bcc7de5e9b84d9a8ea55a6@ec2-.....2.compute-1.amazonaws.com:5432/dfa6.....bg

   ```

10. In config.py assign it to DATABASE_URL in Config

11. Remove `migrations` direcory

12. Create a database schema (a new `migrations` dicrectory will be created)

    `flask db init`
    
    `flask db migrate -m "tg_user"`
    
13. In `config.py` assign `os.environ.get('DATABASE_URL')` back to `DATABASE_URL` in `Config` 
in order to read this variable from Heroku envinronment

14. Add environment variables names

    `$ heroku config:set FLASK_APP=bot.py`
    
    `$ heroku config:set SECRET_KEY='put-here-your-secret-key'`
    
    `$ heroku config:set BOT_TOKEN='put-here-your-bot-token'`
    
    `$ heroku config:set APP_URL=https://ce-bot-stratila.herokuapp.com/`
    
15. `$ git commit -m "heroku deploy"`

16. `$ git push heroku master`
    
    



