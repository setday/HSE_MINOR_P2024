# PyBot
Minor python bot.

# Development setup

Create env:
```shell
python -m venv PyBot

.\PyBot\Scripts\activate

pip install -r requirements.txt
```

Save install:
```shell
pip freeze > requirements.txt
```

Build debug
```shell
python ./src/main.py
```

Check build release:
```shell
mypy .

pyinstaller.exe ./src/main.py

.\build\main\main.exe
```
