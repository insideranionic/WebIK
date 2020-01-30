# Facta

## Gemaakt door:
- Robin Bergman
- Ruben Curiël
- Mike Evertsen
- Merijn van der Leek

## Samenvatting

- Wij hebben een trivia web app gemaakt die gefocust is op leraren en leerlingen.
  Het doel van Facta is om kinderen voor te bereiden op de CITO toets waar de vragen ook meerkeuze zijn.
  De website heet Facta afkomstig van het Zweedse woord voor weetje.
  Hierin kan je op een king of the hill achtige wijze individueel je vragen maken.
  Als de quiz klaar is kan je je resultaten vergelijken met andere op het leaderboard.
  Er zijn verschillende vakken voor de quiz zodat je kan zien waar je nog aan moet werken.
  Wat onze trivia uniek maakt is dat de leraar de voortgang van zijn leerlingen kan bekijken
  en zo kan de leraar nog extra aandacht besteden op categorieën die minder goed zijn gemaakt.

## Belangrijkste features van Facta:

1. Gebruikers kunnen een account aanmaken voor zowel leraar als leerling.
2. Leraar kan een quiz genereren op basis van parameters die hij/zij invult.
3. Vervolgens kan de gemaakt quiz gemaakt worden door iedereen die weet wat de naam van de quiz is
4. Na de quiz is er een leaderboard te zien om te kijken hoe je heb gescored ten opzichte van de rest
5. De leraar kan op zijn eigen account bekijken wat leerlingen hebben gescoord voor quizes en op basis daarvan ondersteuning bieden.

## Rolverdeling.
Tijdens het maken van de website zijn de rollen over het algemeen hetzelfde gebleven.
Merijn deed vooral de layout en de algemene opmaak van de website. Hij werd hierbij zo nu en dan ondersteund door Ruben
die hier al wat meer ervaring mee heeft.
Verder Heeft Ruben zich net als Mike vooral gefocust op het laten werken van de functies. Bij het maken van deze functies
functioneerde Robin in principe als een vliegende kiep en hielp hij mij en Ruben in het bugfixen van de functies.

### Help_web.py
In dit bestand zal je onze functies vinden voor application.py. In dit bestand staan funcies die SQL code bevat
en er staan ook veel check functies in om te voorkomen dat de gebruiker iets verkeerds doet.

### Navigatie
Onze github heeft een map genaamd WebIK en daarin bevinden zich ook submappen en bestanden.
De bestanden die hier staan zijn apart van de README file zijn de python en de database bestanden.'
De submappen die zich bevinden in de map zijn: html, static en templates.
HTML bevat gebruikte plaatjes voor onze website
Static bevat vooral onze CSS bestanden die we gebruiken in application.py
Als laatste hebben we nog Templates waarin al onze html bestanden zijn.

### Databronnen
Om onze trivia website te maken is een API van belang.
Daarom hebben we voor [Open Trivia DB](https://opentdb.com/) gekozen.
Deze API stelt ons in staat om de gebruiker een random generated vragenlijstje
te laten maken met bepaalde parameters die de gebruiker kan afstellen.
De parameters zijn:

- Hoeveelheid vragen
- Categorie
- Moeilijkheidsgraad
- Het type vragenlijst. (Waar/Niet waar of Multiple choice) -- wij hebben ervoor gekozen om alleen multiple choice te gebruiken

### Externe componenten
We hebben niet gebruikt gemaakt van een framework aangezien we ervoor hebben gekozen om de website zelf te stylen.
op deze manier hadden we meer ruimte om de site precies op te maken zoals wij wilden en ook orgineel te blijven.
De site is nog steeds bruikbaar op de mobiel zonder gebruik te maken van een framework

### Concurrende bestaande websites
Een welbekende trivia website is zonder twijfel kahoot.
Het interessante aan kahoot is het feit dat iedereen tegelijk dezelfde vragenlijst kan maken.
Ookwel een room genoemd.

Verder biedt kahoot ook de mogelijkheid om je eigen vragenlijsten te bedenken wat kahoot ook zo populair
maakt in het onderwijs.

Een andere bekende trivia pagina is Sporcle. Het interessante aan Sporcle is dat er al vragenlijsten zijn voor veel categorieën
die ook weer vervolgens in andere soorten rooms gespeeld kan worden. Een voorbeeld van zo'n variant is een room waar elke vraag goed beantwoordt moet worden.
Als je een vraag fout beantwoordt, dan eindigt de quiz

### Producvideo
[Link naar youtube](https://youtu.be/vxXI9tiqzOM)

### Website homepage

![Website pagina voorstel](/html/facta.png)

