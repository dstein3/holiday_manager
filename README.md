# holiday_manager
This repo contains all necessary files for the holiday-management assignment.

Running the file is all that is necessary for the code to run.
A single instance of main() is called at the bottom of the file.
While there is an attempt to group similar functions together,
some organizational harmony was sacrificed so that functions
could run in the proper order, many functions relying on prior ones.

The first section contains the urls for the APIs.
Next I defined the holiday class.
Following this are several functions that are necessary for filtering and handling dates.
Following this are the functions build for scraping the holiday-API.
Following this is the HolidayList object-class and all of its self-referential functions.
Next are functions that query text for the menu descriptions.
Following this are several functions built specifically for handling the querying of weeks
in the visualization section of the interface.
Following this are the larger functions built for handling the flow of the "adding" and "subtracting" menus.

Lastly is the function for main(). It handles the navigation of the menus, queries the lists of holidays
and contains the code for saving the final Holiday List to a JSON file.
