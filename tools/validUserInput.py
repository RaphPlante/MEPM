#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def valid_user_input(sentence, type_, *args):
    """
    valid_user_input is the function used to ask the user a choice of answer related to
    the sentenced passed in the parameter sentence. The valid choices can be
    multiple or single and are contained in the vararagin cell. The function
    keeps asking the input if it is invalid.
    
    Inputs:
        sentence : the question asked to the user.
        type_ : validation type
                0 : choice of answers (strings)
                1 : positive numeric
        *args : the choices of valid answers.
        
    Outputs:
        userInput : the valid user input.
        
    Author: Jean-François Chauvette
    Date: 2019-01-19
    """
    userInput = input(sentence)
    
    if type_ == 0:
        while userInput not in args:
            userInput = input('Invalid choice\n' + sentence)
    elif type_ == 1:
        while not userInput.isdigit() or int(userInput) < 0:
            userInput = input('Input must be positive numeric\n' + sentence)
        userInput = int(userInput)
    
    return userInput
