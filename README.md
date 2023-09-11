# Werkplaats2_starter
Starter repository voor Werkplaats 2. Deze repository bevat een Flask applicatie met een aantal van de componenten die we ook nodig hebben om de werkplaats opdracht uit te voeren: 
- Een database
- Templates
- De Flask server
- HTML & Style sheets


# Installatie
Om de virtual environment te activeren moet je het uitvoeringsbeleid van PowerShell wijzigen: 

1. Zoek PowerShell in de Windows zoekbalk. 
2. Open PowerShell als administrator.
3. Type het volgende commando in PowerShell:
``` 
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```


Om Flask te kunnen starten zul je eerst de Flask packages moeten installeren. Wil je latere problemen met versies voorkomen, dan raden we je aan een virtual environment te maken en daar de modules in te installeren:
Mocht je Python versie 3 of hoger gebruiken in Pycharm, dan krijg je al de optie om een VENV aan te maken. Regel 1 en 2 van onderstaande code zijn in dat geval niet nodig.
```
pip install virtualenv
virtualenv venv
.\venv\scripts\activate
pip install -r requirements.txt
```


Om de demo applicatie te starten: 
``` 
.\venv\scripts\activate
python app.py
```

Om de virtual environment te verlaten:
 ``` 
deactivate
```

# Inloggen
Als je de demoapplicatie start, kom je op het inlogscherm terecht.
Op deze manier hebben alleen redacteurs toegang tot de applicatie. 
Voor het gemak hebben we een testaccount gemaakt waarmee je toegang krijgt tot de applicatie.

Inloggegevens
``` 
Gebruikersnaam: Admin
Wachtwoord: test123
```


# Navigatiebar
Na het inloggen word je doorverwezen naar de homepage.
Bovenin zie je een navigatiebar.
Deze maakt gebruik van dropdowns die zichtbaar worden op het moment dat je met je muis over een kopje zweeft.

Hieronder beschrijven we wat elk kopje in de navigatiebar doet:

Home
``` 
> Je wordt teruggebracht naar ons Home-scherm
```

Auteurs 
``` 
> Alle Auteurs (Dit toont alle rijen in de tabel auteurs.)
> Ongeldige Medewerkers (Dit toont alle rijen in de tabel auteurs waarvan de kolom medewerker fouten bevat.)
> Ongeldige Auteurs (Dit toont alle rijen in de tabel vragen met ongeldige auteurs.)
> Ontbrekende Auteurs (Dit toont alle rijen in de tabel vragen met ontbrekende auteurs.)
``` 

Leerdoelen 
``` 
> Alle leerdoelen (Dit toont alle rijen in de tabel leerdoelen.)
> Ongeldige leerdoelen (Dit toont alle rijen in de tabel vragen met ongeldige leerdoelen.)
> Ontbrekende leerdoelen (Dit toont alle rijen in de tabel vragen met ontbrekende leerdoelen.)
``` 

Vragen 
``` 
> Alle vragen (Dit toont alle rijen in de tabel vragen.)
> HTML-fouten (Dit toont alle rijen in de tabel vragen met HTML-codes.)
```

Logout 
``` 
 > Je wordt uitgelogd en teruggebracht naar het loginscherm.
           
```
