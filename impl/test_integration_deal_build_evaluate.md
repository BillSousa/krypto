Runs `deal()` with a seeded random source, calls `evaluate()` with a 
fixed token list that is known to calculate to the target, then asserts 
the result is correct. `evaluate()` calls `is_valid_token_chain()` and 
`build_expr_string()` internally, so this exercises all four modules 
together.
```
<<<pytest>>>
```