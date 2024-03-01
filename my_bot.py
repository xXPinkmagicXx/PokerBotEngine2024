from poker_game_runner.state import Observation
from poker_game_runner.utils import Range, HandType
import time
import random

class Bot:
  def get_name(self):
      return "Nicklas"

  def callIfMinRaiseElseFold(self, obs: Observation):
      
      if obs.get_call_size() == obs.get_min_raise():
        ##call 
        return 1
      ## fold
      return 0
  
  def canCall(self, obs: Observation, fractionOfStack):
    
    maxCallSize = fractionOfStack * obs.get_my_player_info().stack
    if maxCallSize > obs.get_call_size():
      return True
    
    return False
  
  def getMinLegalAction(self, obs: Observation):
      return min(obs.legal_actions)

  def veryGoodHand(self, currentHandType: HandType):
      ## if over two pairs
      if currentHandType > 3:
        return True
      
      return False
  def goodHand(self, currentHandType: HandType):
      if currentHandType > 1:
        return True
      return False
      
  def getMinRaise(self, obs: Observation, n=1):
      minRaise = obs.get_min_raise()
      if minRaise == 1:
        return 1
      return minRaise * n

  def act(self, obs: Observation):
    """
    0 = fold/check
    1 = check/call


    HANDTYPE
    STRAIGHTFLUSH = 9
    FOUROFAKIND = 8
    FULLHOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREEOFAKIND = 4
    TWOPAIR = 3
    PAIR = 2
    HIGHCARD = 1
    ERROR = 0


    """ 
    myBot = obs.get_my_player_info()
    myStack = myBot.stack

    legalActions = obs.legal_actions

    # Your code here
    currentHand = obs.get_my_hand_type()
    ## board_hand is excluding my cards
    current_board_hand = obs.get_board_hand_type()
    canRaise = obs.can_raise()
    # Get type of hand
    highString = "66+, A8s+, KTs+, QJs, AJo+, KQo"
    midString = "44+, A2s+, K5s+, Q8s+, J9s+, T9s, A7o+, K9o+, QTo+, JTo"
    lowString = "22+, A2s+, K6s+, Q8s+, J8s+, T8s+, 97s+, 86s+, 75s+, 65s, 54s, 43s, 32s, A8o+, A5o, KTo+, QTo+, JTo, T9o, 98o"

    isHigh = Range(highString).is_hand_in_range(obs.my_hand)
    isMid = Range(midString).is_hand_in_range(obs.my_hand)
    isLow = Range(lowString).is_hand_in_range(obs.my_hand)
    ## Preflop
    if obs.current_round == 0:
      
      ## Has good cards
      if isHigh:
        return obs.get_min_raise()
      ## if has mid cards
      if isMid:
        ## if to much
        if self.canCall(obs, 0.25):
          return 1
        else:
          return self.getMinLegalAction(obs)
        
      if isLow:
        if self.canCall(obs, 0.15):
          return 1
        
        return self.getMinLegalAction(obs)

      ## if out of range
      return self.getMinLegalAction(obs) 
    
    ## Flop
    if obs.current_round == 1:
      
      ## if very good hand
      if self.veryGoodHand(currentHand) and self.canCall(obs, 0.75):
          return self.getMinRaise(obs, 2)
      
      if self.goodHand(currentHand) and self.canCall(obs, 0.30):
        return obs.get_min_raise()
      
      return self.getMinLegalAction(obs)
    
    ## Turn
    if obs.current_round == 2:
      ## if very good hand
      if self.veryGoodHand(currentHand) and self.canCall(obs, 0.75):
          
          if isHigh:
            return self.getMinRaise(obs, 2)
          if isMid:
            return self.getMinRaise(obs, 1)
          
          return self.getMinRaise(obs)
      
      ## good hand
      if self.goodHand(currentHand) and self.canCall(obs, 0.30):
        
        if isHigh:
          return self.getMinRaise(obs, 3)
        if isMid:
           return self.getMinRaise(obs, 2)
        
        return self.getMinRaise(obs)
      
      ## fold or check
      return self.getMinLegalAction(obs)

    if obs.current_round == 3:
      ## if very good hand
      if self.veryGoodHand(currentHand) and self.canCall(obs, 0.75):
          
          if isHigh:
            return self.getMinRaise(obs, 4)
          if isMid:
            return self.getMinRaise(obs, 2)
          
          return self.getMinRaise(obs)
      
      ## good hand
      if self.goodHand(currentHand) and self.canCall(obs, 0.30):
        
        if isHigh:
          return self.getMinRaise(obs, 3)
        if isMid:
           return self.getMinRaise(obs, 1)
      
      ## fold or check
      return self.getMinLegalAction(obs)

    if obs.current_round == 4:
      ## if very good hand
      if (currentHand == HandType.STRAIGHTFLUSH):
         ## All IN
         return obs.get_max_raise()
      if currentHand == HandType.FLUSH:
        return self.getMinRaise(obs, 5)
       
      if self.veryGoodHand(currentHand) and self.canCall(obs, 0.8):
          
          if isHigh:
            return self.getMinRaise(obs, 4)
          if isMid:
            return self.getMinRaise(obs, 3)
          
          return self.getMinRaise(obs)
      
      ## good hand
      if self.goodHand(currentHand) and self.canCall(obs, 0.3):
        
        if isHigh:
          return self.getMinRaise(obs, 3)
        if isMid:
           return self.getMinRaise(obs, 2)
        
      ## fold or check
      return self.getMinLegalAction(obs)

    ## Fold if nothing
    return self.getMinLegalAction()
