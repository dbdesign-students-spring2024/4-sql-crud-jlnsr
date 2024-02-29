# SQL CRUD
# Links 
[restaurants.csv](data/restaurants2.csv)  
[posts.csv](data/posts2.csv)  
[users.csv](data/users4.csv)
# Part 1: Restaurant Review
## Creating table for restaurants  
```
CREATE TABLE restaurants (id INTEGER PRIMARY KEY,restaurant_name TEXT, cuisine TEXT,neighborhood TEXT,hours TEXT,avg_rating INTEGER,good_for_kids INTEGER)
```
## Importing restaurant.csv into restaurants table
```
.import data/restaurants2.csv restaurants
```
### Q1: Find all cheap restaurants in a particular neighborhood (pick any neighborhood as an example).
```
SELECT * FROM restaurants WHERE price_tier="$" AND neighborhood="Midtown";
```
### Q2: Find all restaurants in a particular genre (pick any genre as an example) with 3 stars or more, ordered by the number of stars in descending order.
```
SELECT * FROM restaurants WHERE cuisine="Greek" AND avg_rating>=3 ORDER BY avg_rating DESC;
```
### Q3: Find all restaurants that are open now (see hint below).
```
SELECT * FROM restaurants2 WHERE opening < (strftime('%H:%M','now','localtime')) AND closing > (strftime('%H:%M','now','localtime'));
```
### Q4: Leave a review for a restaurant.

FIRST create a ‘reviews’ table;
```
CREATE TABLE reviews (id INTEGER PRIMARY KEY,restaurant_name TEXT,rating INTEGER,review TEXT);
```
NEXT leave a review
```
INSERT INTO reviews(id,restaurant_name,rating,review) VALUES (1,(SELECT restaurant_name FROM restaurants WHERE id=2),3,"Okay food, not worth the price.");
```
### Q5: Delete all restaurants that are not good for kids.
```
DELETE FROM restaurant WHERE good_for_kids=0;
```
### Q6: Find the number of restaurants in each NYC neighborhood.
```
SELECT neighborhood,count(neighborhood) FROM restaurantS GROUP BY neighborhood
```  

# Part 2: Social Media App
## Creating a USERS table;
```
CREATE TABLE users (id INTEGER PRIMARY KEY,username TEXT,email TEXT,password TEXT)
```
## Importing users.csv into users table;
```
.import data/users4.csv
```
## Creating a POSTS table;
```
CREATE TABLE posts (id INTEGER PRIMARY KEY, status TEXT, sent_by TEXT, sent_to TEXT, post_type TEXT, content TEXT, time_posted TEXT);
```
## Importing posts.csv into posts table;
```
.import data/posts2.csv posts
```
### Q1: Register a new User
```
INSERT INTO users (id,username,email,password) VALUES (1001,"jls9980","jls9980@nyu.edu","juliusCaesar");
```
### Q2: Create a new Message sent by a particular User to a particular User (pick any two Users for example).

```
INSERT INTO posts (id,status,sent_by,sent_to,post_type,content,time_posted) VALUES (1001,"visible","jls9980","ycraigheadpd","message","Hello ycraigheadpd, this is an example message","2024-02-28 09:30:00"); 
```
### Q3: Create a new Story by a particular User (pick any User for example).

```
INSERT INTO posts (id,status,sent_by,sent_to,post_type,content,time_posted) VALUES (1002,"Visible","ycraigheadpd","public","story","This is an example story","2024-02-28 09:30:34");
```
### Q4: Show the 10 most recent visible Messages and Stories, in order of recency.
```
SELECT * FROM posts ORDER BY time_posted DESC LIMIT 10; 
```
### Q5: Show the 10 most recent visible Messages sent by a particular User to a particular User (pick any two Users for example), in order of recency.
```
SELECT * FROM posts WHERE sent_by='bbinder68' AND sent_to='jfisbey68' AND status='visible' AND post_type='message' ORDER BY time_posted DESC LIMIT 10; 
```
### Q6: Make all Stories that are more than 24 hours old invisible.
FIRST update the ‘status’ field so that it reports the # of hours that have passed since the post was made;
```
UPDATE posts SET status=ROUND( (JULIANDAY('now','localtime') - JULIANDAY(time_posted))*24 );
```
THEN set the status to ‘invisible’ for stories that are more than 24 hours old;
```
UPDATE posts SET status='invisible' WHERE post_type='story' AND cast(status AS INT) >24;
```
### Q7: Show all invisible Messages and Stories, in order of recency.
```
SELECT * FROM posts WHERE status='invisible' ORDER BY time_posted DESC;
```
### Q8: Show the number of posts by each User.
```
SELECT username,count(sent_by) FROM users LEFT JOIN posts ON users.username=posts.sent_by GROUP BY sent_by;
```
### Q9: Show the post text and email address of all posts and the User who made them within the last 24 hours.
```
SELECT content,email,username FROM posts INNER JOIN users ON posts.sent_by=users.username WHERE (( ( JULIANDAY('now','localtime') - JULIANDAY(time_posted))*24)<=24); 
```
### Q10: Show the email addresses of all Users who have not posted anything yet.
FIRST create a table with just the emails from ‘users’ and the number of posts associated with said email;
```
CREATE TABLE posts_per_email (email INTEGER,num_posts INTEGER);
```
NEXT insert the emails and number of posts associated with that email from the ‘posts’ table;
```
INSERT INTO posts_per_email (email,num_posts) SELECT email,count(sent_by) FROM users LEFT JOIN posts ON posts.sent_by=users.username GROUP BY sent_by;
```
THEN select only the emails whose count is 0, i.e. no posts
```
SELECT * FROM posts_per_email WHERE num_posts==0;
```