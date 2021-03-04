
# Portfolio API
  

## Setting up the Project

  

- create a virtual environment to isolate package dependencies

```

darshil@darshil-Inspiron-5555:~/Online Learning/smallcase$ python3 -m venv smallcase-env

darshil@darshil-Inspiron-5555:~/Online Learning/smallcase$ source smallcase-env/bin/activate

(smallcase-env) darshil@darshil-Inspiron-5555:~/Online Learning/smallcase$

```

- django project named `smallcase` is created and an app `api` is created as well. (This steps need not be performed again, as the project is already generated)

```

(smallcase-env) darshil@darshil-Inspiron-5555:~/Online Learning/smallcase$ django-admin startproject smallcase

(smallcase-env) darshil@darshil-Inspiron-5555:~/Online Learning/smallcase$ cd smallcase/

(smallcase-env) darshil@darshil-Inspiron-5555:~/Online Learning/smallcase$ django-admin startapp api

```

Project structure is as follows:

  

```

-smallcase
  -smallcase
    -api
    -smallcase
    -db.sqlite3
    -manage.py
    -README.md
    -requirements.txt

```

  

- Install the required packages from requirements.txt

  
  

```

(smallcase-env) darshil@darshil-Inspiron-5555:~/Online Learning/smallcase$ pip3 install -r requirements.txt

```

- Now we have setup our project.

  

## Creating Models

- Inside the models.py file, we have defined our models **Trade** and **Portfolio**

  

  

## Creating `serializers.py`

- now we create a serializers.py file inside our app api

- this will define a TradeSerializer and PortfolioSerializer


## Setting the views

  

- now inside the views.py file, the call to the routes `/trades`, `/portfolio` and `/returns` is handled

  

## Start the server

  

- start the django server

```

(smallcase-env) darshil@darshil-Inspiron-5555:~/Online Learning/smallcase/smallcase$ python3 manage.py runserver

Watching for file changes with StatReloader

Performing system checks...

  

System check identified no issues (0 silenced).

March 03, 2021 - 09:59:55

Django version 3.1.7, using settings 'smallcase.settings'

Starting development server at http://127.0.0.1:8000/

Quit the server with CONTROL-C.

  

```

- open the link in the browser `http://127.0.0.1:8000/`

- you can test the api in postman or in the browser itself

  

### GET /trades

Request : GET /trades

Response: 200 OK

```
[
    {
        "id": 15,
        "ticker": "TCS",
        "trade_type": "BUY",
        "quantity": 3,
        "price": 600.0
    },
    {
        "id": 16,
        "ticker": "TCS",
        "trade_type": "SELL",
        "quantity": 3,
        "price": 600.0
    },
    {
        "id": 17,
        "ticker": "WIPRO",
        "trade_type": "BUY",
        "quantity": 6,
        "price": 366.0
    },
    {
        "id": 18,
        "ticker": "WIPRO",
        "trade_type": "BUY",
        "quantity": 2,
        "price": 200.0
    },
    {
        "id": 19,
        "ticker": "WIPRO",
        "trade_type": "BUY",
        "quantity": 4,
        "price": 400.0
    },
    {
        "id": 20,
        "ticker": "WIPRO",
        "trade_type": "SELL",
        "quantity": 6,
        "price": 500.0
    },
    {
        "id": 21,
        "ticker": "WIPRO",
        "trade_type": "SELL",
        "quantity": 2,
        "price": 500.0
    }
]    

```

### GET /trades/<id>

Request : GET /trades/20

Response: 200 OK

```
{
    "id": 20,
    "ticker": "WIPRO",
    "trade_type": "SELL",
    "quantity": 6,
    "price": 500.0
}

```

### POST /trades

Request : POST /trades
Body: `{
    "ticker": "WIPRO",
    "trade_type": "BUY",
    "quantity": 2,
    "price": 100
}`
 

Response: 201 Created

```
{
    "id": 22,
    "ticker": "WIPRO",
    "trade_type": "BUY",
    "quantity": 2,
    "price": 100.0
}

```
### PUT /trades/<id>

Request : PUT /trades/22
Body: `{
    "ticker": "WIPRO",
    "trade_type": "BUY",
    "quantity": 2,
    "price": 200
}`

Response: 200 OK

```
{
    "id": 22,
    "ticker": "WIPRO",
    "trade_type": "BUY",
    "quantity": 2,
    "price": 200.0
}

```

### DELETE /trades/<id>

Request : DELETE /trades/22

Response: 200 OK


### GET /portfolio

Request : GET /portfolio

Response: 200 OK

```
[
    {
        "id": 12,
        "ticker": "TCS",
        "average_buy_price": 600.0,
        "quantity": 0
    },
    {
        "id": 13,
        "ticker": "WIPRO",
        "average_buy_price": 349.6666666666667,
        "quantity": 4
    }
]

```

### GET /returns

Request : GET /returns

Response: 200 OK

```
{
    "returns": -998.6666666666667
}

```
