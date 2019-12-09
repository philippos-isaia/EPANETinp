# EPANETinp
Reads EPANET input (inp) file and saves all the data to a PostgreSQL database.

Generate a new EPANET input (inp) file using the data recorded from the original EPANET file plus any changes in the database.


**readinputfile** function reads a file and return its contents in a list

**addinfotolists** allocates the inputted list into a structured dictionary

**addDataToDatabase** adds the contents of the structured dictionary into the database (PostgreSQL)

**newinputfilecreation** generates a new EPANET input file using the structured dictionary

