# WebIK

## Samenvatting

- Wij gaan een trivia web app maken die gefocust is op leraren en leerlingen.
  De website zal Fakta heten.
  Hierin zullen gebruikers het tegen elkaar opnemen door trivia vragen omstebeurt te beantwoorden.
  Er zullen verschillende categorieën zijn voor vragen (denk hierbij aan examenvakken).
  Wat onze trivia uniek maakt is dat de leraar de voortgang van zijn leerlingen kan bekijken
  en zo kan de leraar nog extra aandacht besteden op categorieën die minder goed zijn gemaakt.


## Afhankelijkheden

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
Voor het creëeren van een trivia website zijn een aantal externe componenten benodigd.

#### BootStrap:
BootStrap is een framework wat ons in staat stelt om snel en simpel een website te creëeren.
Het Framework biedt veel manieren om een pagina snel en professioneel op te maken.
Voornamelijk is het framework handig om een standaard lay-out te maken voor elke pagina

#### Foundation Framework
Foundation framework is een handig framework waar wij gebruik van kunnen maken om onze lay-out te creëeren.
[Foundation Framework](https://foundation.zurb.com/)

### Concurrende bestaande websites
Een welbekende trivia website is zonder twijfel kahoot.
Het interessante aan kahoot is het feit dat iedereen tegelijk dezelfde vragenlijst kan maken.
Ookwel een room genoemd.

Verder biedt kahoot ook de mogelijkheid om je eigen vragenlijsten te bedenken wat kahoot ook zo populair
maakt in het onderwijs.

Een andere bekende trivia pagina is Sporcle. Het interessante aan Sporcle is dat er al vragenlijsten zijn voor veel categorieën
die ook weer vervolgens in andere soorten rooms gespeeld kan worden. Een voorbeeld van zo'n variant is een room waar elke vraag goed beantwoordt moet worden.
Als je een vraag fout beantwoordt, dan eindigt de quiz

### Moeilijkste delen
Een groot probleem wat in voorbereiding tot het maken van een trivia website is hoe we ervoor gaan zorgen dat mensen bij de vragen kunnen komen die iemand heeft gegenereed.
Verder moet een gebruiker; een account kunnen aanmaken, in/uitloggen, vragenlijsten kunnen maken en een gebruiker moet ook in staat zijn om de scorelijst te bekijken zodra
hij of zij klaar is met de vragenlijst.

Verder moet een gebruiker niet vragen 2 keer kunnen maken. Daarom gaan we een room.html file maken die elke keer 1 vraag oproept
door dit te doen kunnen we op button press checken of het antwoord goed of fout is dat toevoegen aan de score en daarna de nieuw vraag laden


## Belangrijkste features trivia-applicatie:

1. Gebruikers moeten een account kunnen aanmaken
2. Gebruikers moeten daarna een quiz kunnen genereren/kiezen
3. Vervolgens krijgen gebruikers multiplechoice vragen uit de gekozen categorie.
4. Daarna moeten de gebruikers de vragen kunnen beantwoorden.
5. Tijdens het beantwoorden moet een score worden bijgehouden
4. Na het afmaken van een quiz moeten gebruikers kunnen zien hoe ze presteren t.o.v. ander gebruikers d.m.v. een leaderboard.
5. Een leraar moet een tabel kunnen zien waar de quiz uitgelicht staat en daarna kunnen zien of een vak in het algemeen goed of slecht is gemaakt.

## Website pagina voorstel

![Website pagina voorstel](/Images/pagina_voorstel.jpeg)