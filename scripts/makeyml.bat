cd "%USERPROFILE%\documents\projects\chatbot\scripts"

call C:\miniconda3\scripts\activate.bat

call conda activate chatbot

call conda list -e > condalist.txt

call pip freeze > piplist.txt

call conda env export > chatbot.yml