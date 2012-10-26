Thumbtack Programming Challenge - Problem 2: Simple Database
============================================================

Details: http://www.thumbtack.com/challenges

roblem 2: Simple Database

Your task is create a very simple in-memory database, which has a very
limited command set. All of the commands are going to be fed to you
one line at a time via stdin, and your job is the process the commands
and perform whatever operation the command dictates. Here are the basic
commands you need to handle:

 * SET [name] [value]: Set a variable [name] to the value [value].
   Neither variable names or values will ever contain spaces.
 * GET [name]: Print out the value stored under the variable [name].
   Print NULL if that variable name hasn't been set.
 * UNSET [name]: Unset the variable [name]
 * NUMEQUALTO [value]: Return the number of variables equal to [value].
   If no values are equal, this should output 0.
 * END: Exit the program

