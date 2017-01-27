#Empty Simple Flask Project with Notes.

These are my notes on how to get a new project rolling.

###server set up
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

###initial set up
```
virtualenv myprojectenv
source myprojectenv/bin/activate
pip install gunicorn flask
```

###create a fork and clone the github repository
on github, create a fork for the new project (based on this one, duh) 
then clone that new project into a new directory

In the new project, goto clone with HTTPS section and copy the url 
```
git clone <url>
```

###run simpleapp.py with flask
```
cd fwww
export FLASK_APP=simpleapp.py
export FLASK_DEBUG=1
flask run
```

###run simpleapp.py with gunicorn
```
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

###install simpleapp as service
```
sudo cp /<path to>/simpleapp/server/simpleapp.service /etc/systemd/system/
sudo systemctl start simpleapp
sudo systemctl enable simpleapp
sudo systemctl status simpleapp
```

###Configure NGinx
```
sudo cp /<path to>/simpleapp/server/simpleapp.nginx /etc/nginx/sites-available/simpleapp
sudo ln -s /etc/nginx/sites-available/simpleapp /etc/nginx/sites-enabled
sudo systemctl restart nginx
sudo ufw allow 'Nginx Full'
```
