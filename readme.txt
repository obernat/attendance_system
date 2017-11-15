mat moznost aktivne a neaktivne predmety, teda na zaklade uzivatela by som si pamatal dva listy a podla toho generoval okna

kazdy predmet bude mat button HIDE..ak kliknem na hide, vytvori sa novy tab, kde sa presunie dany predmet..a novy tab ostane
vsetky predmety sa budu dynamicky presuvat medzi tabmi na zaklade toho buttonu (alebo checkboxku)
toto vsetky musime ukladat do SETTINGS!!!.txt alebo daco take


!!OVERIT CI MAM AKTUALNE OBDOBIE,!!!

pocas semestrae moze pribudnut a odbudnut predmet ...to treba handlovat
mozna manualne synchronizovat IS...ze bude niekde button ze sync ...alebo import
v APP treba vidiet dochadzku aj z predchadzajucich tyzdnov, teda musi fungovat aj import


hlavne menu bude subjects v nom tlacitko sync

na zaciatku to bude prazdne, stlaci sa tlacitko sync

stavy predmetu:
  Aktivny
  Neaktivny
stavy studenta:
  A  Aktivny
  NA NeaktualizovanyAktivny (pri prechode z N na NA)
  N  Neaktivny
  O  Odpisany

SYNC:
1. predmety = stiahni zoznam predmetov z ais
2. zrusene = lokalna DB predmetov minus predmety z bodu 1
3. pre z in zrusene:
4.   zrus zaznamy pre z z lokalnej DB

5. pre p in predmety:
6.   if p not in local db:
7.      init p in local db 
8.   studenti = stiahne sa zoznam studentov z ais
9.   odpisani = lokalna DB studentov minus studenti z bodu 4
10.  pre o in odpisani:
11.     o.set_state(O)
12.  pre s in studenti:
13.     if (s not in local db) or (s.get_state()==NA):
14.        if s not in local db:
15.           init s in local db pre dane p
16.        if s.get_state() == NA:
17.           s.set_state(A)
18.     elif s.get_state() in [N,O]:
19.        continue
20.     dochadzka = stiahni dochadzku pre s
21.     aktualizacia local DB dochadzka podla IS!!!



lavy klik da ano nie, pravy da na vyber..v tomto menu


