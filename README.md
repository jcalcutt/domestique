<i><b> Requires: Python 3.7+ </b></i>

###### _Domestique - "A rider who works for the benefit of their team and leader"_

A tool to create summary stats for riders that are on the startlist for
a British Cycling race event.

Bike racing is tough. But knowing your opponents in your race can help.
For example, it's better to follow an attack from somebody who
consistently finishes in the top 10, compared to somebody who has raced
in 50+ races and yet to score a result ...in which case you'd probably
just be wasting energy.

On (most) BC event pages its possible to see the riders on the startlist
for a race. Whilst its possible to manually click through the startlist
to see who's any good (by navigating to the riders results page), it's
quite a laborious task.
The aim of this app is to create quick and easy summary stats for all
the riders on the online startlist, passing just the event URL and the
year you'd like to create the stats from (i.e. if it's early on in the
season, it may be more meaningful to examine last years stats for the
riders).


To Run:
```
$python run.py
```
Copy and Paste a BC Event URL:
```
Enter a race URL: <Copy & Paste Event URL here>
```
Choose which year to collect rider data from:
```
Year to collect rider stats from: <2018>
```
A CSV will be created in the 'data' directory, with the following stats
for each rider:
Number of Races, Total Points, (average) Points per Race, Number of Top
Ten Results, Number of Wins.

\- \- \- \-

:pencil: TO-DO:

- Tests
- Error handled for no startlist found
- Handle more than one startlist on the event page
- Previous season(s) stats
- Status bar

![image](img.png?raw=true)

_RLSCC RR 2018_, :camera:: Peter Davies