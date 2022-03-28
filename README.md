Backend developer assignment:

Architectue:

3 sensors data is distributed to a single kafka topic, which is divided into 3 partitions.
Logic works such that every partition stores the data from each sensor exclusively.

Logic:

Generic function located at utility helper builds temporary results in output_file.txt according to each sensor 
aggregation function (file attached for 30 minutes of execution).
Results in this file are composed from 3 sensors according to the output of it's aggregation function per each seperate minute.

Additional function in utility helper process the results from output_file.txt to final results file, which is attached by name
results_file.txt.
This file contains results as requsted format of the exercise, for 30 minutes of execution.
