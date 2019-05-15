#!/usr/bin/env python

"""

Constraint Driven Random TimeTable Genearator

"""
__author__ ='jayarajanjn@gmail.com'
__version__ = '1.1'

import random
def get_empty_tt(days = 5, hours =7):
    # [day, hour, subject, type, faculty]
    return [[day,hour,-1,-1,-1] for day in range(days) for hour in range(hours) ]

constraints = []
subjects = list(range(8))
faculties = list(range(8))
subject_allocation = {0:7, 1:3, 2:3, 3:1, 4:4, 5:1, 6:2, 7:4}
LEC_TYPE = 1
LAB_TYPE = 2
subject_slots_per_week = {0:5, 1:4, 2:4, 3:4, 4:5, 5:2, 6:1, 7:1}
max_first_hours = 1
labs = list(range(2))
labslots = [[1,2,3], [4,5,6]] # counting starts from 0
lab_faculties = [[1,2,3], [5,6,7]]
lab_slots_per_week = {0:2, 1:1}
tt_slots = get_empty_tt()
no_of_hours_per_day = 7
no_of_days_per_week = 5

def rule(func):
    constraints.append(func)
    return func

def integrity_check(subject_slots_per_week,lab_slots_per_week, tt_slots):
    print(len(tt_slots), sum(subject_slots_per_week.values()), sum(lab_slots_per_week.values())*3)
    return len(tt_slots) >= sum(subject_slots_per_week.values()) + sum(lab_slots_per_week.values())*3


@rule
def no_all_first(candidate):
    #print candidate
    first_hour_faculties = [slot[-1] for slot in candidate[::no_of_hours_per_day]]
    print "first_hour_faculties"
    print first_hour_faculties
    for faculty in set(first_hour_faculties):
        if first_hour_faculties.count(faculty) > max_first_hours:
            return 0
    else:
        return 1

@rule
def no_two_labs_a_day(candidate):
    for i in range(0,len(candidate), no_of_hours_per_day):
        day = candidate[i:i+no_of_hours_per_day]
        labs_per_day =[1 for lab_slot in labslots if day[lab_slot[0]][3] == LAB_TYPE ]
        if len(labs_per_day)>1:
            return 0
    return 1

@rule
def no_consecutive(candidate):
    #print candidate
    faculties = [(slot[0],slot[4]) for slot in candidate]
    #print faculties
    for i in range(len(faculties)-1):
        if type(faculties[i][1]) is list:
            pass
        elif type(faculties[i+1][1]) is list and faculties[i][1] in faculties[i+1][1]:
            return 0
        elif faculties[i][1] == faculties[i+1][1]:
            return 0
    else:
        print_tt(faculties)
        return 1


def get_fitness(candidate, constraints):
    satisfied = sum(constraint(candidate) for constraint in constraints)
    score = satisfied/len(constraints)
    return score

def get_random_fill(tt_slots, subjects, subject_slots_per_week, labs, labslots, lab_slots_per_week):
    lab_slots_available = [(day,slot) for day in range(5) for slot in labslots]
    print lab_slots_available
    for lab in labs:
        for the_slot in range(lab_slots_per_week[lab]):
            picked_slot = random.randint(0, len(lab_slots_available)-1)
            print picked_slot
            day, slot = lab_slots_available[picked_slot]
            for hour in slot:
                tt_slots[day* no_of_hours_per_day +hour][2] = lab
                tt_slots[day* no_of_hours_per_day +hour][3] = LAB_TYPE
                tt_slots[day* no_of_hours_per_day +hour][4] = lab_faculties[lab]
            del lab_slots_available[picked_slot]
    sub_slots_available = [i for i, tt_slot in enumerate(tt_slots) if tt_slot[2] == -1]
    for subject in subjects:
        for the_slot in range(subject_slots_per_week[subject]):
            picked_slot = random.randint(0, len(sub_slots_available)-1)
            slot = sub_slots_available[picked_slot]
            tt_slots[slot][2] = subject
            tt_slots[slot][3] = LEC_TYPE
            tt_slots[slot][4] = subject_allocation[subject] # for now subject id and faculaty id are same... we will fix this later
            del sub_slots_available[picked_slot]
    #print tt_slots
    return tt_slots

def print_tt(candidate):
    for i in range(0,len(candidate),no_of_hours_per_day):
        print candidate[i:i+no_of_hours_per_day]

if __name__ == '__main__':
    if integrity_check(subject_slots_per_week, lab_slots_per_week, tt_slots):
        raw_input("press enter to continue...")

        while True:
            tt_slots = get_empty_tt(days = no_of_days_per_week, hours= no_of_hours_per_day)
            #raw_input("press enter to continue...")
            candidate = get_random_fill(tt_slots, subjects, subject_slots_per_week, labs, labslots, lab_slots_per_week)
            fitness = get_fitness(candidate, constraints)
            if fitness == 1.0:
                print("best")
                print_tt(candidate)
                break
            if fitness > 0.9:
                print(fitness, candidate)
