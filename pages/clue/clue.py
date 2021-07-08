from flask import Blueprint, render_template, session, request
from utilities.db.db_manager import dbManager
import random
from datetime import datetime
from csv import writer
import math


# clue blueprint definition
clue = Blueprint('clue', __name__, static_folder='static', static_url_path='/clue', template_folder='templates')


##-------------------functions-----------------------------
##-------------------general functions-----------------------------
def get_relevant_clues():  # returns a table of all of the relevant clues for a specific func and sub-func

    function_name = session.get('function').strip()
    subFunction_name = session.get('subFunction').strip()

    relevantTopics = dbManager.fetch('SELECT TopicID FROM topics WHERE FunctionName=%s AND SubFunctionName=%s ORDER BY TopicID ASC',(function_name, subFunction_name))
    relevantClues = []

    for topic in relevantTopics:  # gets the table with all the relevant clues for the specific func and sub func
        tempClues = dbManager.fetch('SELECT * FROM clues WHERE TopicID=%s ORDER BY TopicID ASC, ClueID ASC', (topic[0],))
        relevantClues = relevantClues + tempClues

    return relevantClues


def update_clues_for_user(email, AnswerID, TopicID, ClueID):  # update the grade for each clue by answer
    clue_for_user = dbManager.fetch('SELECT * FROM clues_for_user WHERE Email=%s And TopicID=%s And ClueID=%s ORDER BY TopicID ASC, ClueID ASC ',
                                    (email, TopicID, ClueID))

    if len(clue_for_user) == 0:  # if the current clue is not in the table, insert it
        dbManager.commit('INSERT INTO clues_for_user VALUES (%s, %s, %s, %s, %s)', (email, TopicID, ClueID, True, 0))
        clue_for_user = dbManager.fetch('SELECT * FROM clues_for_user WHERE Email=%s And TopicID=%s And ClueID=%s ORDER BY TopicID ASC, ClueID ASC',
                                        (email, TopicID, ClueID))

    grade = int(clue_for_user[0][4])
    updated_grade = grade
    if AnswerID == 1: # the clue helped
        if grade == 0:
            updated_grade = grade
        else:
            updated_grade = grade - 1
    if AnswerID == 2: #the clue didnt help
        updated_grade = grade + 1

    dbManager.commit('UPDATE clues_for_user SET Grade=%s  WHERE Email=%s And TopicID=%s And ClueID=%s',
                     (updated_grade, email, TopicID, ClueID))


def next_SubStage(clues, current_clue_index):
    current_topic = clues[current_clue_index][0]
    next_clue_index = len(clues) + 1

    for i in range(current_clue_index, len(clues)):
        if clues[i][0] == current_topic + 1:
            next_clue_index = i
            break
        else:
            next_clue_index = current_clue_index + 1

    return next_clue_index


def listStages(): #makes a list of lists, each list contains the stage first and the subStages next
    stages_list = []
    sub_stages_list = []
    stages = dbManager.fetch('SELECT Stage, SubStage FROM topics GROUP BY Stage, SubStage ORDER BY TopicID ASC')
    first = stages[0][0]
    for i in range(0, len(stages)):
        stage = stages[i][0]
        sub_stage = stages[i][1]
        if first == stage:
            if sub_stages_list:
                sub_stages_list.append(sub_stage)
            else:
                sub_stages_list.append(stage)
        else:
            stages_list.append(list(sub_stages_list))
            sub_stages_list.clear()
            first = stage
            sub_stages_list.append(stage)
            if sub_stage:
                sub_stages_list.append(sub_stage)
    stages_list.append(list(sub_stages_list))
    return stages_list


def check_show_bubble(clue):
    clueID = dbManager.fetch('SELECT ClueID FROM clues  WHERE Content=%s ORDER BY TopicID ASC, ClueID ASC', (clue,))
    if clueID[0][0] == 1:
        return True
    return False


def reset_grades(email, resetAll):
    function_name = session.get('function').strip()
    subFunction_name = session.get('subFunction').strip()
    if resetAll is True:
        relevantTopics = dbManager.fetch('SELECT TopicID FROM topics WHERE FunctionName=%s AND SubFunctionName=%s ORDER BY TopicID ASC', (function_name, subFunction_name))
        for topic in relevantTopics:
            relevantClues = dbManager.fetch('SELECT ClueID From clues_for_user WHERE Email=%s And TopicID=%s ORDER BY TopicID ASC, ClueID ASC', (email, topic[0]))
            for clue in relevantClues:
                dbManager.commit('UPDATE clues_for_user SET Appear=%s, Grade=%s  WHERE Email=%s And TopicID=%s And ClueID=%s', (1, 0, email, topic[0], clue[0]))
    else:
        if 'current_sub_stage' in request.args:
            subStage = request.args['current_sub_stage']

            if subStage != '':
                relevantTopic = dbManager.fetch('SELECT TopicID FROM topics WHERE FunctionName=%s AND SubFunctionName=%s AND subStage=%s ORDER BY TopicID ASC', (function_name, subFunction_name, subStage))
                topic = relevantTopic[0][0]
                relevantClues = dbManager.fetch('SELECT ClueID From clues_for_user WHERE Email=%s And TopicID=%s ORDER BY TopicID ASC, ClueID ASC', (email, topic))
                for clue in relevantClues:
                    dbManager.commit('UPDATE clues_for_user SET Appear=%s, Grade=%s  WHERE Email=%s And TopicID=%s And ClueID=%s', (1, 0, email, topic, clue[0]))

            else:
                stage = request.args['current_stage']
                relevantTopic = dbManager.fetch('SELECT TopicID FROM topics WHERE FunctionName=%s AND SubFunctionName=%s AND stage=%s ORDER BY TopicID ASC', (function_name, subFunction_name, stage))
                for topic in relevantTopic:
                    relevantClues = dbManager.fetch('SELECT ClueID From clues_for_user WHERE Email=%s And TopicID=%s ORDER BY TopicID ASC, ClueID ASC', (email, topic[0]))
                    for clue in relevantClues:
                        dbManager.commit('UPDATE clues_for_user SET Appear=%s, Grade=%s  WHERE Email=%s And TopicID=%s And ClueID=%s', (1, 0, email, topic[0], clue[0]))


def update_csv(email, clicked_on): ## appends every activity the user does at a csv file
    with open('users_activity.csv', 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow([email, datetime.datetime.now(), clicked_on])


##-------------------ALGORITHMS FUNCTIONS-----------------------------
##these algorithms calculates the clues order and returns the table ordered.

def all_relevant_clues(relevantClues):
    ordered_clues = relevantClues
    session['random'] = False
    return ordered_clues


def random_order(relevantClues):
    session['random'] = True
    random.shuffle(relevantClues)
    ordered_clues = relevantClues
    return ordered_clues


def basic_algorithm(email, relevantClues):
    session['random'] = False
    ordered_clues = []

    for clue in relevantClues:
        topicID = clue[0]
        clueID = clue[1]
        clue_for_user = dbManager.fetch('SELECT * FROM clues_for_user WHERE Email=%s AND TopicID=%s AND ClueID=%s ORDER BY TopicID ASC, ClueID ASC',
                                        (email, topicID, clueID))

        if len(clue_for_user) != 0:
            grade = int(clue_for_user[0][4])

            if grade < 3:  # if grade is smaller than 3 then we add it to the ordered clues
                checkedClue = dbManager.fetch('SELECT * FROM clues WHERE TopicID=%s AND ClueID=%s ORDER BY TopicID ASC, ClueID ASC',
                                              (topicID, clueID))
                ordered_clues.append(checkedClue[0])
            else:
                dbManager.commit('UPDATE clues_for_user SET Appear=%s  WHERE Email=%s And TopicID=%s And ClueID=%s',
                                 (0, email, topicID, clueID))

        else:  # if the user never answered it before we add it to the ordered clues
            checkedClue = dbManager.fetch('SELECT * FROM clues WHERE TopicID=%s AND ClueID=%s ORDER BY TopicID ASC, ClueID ASC',
                                          (topicID, clueID))
            ordered_clues.append(checkedClue[0])
    return ordered_clues


def second_algorithm(email, relevantClues):
    # this algorithm updates the clues if the user solved 5 question of the same function type (every 5 finished questions there is an update).
    # the updates filters the first 25% of the clues that werent filtered out yet, ordered by highest grage, aka clicked 'didnt help' the most
    ordered_clues = []
    function_name = session.get('function')
    subFunction_name = session.get('subFunction')
    numOfFinished = len(dbManager.fetch('SELECT * FROM progress WHERE Email=%s AND FunctionName=%s AND SubFunctionName=%s AND Finished=%s',
                                        (email, function_name, subFunction_name, True)))
    if numOfFinished != 0 and numOfFinished % 5 == 0: #if the user finished 5 exercises of the same type of function, filer top 10%
        clues = dbManager.fetch('SELECT cfu.TopicID, cfu.ClueID FROM clues_for_user as cfu JOIN '
                                '(SELECT TopicID FROM topics where FunctionName=%s AND SubFunctionName=%s )'
                                ' as t ON cfu.TopicID = t.TopicID where Email=%s  and appear=%s  order by Grade Desc, cfu.TopicID, cfu.ClueID',
                (function_name.strip(), subFunction_name.strip(), email, 1))
        beforeCurrent = dbManager.fetch('SELECT Finished FROM progress WHERE Email=%s AND FunctionName=%s AND SubFunctionName=%s',
                                        (email, function_name, subFunction_name))

        if math.floor(len(clues)*0.25) == 0 and len(clues)*0.25 != 0: ## floored 25% brings 0 but there are clues, update just the first clue
            if beforeCurrent[-2][0]: ## makes sure it updates ONLY for the first time it gets to %5 by checking if the one before the current was 1
                dbManager.commit('UPDATE clues_for_user SET Appear=%s  WHERE Email=%s And TopicID=%s And ClueID=%s',
                                 (0, email, clues[0][0], clues[0][1]))
        else:
            if beforeCurrent[-2][0]: ## makes sure it updates ONLY for the first time it gets to %5 by checking if the one before the current was 1
                for i in range(math.floor(len(clues)*0.25)):
                    dbManager.commit('UPDATE clues_for_user SET Appear=%s  WHERE Email=%s And TopicID=%s And ClueID=%s',
                                (0, email, clues[i][0], clues[i][1]))

    for clue in relevantClues: ##makes the list that contains the returned clues (every clue with Appear==1)
        topicID = clue[0]
        clueID = clue[1]
        clue_for_user = dbManager.fetch('SELECT * FROM clues_for_user WHERE Email=%s AND TopicID=%s AND ClueID=%s ORDER BY TopicID ASC, ClueID ASC',
                                        (email, topicID, clueID))

        if len(clue_for_user) != 0: #if the user got this clue before we check the Appear state
            appear = int(clue_for_user[0][3])

            if appear == 1:
                checkedClue = dbManager.fetch('SELECT * FROM clues WHERE TopicID=%s AND ClueID=%s ORDER BY TopicID ASC, ClueID ASC',
                                              (topicID, clueID))
                ordered_clues.append(checkedClue[0])

        else:  # if the user never got this clue before we add it to the ordered clues
            checkedClue = dbManager.fetch('SELECT * FROM clues WHERE TopicID=%s AND ClueID=%s ORDER BY TopicID ASC, ClueID ASC',
                                          (topicID, clueID))
            ordered_clues.append(checkedClue[0])
    return ordered_clues


# Routes
@clue.route('/clue')
def index():

    stages_types = listStages()
    answers = dbManager.fetch('SELECT * FROM answers ORDER BY AnswerID ASC')
    email = session.get('user')["Email"]
    function_types = dbManager.fetch('SELECT FunctionName FROM topics GROUP BY FunctionName ORDER BY TopicID ASC')

    if 'func_type' in request.args:
        session['function'] = request.args['func_type']
        sub_function_types = dbManager.fetch('SELECT SubFunctionName FROM topics GROUP BY SubFunctionName ORDER BY TopicID ASC')
        # update_csv(email, 'function:' + request.args['func_type'])
        return render_template('clue.html', clue_id='chooseSubFunc', stages=stages_types, clue='האם הפונקציה מכילה שורש או מנה?', type_function=sub_function_types)

    if 'subFunc_type' in request.args:
        session['subFunction'] = request.args['subFunc_type']
        session['relevantClues'] = get_relevant_clues()
        time = datetime.now()
        session['starting_time'] = time.replace(microsecond=0)
        relevantClues = session.get('relevantClues')
        dbManager.commit('INSERT INTO progress VALUES (%s, %s, %s, %s, %s)', (email, session.get('starting_time'), session.get('function'), session.get('subFunction'), 0))

    # update_csv(email, 'subFunction:' + request.args['subFunc_type'])


    ##----------------------------CHOOSE AN ALGORITHM-----------------------------------------------------
    # --------clues_order - here we can choose different functions (algorithms) for different results-----
        session['clues_order'] = basic_algorithm(email, relevantClues)
        # session['clues_order'] = second_algorithm(email, relevantClues)
        # session['clues_order'] = random_order(relevantClues)
        # session['clues_order'] = all_relevant_clues(relevantClues)


        clues_order = session.get('clues_order')
        if len(clues_order):
            topic = dbManager.fetch('SELECT Stage, SubStage FROM topics WHERE TopicID=%s ORDER BY TopicID ASC', (clues_order[0][0],))
            return render_template('clue.html', clue_id='0', stages=stages_types, clue=clues_order[0][2], answers=answers, current_stage=topic[0][0] ,current_sub_stage=topic[0][1], clue_info=clues_order[0][3], clue_img=clues_order[0][4])
        else:
            return render_template('clue.html', done=True, stages=stages_types, clue='לפי הרשומות שלנו אתה כבר מכיר את כל הרמזים!', reset_grade_option=True)

    if 'answer' in request.args:
        # update_csv(email, 'answer:' + request.args['answer'])
        answer = int(request.args['answer'])
        clue_id = int(request.args['pre_clue_id'])  ## clue_id for the current clue that the user answered
        clues_order = session.get('clues_order')
        if clue_id == len(clues_order) - 1:
            update_clues_for_user(email, answer, clues_order[clue_id][0], clues_order[clue_id][1])  # relevant for every algorithm that use grades
            dbManager.commit('UPDATE progress SET Finished=%s  WHERE Email=%s And StartingTime=%s', (1, email, session.get('starting_time')))

            return render_template('clue.html', done=True, stages=stages_types, clue='סוף תרגיל', show_bubble=True)
        else:
            if answer == 3:
                new_clue_id = next_SubStage(clues_order, clue_id)
                topic = dbManager.fetch('SELECT Stage, SubStage FROM topics WHERE TopicID=%s ORDER BY TopicID ASC', (clues_order[new_clue_id][0],))
                return render_template('clue.html', clue_id=new_clue_id, stages=stages_types, clue=clues_order[new_clue_id][2], answers=answers, current_stage=topic[0][0], current_sub_stage=topic[0][1], show_bubble=check_show_bubble(clues_order[new_clue_id][2]), clue_info=clues_order[new_clue_id][3], clue_img=clues_order[new_clue_id][4])
            else:
                update_clues_for_user(email, answer, clues_order[clue_id][0], clues_order[clue_id][1])  # relevant for every algorithm that use grades
                topic = dbManager.fetch('SELECT Stage, SubStage FROM topics WHERE TopicID=%s ORDER BY TopicID ASC', (clues_order[clue_id + 1][0],))
                return render_template('clue.html', clue_id=clue_id + 1, stages=stages_types, clue=clues_order[clue_id + 1][2], answers=answers, current_stage=topic[0][0] ,current_sub_stage=topic[0][1], show_bubble=check_show_bubble(clues_order[clue_id + 1][2]),clue_info=clues_order[clue_id + 1][3], clue_img=clues_order[clue_id + 1][4])

    if 'stage' in request.args: ##the user used the side menu
        # update_csv(email, 'stage:' + request.args['stage'])
        clues_order = session.get('clues_order')
        session['stage'] = request.args['stage']
        # if 'subStage' in request.args: ##if the user chose a sub stage update csv
            # update_csv(email, 'subStage:' + request.args['subStage'])
        for i in range(0, len(clues_order)):
            clue = clues_order[i]
            if 'subStage' in request.args: ##if the user chose a sub stage
                sub_stage = request.args['subStage']
                session['sub_stage'] = sub_stage
                sub_stage_string = dbManager.fetch('SELECT SubStage FROM topics WHERE TopicID=%s ORDER BY TopicID ASC ', (clue[0],))
                if sub_stage_string[0][0] == sub_stage:
                    topic = dbManager.fetch('SELECT Stage, SubStage FROM topics WHERE TopicID=%s ORDER BY TopicID ASC', (clue[0],))
                    return render_template('clue.html', clue_id=i, stages=stages_types, clue=clue[2], answers=answers,  current_stage=topic[0][0] ,current_sub_stage=topic[0][1], show_bubble=check_show_bubble(clue[2]), clue_info=clue[3], clue_img=clue[4])

            else: ##if the user chose a stage,
                stage = request.args['stage']
                stage_string = dbManager.fetch('SELECT Stage FROM topics WHERE TopicID=%s ORDER BY TopicID ASC', (clue[0],))
                if stage_string[0][0] == stage:
                    topic = dbManager.fetch('SELECT Stage, SubStage FROM topics WHERE TopicID=%s ORDER BY TopicID ASC', (clue[0],))
                    return render_template('clue.html', clue_id=i, stages=stages_types, clue=clue[2], answers=answers,  current_stage=topic[0][0],current_sub_stage=topic[0][1], show_bubble=check_show_bubble(clue[2]), clue_info=clue[3], clue_img=clue[4])

        if 'subStage' in request.args: ##if there are not clues for this subStage
            return render_template('clue.html', stages=stages_types, clue='לפי הרשומות שלנו אתה כבר מכיר את כל הרמזים לסעיף זה', current_stage=request.args['subStage'], current_sub_stage=request.args['subStage'], reset_grade_option=True) ## if there are no relevant clues for this topic for this user
        else: ##if there ar enot clues for this stage
            return render_template('clue.html', stages=stages_types, clue='לפי הרשומות שלנו אתה כבר מכיר את כל הרמזים לסעיף זה', current_stage=request.args['stage'], reset_grade_option=True) ## if there are no relevant clues for this topic for this user

    if 'reset_grade' in request.args:
        # update_csv(email, 'reset_grade:' + request.args['reset_grade'])
        reset_grades(email, True)
        return render_template('clue.html', clue_id='chooseFunc', stages=stages_types, clue='מהו סוג הפונקציה?', type_function=function_types)

    if 'reset_topic_grade' in request.args:
        # update_csv(email, 'reset_topic_grade:' + request.args['reset_topic_grade'])
        reset_grades(email, False)
        return render_template('clue.html', clue_id='chooseFunc', stages=stages_types, clue='מהו סוג הפונקציה?', type_function=function_types)

    else: #if request.args in none, thats the starting point
        return render_template('clue.html', clue_id='chooseFunc', stages=stages_types, clue='מהו סוג הפונקציה?', type_function=function_types)
