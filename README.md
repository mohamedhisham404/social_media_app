# Social Media App
The app is a fully functional social media app with multiple features built with fastAPI
![Screenshot from 2024-07-14 23-19-21](https://github.com/user-attachments/assets/32e86472-cd4c-45ad-831a-99dcddf223ae)

# Features
* the user can create an account and login with the email and password
* the user can view other users details
* the user can view all posts or specific post with post id 
* the user can create, update and delete its own posts
* the user can vote posts

# How to run it 
1- Download the code
```
git clone https://github.com/mohamedhisham404/social_media_app
```
2- Make an vertual environment
```
cd social_media_app
python3.8 -m venv fastapi
```
3- Mctivate it 
```
source fastapi/bin/activate 
```
4- Install the requirments
```
pip install -r requirements.txt 
```
5- Run the app
```
fastapi dev app/main.py --reload
```
6- put that url in the web browser
```
http://127.0.0.1:8000/docs#/
```