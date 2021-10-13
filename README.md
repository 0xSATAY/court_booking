# NTU Court Booking Script

Tired of camping NTU's court booking system at 12am every day just to be disappointed in your slow fingers? Say no more. This shit works. Satisfaction guaranteed.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dependencies](#dependencies)
3. [TODO](#todo)



## Getting Started

1. Download or clone the project with your terminal:
```
$ git clone https://github.com/wdwdwdwdwdwdwd/court_booking.git
$ cd court_booking
```
2. Change file permissions (Don't do this if you're on Windows unless if you're running this through WSL):
```
$ chmod +x court_booking.py
```

3. Create a .txt file with your NTU network account credentials and store it in the same folder as the script.
e.g.
```
<network username>;<network password>
```
You can even have multiple accounts by having one account on every line!!
e.g.
```
MrDeansLister;VerySecurePassword
leetcoder1337;cafebabe
```

4. Download [Chromedriver](https://chromedriver.chromium.org/downloads) for your [Chrome version](https://help.zenplanner.com/hc/en-us/articles/204253654-How-to-Find-Your-Internet-Browser-Version-Number-Google-Chrome) and place it in the same folder as the script.

5. Change the parameter on line 41 to your Chromedriver filename. For Windows: "./chromedriver.exe"; For *NIX: "./chromedriver"

6. Run the script (Make sure you have [Python 3](https://www.python.org/downloads/) installed!!).
On Windows:
```
$ python3 court_booking.py <creds.txt file that you created>
```
On *NIX:
```
$ ./court_booking.py <creds.txt file that you created>
```

## Dependencies

- [Chromedriver](https://chromedriver.chromium.org/downloads)
- [Python 3](https://www.python.org/downloads/)

## TODO
[ ]Clean up my code???
[ ]Make a GUI Electron app so that anyone (even your grandmother) can use it

If it doesn't work, go debug it yourself. Unless if you know me, then feel free to PM me.
