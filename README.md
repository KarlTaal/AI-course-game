# AI-course-game
Tehisintellekti kursuse raames loodud mäng, kus käsklusi antakse käe liigutustega.     

#Käivitamine (Ideaalis võiks ka notebookis samu versioone kasutada)
1.  Tee endale Python 3.6.8 environment. Pythoni 3.6.8 leiad siit: https://www.python.org/downloads/release/python-368/
2.  Esimese asjana tuleks uuendada ära pip ja setuptools. Selleks tuleb environmentis Script kaustas käivitada järgmised kaks käsku:   
    `python -m pip install -U --force-reinstall pip`   
    `python -m pip install -U --force-reinstall setuptools`
3.  Järgmiseks tuleks liikuda failiga *requirements.txt* samasse kausta ja käivitada käsk vajalike moodulite tõmbamiseks:   
    `pip install -r requirements.txt`    
    
Kui asja valmis saab, siis peab uurima, et kas saab kuidagi mängu kokku ehitada nii, et õpetajad saaksid lihtsalt klikkides käima panna. Kui ei, siis võiks vähemalt mingi demo video teha, kuidas see mäng töötab.
