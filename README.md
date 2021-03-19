# SportDiscuss
Users can register/log in, see all currently available games for sports betting, comment on the game, and like others comments. This creates a community in the sports betting area that is not available at this moment. Sports betting websites do not allow for commenting or discussion to see or give a point of view that others may not know or have considered.

## API information
All information is brought in from [The Odds API](https://the-odds-api.com/). Response is in JSON and parsed with axios and python-flask. 

## Database information
Database is in postgresql and created/updated with flask-sqlalchemy. 

## Tables in database
---
### Users
username (primary key)  
email  
password

### Games  
game_id (primary key)  
home_team  
away_team  

### Comments (users_games) 
comment_id (primary key)  
username (foreign key)  
game_id (foreign key) 

### Likes (users_comments)  
like_id (primary key)  
username (foreign key)  
comment_id (foreign key) 