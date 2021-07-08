# REMEZ 
## A Clue-Based Learning Support System

This project is a web application that provides help for solving math problems with clues.
the app does not need to be familiar with each question the user is trying to solve, rather give directions, tips and advises on how to solve the problem, step by step.
the app also filters the clues in order to display the most relevant clues for the user. 

As an admin you can change the algorithm responsible for filtering the clues, and either use one of the existing algorithms that the app provides, or write your own algorithm and integrate it to the app by following the instructions below.

For any additional questions and help you can reach us via e-mail at: hagitbu@post.bgu.ac.il or izhakig@post.bgu.ac.il.

## Getting Started

Steps:
1. download the project to your local host 
2. install Prerequisites
3. optional: change the algorithm by following the instructions below.  

### Prerequisites

What needs to be installed:
1. PyCharm
2. Python
3. Anaconda
4. MySQL

In addition, open the project's dir in the terminal and run the following commands:
1. pip install virtualenv
2. virtualenv venv
3. pip install python-dotenv

#### Run:
Run the project with your IDE's configuration, or from the terminal by using the **flask run** command


## Changing the Algorithm

The algorithm is responsible for filtering the clues so that the app will display the most relevant clues to the user. 
you can either change the existing algorithm to another one that the app provides, or write your own. 

### Replacing the existing Algorithm
In order to replace the algorithm with another existing algorithm you should follow the following steps:
1. open clue.py located at 'pages/clue/clue.py' 
2. look for the 'CHOOSE AN ALGORITHM' section starting at line 240
3. comment the existing uncommented algorithm 
4. uncomment the chosen algorithm
5. run the app

### Writing a new Algorithm

In order to write a new algorithm you should follow the following steps:
1. open clue.py located at 'pages/clue/clue.py'
2. look for the 'ALGORITHMS FUNCTIONS' section starting at line 131
3. add a new function. this function will contain your algorithm.
4. the function input should be: **email**- the current user email address, and **relevantClues** - a list of all the clues that are relevant for the type of function the user chose. 
5. the function output should be a list of the clues after the algorithm performed. meaning the output will be a list of the clues that were not filtered out by the algorithm, ordered in the same order you want to display the clues to the user. 
6. when the function is finished, use the instructions shown at **replacing the algorithm** above, but instead of step 4, add a new line : session['clues_order'] = *your function's name*(email, relevantClues)

If your algorithm requires using data from the database you can use the following:
* for select: dbManager.fetch('query', args=())
* for update, insert or delete: dbManager.commit('query', args=())

For example:
```
dbManager.fetc('SELECT * FROM clues WHERE TopicID=%s AND ClueID=%s ORDER BY TopicID, ClueID', (topicID, clueID))

dbManager.commit('UPDATE clues_for_user SET Grade=%s  WHERE Email=%s And TopicID=%s And ClueID=%s', (updated_grade, email, TopicID, ClueID))
```


## Built With

Flask skeleton project by Barak Pinchovski:  
[https://github.com/barakpinchovski/flask-skeleton-project](https://github.com/barakpinchovski/flask-skeleton-project)


## Authors

* Hagit Buda 
* Gal - Margalit Izhaki


