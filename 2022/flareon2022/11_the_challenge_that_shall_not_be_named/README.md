# Chall11
- `"_MEIPASS2"` string in the binary -> PyInstaller packed program
- Extract it with PyExtractor using python3.7 -> entry point at `11`
- Rename it to `11.pyc` and decompile it with `decompyle3`
- It's an PyArmor obfuscated script, running it will result in an error `No module named _crypt`
- We can inject code via this `_crypt` package -> simply put your own python script named `_crypt.py` in the same directory
- Inject some code to analyze the stack frames -> the flag is stored in `11.py`'s frame in plain text
