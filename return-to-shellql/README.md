# ret to shellql

## "web"

### La Forge built a new web application platform for our ShellQL product. Can you get the flag out?  The flag is the file `/flag`. Although the flag is not in the database this time; using shellQL to query the database might be helpful.

#### we patched the [pymysql](pymysql) library to solve this challenge
#### we wrote a pretty sweet little [database client](win.py). Maybe use it in shellql in dc-quals-20?
#### the table dump with the flag is [here](data/INFORMATION_SCHEMA.PROCESSLIST)

This challenge was a [revisited challenge](https://ctftime.org/task/6100) from the 2018 defcon quals. This challenge was (at the time) a fresh take on the traditional "web" category. The vulnerability was in a custom PHP extension instead of traditional web application logic. The major difference this year was the the flag was stored as a file `/flag` instead of being located in the databse. This writeup assumes you have read writeups from the previous challenge as the solution builds from it.

The very first thing we did was obtain a copy of last year's `shellme.so` and compare it to the `shellme.so` from this year to see what, if any, changes were made. Using the [ghidra](https://ghidra-sre.org/) decompiler, we compared the two [decompilations](givens/decomp/). After a _very_ quick look, the only interesting info from [our results](givens/decomp/shellme.diff) were the introduction of seccomp rules.

Knowing that the sql access was more or less identical to last year, we borrowed someone's solution from last year as a starting point for this year.

After getting an existing payload up and running to reliably execute sql queries, we tried the obvious thing tried to `LOAD_FILE('/flag)`. This seemingly should have worked, but didn't for some reason that only became clear after CTF ended. 

Because we weren't able to simply load the file, we began dumping the database to see if we could derive some more clues about what to do next. This database (in addition to all of the mysql overhead stuff), contained data about someone's personal poker games. This data included notes about other players, detailed information about locations of games he had attended including SSIDs and BSIDs of visible networks, latitude and longitude data, etc. We looked over all of this data for a very long time to see if we could find anything interesting.

At this point we kind of believed that there was some other service running on the domain that we could access. But, the database didn't give us any leads on where to look. We tried looking on web archive sites, google, and other places that might contain additional route information about the domain but didn't find anything useful. 

A team did manage to solve this challenge in about an hour, so we thought that we were missing something quite simple. At this point, we starting dumping more of the stack memory to see if we could derive some more useful information about the system, or see if maybe we were exploiting the wrong service (mysql). No and no.

About this time, we gave the [given php source](givens/index.php) another read and noticed something interesting. We found the following things a bit strange:

- a hex encoding of our input was stored in a variable and placed in a string
- this string was written to a log file with an appended `EOF` (why tho?)
- the return value of that `file_put_contente()` call was assigned to a variable (`$myfile`). (the return value is an _integer_ of the number of bytes written, not a file or php resource)
- that same long string was "written" to `$myfile`, without an appended `EOF`. (but `$myfile` is an integer and not a file handle? wtf?)
- then `$myfile` was closed.

Ok. this is where we spent a *TON* of time. We tried to examine the internal working of PHP to see if there was any possible way to use an integer to write to a file instead of the expected resource type. We were thinking that maybe this is where we were supposed to look. Maybe we could write to arbitrary memory addesses or something instead? But we then realized we would have to send enormous amounts of POST data to get our integer values high enough for that to even be viable. Maybe it is? But we didn't find anything indicating this was possible -- we also kept reminding ourselves that a team solved this in about an hour. Hmm.

We did another look at the database data and started looking a bit at the [INFORMATION_SCHEMA.PROCESSLIST](https://dev.mysql.com/doc/refman/8.0/en/processlist-table.html) table. It was fun seeing other people's queries, but we thought that surely the organizers knew about this, and the flag wouldn't make an appearnce there. 

At this point its also worth noting that the server would, at times, return extra data. These were seemingly random bytes, or potentially messed up stack data since it seemed like these servers were getting hammered by people. We didn't think too much of this, although we did notice that the byte patterns did seem to contain the same data over and over again. Like I said, we weren't too worried about this (keep in mind that all of our interactions with the database were coming through an exploited PHP plugin via shellcode that was writing raw mysql packets to a file descriptor and dumping raw mysql packet responses back to us with extra stack data). The organizers annouced that they were increasing the number of instances that this challenge was on. As that happened, the seeming random extra data seemed to be much better. This also really helped up dump really clean data from the database.

After another look at the data and some more poking, we decided to move on. Whatever was happening was solvable in less than an hour and we were just stumped. Either that or the first team dropped an Apache or PHP zero day. That wouldn't be super weird as 3 zero days were [dropped at quals last year](https://twitter.com/oooverflow/status/995833817679065088). Or maybe they were super lucky and stumbled across an unintended solution. 

The following day, we saw a Tweet (a little late) that they went ahead and reduced the number of instances. We thought this was an interesting move. We also saw that there are ~20 solves suddenly. Hmm. Time to revisit.

We tried some of our old tricks again.. `LOAD_FILE`, some other clever mysql-fu, poked around the website some more, looked at the data again (that we stupidly didn't keep from the frist time). As the data was dumping, we noticed some interesting traffic in the `PROCESSLIST` table... it looked like someone was spamming fake flags or giving hints in there. We thought, what the hell, let's submit a few of them just to see. And *IT WORKED*. Mind blown. We were a little confused to be honest. But it turns out, [WE WEREN'T THE ONLY ONES](https://twitter.com/oooverflow/status/1127741551138852864).

Despite this not being within the framer's intent, it is now the official intended solution. Sweet I guess.
