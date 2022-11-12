# Chall7
- A NodeJS packed binary, analyze the strings to know that it is packed with NEXE and nodejs v14.15.3
- Use `nexe-unpacker` to get the JS source code, which uses a lot of expressions to check the flag
- NodeJS source code cannot be run because the `BigInt` check and the `Math.random()` functions seem to be modified
- Use `nexe` to repack the JS code ourselves, then `BinDiff` it with the original to see the modified code
- `Math.random()` is modified in `v8::base::RandomNumberGenerator::SetSeed` and `sub_140832EE0`
- `BigInt` check is modified in `v8::internal::Literal::ToBooleanIsTrue`
- Now we can rewrite the JS script to print out all the expressions that it uses, pack it and then patch the corresponding modified functions
- There are over 1700 expressions, so Z3 will hang when trying to solve all at once
- But since they are all linear, we can solve from the bottom up for a few (say ~50) expressions at a time, then set the result as the new target for the next set of expressions
