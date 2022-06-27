# Operational Research Tests

Because of work, I had to do an optimization program for a distribution center.

This problem is related to combinatorial optimization. The initial brut-force method would take forever and a day to complete, even with modern computers. People are not going to wait for such time just to get an answer. This is NOT Fluid dynamics.

In this repository are listed a few of the tools I used, however none of them returned an optimal result.

## Using google's OR tools

## Using MIP tools

## Plot sort-of big data

I am used to have data that is 1~10MB in size, which is about 1E5 rows of plain text. However, with the outputs I had from my analysis, I accumulated 1E7 rows of plain text data, which is about 150MB in size. 

I initially loaded the data into Matplotlib, it could not cope with such file, the reason was, as somebody described in StackOverFlow. "The main problem in the code is that strings are read into X and Y arrays. Matplotlib tries to PLOT them as if they were names, not numbers. With 1E4 points the code is extremely slow in trying to cope with too many strings." He recommended to read the file 'by hand', i.e. use an specialized function to read, such as Pandas' read\_csv or Numpy's loadtxt, those functions automatically convert the fields while looping through the file.

## Running conditions

- Environment: Dell Vostro/Core i7/Windows 10

- Language: Python

- Editor: VS code 

