----------------------------------------------------------------------
Gorillas in Python – Imitace hry "Gorillas" z roku 1990 (MS DOS, QBasic)
----------------------------------------------------------------------

Tento projekt je volnou napodobeninou klasické hry „Gorillas“, která byla
součástí ukázkových programů v Microsoft QBasic (MS DOS) z roku 1990. 
Tehdejší hra spočívala v tom, že dva hráči ovládali gorily sedící na 
vrcholcích budov a snažili se navzájem zasáhnout banánem (projektilem) 
tím, že nastavili vhodný úhel a sílu hodu.

V této imitaci je hra napsána v jazyce Python, s využitím knihovny 
`pygame` pro grafiku. Vyžaduje proto mít nainstalovaný Python 3.8 (nebo 
vyšší) a knihovnu `pygame`.

----------------------------------------------------------------------
Ovládání
----------------------------------------------------------------------
1. Šipky nahoru/dolů  ->  Zvětšení či zmenšení úhlu hodu
2. Šipky vlevo/vpravo ->  Zvětšení či zmenšení síly hodu
3. Mezerník           ->  Vykonání hodu banánem
4. F1                 ->  Zobrazení / skrytí nápovědy a informací o hře
5. ESC                ->  Ukončení hry (případně nápovědy)

----------------------------------------------------------------------
Spuštění hry
----------------------------------------------------------------------
1. Ujistěte se, že máte nainstalovaný Python (verze 3.8+).
2. Doinstalujte knihovnu pygame příkazem:
   
   pip install pygame

3. Stáhněte (nakopírujte) si zdrojové soubory hry do jedné složky.
4. V dané složce spusťte příkaz:

   python gorillas.py

Tím se otevře okno s hrou. Pokud si nejste jisti, že máte nainstalovaný 
Python, zkontrolujte pomocí:

   python --version

nebo

   python3 --version

----------------------------------------------------------------------
Kompilace
----------------------------------------------------------------------
Kompilaci v klasickém slova smyslu Python nepotřebuje (jedná se o 
interpretovaný jazyk). Pokud byste chtěli vytvořit spustitelný 
soubor (např. .exe pro Windows), lze využít nástroje jako `pyinstaller`.

Postup by vypadal například takto:
1. Nainstalujte pyinstaller: 
   pip install pyinstaller
2. V kořenové složce projektu (soubory gorillas.py atd.) spusťte:
   pyinstaller --onefile gorillas.py
3. Ve složce dist/ se poté objeví samostatný spustitelný soubor 
   (například gorillas.exe na Windows).

----------------------------------------------------------------------
Licence
----------------------------------------------------------------------
Tato hra (zdrojové kódy) je k dispozici pod licencí Creative Commons (CC). 
Uživateli je dovoleno dílo sdílet, upravovat a šířit za předpokladu, 
že uvede autora a zachová stejnou licenci na odvozená díla.

Více detailů viz: 
https://creativecommons.org/licenses/

----------------------------------------------------------------------
Autor
----------------------------------------------------------------------
Tento projekt vytvořil XY jako ukázku, jak by mohla vypadat „moderní“ verze 
klasické DOSové hry. Slouží pro studijní i zábavné účely.
----------------------------------------------------------------------
