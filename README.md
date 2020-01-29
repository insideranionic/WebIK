# Fakta

## Gemaakt door:
Robin Bergman
Ruben Curiël
Mike Evertsen
Merijn van der Leek

## Samenvatting

- Wij hebben een trivia web app gemaakt die gefocust is op leraren en leerlingen.
  Het doel van Fakta is om kinderen voor te bereiden op de CITO toets waar de vragen ook meerkeuze zijn.
  De website heet Fakta afkomstig van het Zweedse woord voor weetje.
  Hierin kan je op een king of the hill achtige wijze individueel je vragen maken.
  Als de quiz klaar is kan je je resultaten vergelijken met andere op het leaderboard.
  Er zijn verschillende vakken voor de quiz zodat je kan zien waar je nog aan moet werken.
  Wat onze trivia uniek maakt is dat de leraar de voortgang van zijn leerlingen kan bekijken
  en zo kan de leraar nog extra aandacht besteden op categorieën die minder goed zijn gemaakt.

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

## Belangrijkste features van Fakta:

1. Gebruikers kunnen een account aanmaken voor zowel leraar als leerling.
2. Leraar kan een quiz genereren op basis van parameters die hij/zij invult.
3. Vervolgens kan de gemaakt quiz gemaakt worden door iedereen die weet wat de naam van de quiz is
4. Na de quiz is er een leaderboard te zien om te kijken hoe je heb gescored ten opzichte van de rest
5. De leraar kan op zijn eigen account bekijken wat leerlingen hebben gescoord voor quizes en op basis daarvan ondersteuning bieden.

## Website pagina voorstel

![Website pagina voorstel](/html/pagina_voorstel.jpeg)

![Website pagina voorstel](/html/Images/pagina_voorstel/login.jpeg)

![Website pagina voorstel](/html/Images/pagina_voorstel/home.jpeg)

![Website pagina voorstel](/html/Images/pagina_voorstel/register.jpeg)

![Website pagina voorstel](/html/Images/pagina_voorstel/room.jpeg)

![Website pagina voorstel](/html/Images/pagina_voorstel/find_room.jpeg)

![Website pagina voorstel](/html/Images/pagina_voorstel/leaderboard.jpeg)

![Website pagina voorstel](/html/Images/pagina_voorstel/result.jpeg)

![Website pagina voorstel](/html/Images/pagina_voorstel/finish.jpeg)
