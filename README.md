#Brain Dead Data Logger

BDL is a very simply Python/Flask/Skeleton web app designed to collect IoT
data an log them to files on the host Linux system.  Notes are for Ubuntu LTS 16. 

See notes in SimplyEmptyFlask for notes on how to clone and install this
app.  It's the same with exceptions below.

###Install Dependencies
```
pip install pygal
```

###Change config.py
* replace UPDATE_KEY with your key string
* replace PATH_TO_DATA with your data directory

###Update changes from repository
```
git pull origin master
sudo systemctl restart bdl.service
```

Yes, I know I could just use Adafruit.io or data.Sparkfun.com to post IoT data to a website.  And yes there are other cool websites that have way more functionality than this.  But, I don't own those sites and I can't add features, write server scripts to email me the data files or yada yada.

I've done some Rails development, and it...well...it's brittle.  And I wanted something even simpler.  Python seems to be the rage (at least for my kids who are learning Python in their school); Google uses Python (or did...I guess they now do whatever the AI tells them to do); I like Pandas, so hey Python.

Rails has lots of great stuff, so I did a quick survey of MVC -like frameworks for Python.  Flask seemed like a reasonable choice.  Read some docs, google, read some blogs, google...repeat.

Progress so far.  Ability to initialize a stream, log data to the stream, return the log as a csv file, an html page with the data displayed in a table, or an html page with the data displayed as a chart.

