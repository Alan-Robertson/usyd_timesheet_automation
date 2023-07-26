## Because Online Timesheet Submissions are a Pain ##

My employer requires that we manually track and transcribe data from our own records of time worked into their online system. We are not paid for the time spent doing this, but without doing it we're not paid at all. 

The system itself has several bugs/flaws/surprise features which makes this a painful event. 

As a result this selenium script exists. It's very hard coded and very bare bones but it gets the job done.

**Update 10/11/22**
Updated to work with "MyHr Ascend", give a shout if anything's broken.


## Usage ##

```bash
python timesheet_submitter.py <csv file> [job number]
```

The default job number is 1; this should only be a problem if you hold jobs in multiple faculties.

After running the script you'll be presented with the login page; do this yourself (so I don't have to touch your credentials) and press enter on the script once you've finished with this.

After that the script should fill everything out until you need to enter your timesheet submitter and lodge. The script will not press the lodge button for you just to be sure.

NOTE: Make sure you do not include any `+`, `,` or `/` characters in your script.


## CSV Format ##

The csv you provide should contain the following columns:

```
DATE, UNIT, HOURS, PAYCODE, [ANALYSIS CODE], [TOPIC], [DETAILS]

```

The script will not check if you have the correct topic; valid topics are probably only TUT and MRK anyway.

Don't forget to enter your timesheet provider!
