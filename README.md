# Browser History Pull/Update Script

Script to pull and update broswer histories.  This example pulls histories 
from Chromium and Firefox browsers.  The histories are pulled, then
the URLs are cleaned up and simplified.  Also a time interval between
each site visit is calculated based on the available timestamps
for site visits.  Finally, these formatted browser histories are 
written to CSV files.  Note that this task can be scheduled by setting up
a cron job from terminal:

```$crontab -e``` 
