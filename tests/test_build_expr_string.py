from typing import List, Union                                                                                                                        
                                                                                                                                                      
import pytest                                                                                                                                         
                                                                                                                                                      
from krypto.build_expr_string import build_expr_string                                                                                                
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
def test_empty_tokens():                                                                                                                              
                                                                                                                                                      
    tokens: List[Union[int, str]] = []                                                                                                                
                                                                                                                                                      
    hand: List[int] = [1, 2, 3, 4, 5]                                                                                                                 
                                                                                                                                                      
    assert build_expr_string(tokens, hand) == ""                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
def test_single_card():                                                                                                                               
                                                                                                                                                      
    tokens: List[Union[int, str]] = [0]                                                                                                               
                                                                                                                                                      
    hand: List[int] = [1, 2, 3, 4, 5]                                                                                                                 
                                                                                                                                                      
    assert build_expr_string(tokens, hand) == "1"                                                                                                     
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
def test_two_cards():                                                                                                                                 
                                                                                                                                                      
    tokens: List[Union[int, str]] = [0, "+", 1]                                                                                                       
                                                                                                                                                      
    hand: List[int] = [1, 2, 3, 4, 5]                                                                                                                 
                                                                                                                                                      
    assert build_expr_string(tokens, hand) == "1+2"                                                                                                   
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
def test_three_cards():                                                                                                                               
                                                                                                                                                      
    tokens: List[Union[int, str]] = [0, "+", 1, "*", 2]                                                                                               
                                                                                                                                                      
    hand: List[int] = [1, 2, 3, 4, 5]                                                                                                                 
                                                                                                                                                      
    assert build_expr_string(tokens, hand) == "1+2*3"                                                                                                 
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
def test_parentheses():                                                                                                                               
                                                                                                                                                      
    tokens: List[Union[int, str]] = [0, "+", "(", 1, "*", 2, ")"]                                                                                     
                                                                                                                                                      
    hand: List[int] = [1, 2, 3, 4, 5]                                                                                                                 
                                                                                                                                                      
    assert build_expr_string(tokens, hand) == "1+(2*3)"                                                                                               
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
def test_all_cards():                                                                                                                                 
                                                                                                                                                      
    tokens: List[Union[int, str]] = [0, "+", 1, "*", 2, "-", 3, "/", 4]                                                                               
                                                                                                                                                      
    hand: List[int] = [1, 2, 3, 4, 5]                                                                                                                 
                                                                                                                                                      
    assert build_expr_string(tokens, hand) == "1+2*3-4/5"                                                                                             
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
def test_negative_index():                                                                                                                            
                                                                                                                                                      
    tokens: List[Union[int, str]] = [-1, "+", 1]                                                                                                      
                                                                                                                                                      
    hand: List[int] = [1, 2, 3, 4, 5]                                                                                                                 
                                                                                                                                                      
    assert build_expr_string(tokens, hand) == "5+2"                                                                                                   
                                                                                                                                                      
                                                                                                                                                      
                                                                                                                                                      
def test_out_of_range_index():                                                                                                                        
                                                                                                                                                      
    tokens: List[Union[int, str]] = [5, "+", 1]                                                                                                       
                                                                                                                                                      
    hand: List[int] = [1, 2, 3, 4, 5]                                                                                                                 
                                                                                                                                                      
    with pytest.raises(IndexError):                                                                                                                   
                                                                                                                                                      
        build_expr_string(tokens, hand)



