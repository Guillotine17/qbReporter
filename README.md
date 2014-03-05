#ABOUT: 
qbReporter takes input from the qb reports and organizes it by user and client. tyReportReader takes the data from qbReporter and compares it to the tayrex data to output data useful for caller QA. now takes multiple qbClients listed after the tyFile, reversed from the original config input.

####3.5.14
today is the day when i fix the time calculations before opportunities, I may have figured out the solution to the tayrex file merging issue, if I had a list of all possible opportunities etc, i could just cycle through them and look for hits while adding things up. merging times will be a bit more of an issue. the issue of the math behind merging the %s is irrelevant since they will be recalculated anyway using the correct time entries from quickbooks.

####3.4.14
still need to change EXISTING time calculations to use qb time
- other time calculations were still using tyTime. changed to QBtime
- changed tyConfig to accept multiple client names, this solves the issue where
	there were multiple qbclients being used by the callers for only one tyClient.
- Need to implement multiple tyClients per single qbClients in addition to vice versa.

####3.3.14
accounted for tayrex csvs, 
NEED TO CHANGE (EXISTING) TIME CALCULATIONS TO USE QBTIME

####2.19.14
everything is working nicely, insert conversion rate is up and running, though i have doubts
about how that will interact with inserting the time calculations. probably just have to do that before I insert the conversion rate etc. gross nested if statements incoming.	
####2.18.14
about to do some serious edits. tyreporter is working for the most part. to do list for the evening includes:

1. merge qbreporter and tyreporter
2. implement get qbTime
3. implement conversion calculations for each opportunity
4. set up for multiple files being run.

good luck amirite?

and honestly qbReporter really needs to be converted to use dictionaries, its going to be slow as hell. what do...


####2.3.14
need to add things to implement tayrex data. also use python dictionaries instead of lists. may implement today.