Empty Simple Flask Project with Notes.

These are my notes on how to get a new project rolling.

#server set up
```
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx
sudo pip3 install virtualenv
sudo ufw allow 5000
```
remember to close down port 5000 when done debugging
```
sudo ufw delete allow 5000
```

#initial set up
```
virtualenv myprojectenv
source myprojectenv/bin/activate
pip install gunicorn flask
```

#clone git


#run app.py with flask
```
cd fwww
export FLASK_APP=app.py
flask run
```
