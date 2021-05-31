# Rock, Paper, Scissors, Lizard, Spock Game API
***

## _Introduction:_
This application provides various endpoints to play the Rock, Paper, Scissors, Lizard, Spock Game.


## _Running the app locally:_
The app is containerized using docker. To setup the app locally install [Docker](https://docs.docker.com/engine/install/)  and [Docker Compose](https://docs.docker.com/compose/install/). Once installed run the command: 
```sh
docker-compose up
```
This will have the app running locally on port 5069. And now the endpoints can be accessed to play the game.


## _Available Endpoints:_
### 1. Choices

Endpoint | Method | Description
----------| ---- | -----------
/choices | GET | This endpoint  gives a list of all available choices for playing the game

### Success Response
+  HTTP Status Code: 200 
+  Example Response:

        [
          {
            “id": 1,
            "name": "rock"
          },
          {
            “id": 2,
            "name": "paper"
          }
        ]


### 2. Choice
Endpoint | Method | Description
----------| ---- | -----------
/choice | GET | Get a randomly generated choice

### Success Response
+  HTTP Status Code: 200 
+  Example Response:

        {
            “id": 1,
            "name": "rock"
        }


### 3. Play
Endpoint | Method | Data Parameter | Description
----------| ---- | ----------- |---------------
/choice | POST | { “player”: choice_id } |Enter your choice ID to play a round against a computer opponent

### Success Response
+  HTTP Status Code: 200 
+  Example Response:

        {
          "results": win,
          “player”: 1,
          “computer”:  3
        }

### Error Response
Exception | HTTP status code | Description
----------| --------------- | ---------
BadRequest | 400 | When the post body of request is not a valid Json or not in accordance with input requirement 


### 4. Scoreboard
Endpoint | Method | Description
----------| ---- | -----------
/scoreboard | GET | Gives a result summary of your last 10 game plays

### Success Response
+  HTTP Status Code: 200 
+  Example Response:

        {
            “win": 1,
            "lose": "4",
            "tie": "5"
        }


### 5. Reset Scoreboard
Endpoint | Method | Description
----------| ---- | -----------
/reset-score | GET | Resets your previous scoreboard results

### Success Response
+  HTTP Status Code: 200 
+  Example Response:

        Scoreboard has been successfully reset!      
