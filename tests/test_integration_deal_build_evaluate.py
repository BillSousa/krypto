"""Integration test: deal() through build_expr_string() and evaluate()."""                                                                                   
                                                                                                                                                             
import random                                                                                                                                                
from fractions import Fraction                                                                                                                               
                                                                                                                                                             
from krypto.build_expr_string import build_expr_string                                                                                                       
from krypto.deal import deal                                                                                                                                 
from krypto.evaluate import evaluate                                                                                                                         
from krypto.is_valid_token_chain import is_valid_token_chain                                                                                                 
                                                                                                                                                             
                                                                                                                                                             
def test_seeded_deal_is_reproducible() -> None:                                                                                                              
    """The same seed yields the same target and hand."""                                                                                                     
    first = deal(rng=random.Random(42))                                                                                                                      
    second = deal(rng=random.Random(42))                                                                                                                     
    assert first == second                                                                                                                                   
                                                                                                                                                             
                                                                                                                                                             
def test_sum_of_seeded_hand_evaluates_to_target() -> None:                                                                                                   
    """A known-correct sum of the dealt hand is accepted as a win."""                                                                                        
    _, hand = deal(rng=random.Random(42))                                                                                                                    
    tokens: list[int | str] = [0, "+", 1, "+", 2, "+", 3, "+", 4]                                                                                            
    total = sum(hand)                                                                                                                                        
    assert is_valid_token_chain(tokens)                                                                                                                      
    assert build_expr_string(tokens, hand).count("+") == 4                                                                                                   
    assert evaluate(tokens, hand, total) == (True, True, Fraction(total))                                                                                    
                                                                                                                                                             
                                                                                                                                                             
def test_wrong_target_evaluates_as_valid_but_not_win() -> None:                                                                                              
    """A well-formed expression with the wrong target is not a win."""                                                                                       
    _, hand = deal(rng=random.Random(7))                                                                                                                     
    tokens: list[int | str] = [0, "*", 1]                                                                                                                    
    wrong = hand[0] * hand[1] + 1                                                                                                                            
    is_valid, is_win, _ = evaluate(tokens, hand, wrong)                                                                                                      
    assert is_valid is True                                                                                                                                  
    assert is_win is False




