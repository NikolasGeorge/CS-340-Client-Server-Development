# CS 340 Client/Server Development

This repository holds my Project Two work from CS 340 at Southern New Hampshire University: a dashboard for Grazioso Salvare, a company that identifies shelter dogs suitable for search and rescue training. The dashboard reads the Austin Animal Center outcomes data from MongoDB and filters it by rescue type, with an interactive data table, a breed chart, and a map of the selected animal.

## Files

| File | Contents |
|---|---|
| `ProjectTwoDashboard.ipynb` | The Dash dashboard: rescue type filters, data table, pie chart, and geolocation map |
| `CRUD_Python_Module.py` | The `AnimalShelter` class, which provides create, read, update, and delete access to MongoDB |
| `CS340_Project_Two_README_Nikolas_George.docx` | Full project documentation, with screenshots of every filter state and instructions for reproducing the project |
| `Grazioso Salvare Logo.png` | Client logo displayed on the dashboard |

## Reflection

### How do you write programs that are maintainable, readable, and adaptable?

The CRUD Python module is the clearest example from this course. I wrote it as one class with four methods, and every method takes and returns plain Python types: a dictionary goes in, and a dictionary, a list, a count, or True or False comes back. Each method also checks its arguments and catches database errors, so a bad call returns an empty list or 0 instead of crashing whatever called it. The connection details are arguments with defaults rather than values written into the code, so the same class can point at a different database or collection without being edited.

The advantage showed up when I built the dashboard. The dashboard never connects to MongoDB itself. It imports the module, creates one `AnimalShelter` object, and passes each rescue filter to `read` as a dictionary. When the filters needed changing, only the queries changed, and the module did not change at all. I had already tested create, read, update, and delete in a separate notebook, so when something went wrong in the dashboard I knew the problem was in the dashboard code and not in the database layer. The same module could sit under a different front end, such as a command line tool or a scheduled report that emails Grazioso Salvare the newest candidate dogs each week, or it could be pointed at another shelter's data with a different collection name.

### How do you approach a problem as a computer scientist?

I start by turning the client's requirements into things I can test. Grazioso Salvare described what they wanted in terms of rescue types, and the Dashboard Specifications Document translated each rescue type into breeds, a sex, and an age range. My job was to turn that into exact MongoDB queries and then check them against the real data instead of trusting that they matched the description. That check mattered. The specification lists Doberman Pinscher as a disaster rescue breed, but the Austin data stores it as "Doberman Pinsch", so a query written straight from the specification would have silently returned fewer dogs than it should. I only caught it because I looked at what the query returned.

This project was different from earlier courses because it was built in layers that each depended on the one before. The database and its user account came first, then the module that reads it, then a test notebook, then the dashboard. Each layer had to work before the next one could be tested, so I tested each one as I finished it instead of all at the end. For future client database requests I would follow the same order: get the real data first and look at it, write and test the queries against it before building anything on top, keep the database access in its own module, and keep checking the results against what the client actually asked for.

### What do computer scientists do, and why does it matter?

Computer scientists take a problem that people are solving slowly or by hand and build something that solves it reliably. Without a tool like this, finding a candidate rescue dog means someone at Grazioso Salvare reading through thousands of shelter records and checking each dog's breed, sex, and age by eye, which is slow and easy to get wrong. The dashboard does that in one click, and anyone on their staff can use it without knowing anything about databases. The map shows which shelter a dog is near, and the chart shows which breeds are available at a glance.

That matters because their real work is training dogs, not sorting data. Every hour the software saves is an hour spent with the dogs, and every dog the filter catches that a person might have missed is another potential rescue dog. The difference between a correct query and an almost correct one, like the Doberman Pinscher spelling, is a dog that either gets found or does not.

## Author

Nikolas George, Southern New Hampshire University
