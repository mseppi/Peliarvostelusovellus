# Peliarvostelusovellus
Sovellus pelien arvostelemiseen. Sovelluksen ideana on, että käyttäjä voi kirjautua sivulle, jossa on pelejä, joita voi arvostella.

### Ominaisuuksiin kuuluu
- Sisäänkirjautuminen ja rekisteröityminen
- Arvostelujen lisääminen
- Arvostelujen kommentoiminen
- Arvosteluista tykkääminen
- Profiilin tarkisteleminen ja muokkaaminen
- Ylläpitäjä voi poistaa postauksia ja käyttäjiä

## Tämänhetkinen tilanne
Sovellukseen voi kirjautua ja rekisteröityä. Sovelluksen sisällä voi tarkastella omaa profiiliaan. Sovelluksessa voi lisätä pelejä, joihin taas voi lisätä arvosteluja. Arvosteluja voi kommentoida.

## Puuttuvat ominaisuudet mitkä tehdään ennen loppupalautusta
- CSS
- Tykkääminen
- CSRF-haavoittuvuuden poistaminen
- Koodin rakenteen hiominen

## Käynnistysohje paikallisesti

- Asenna PostgreSQL kurssin ohjeiden mukaisesti
- Käynnistä tietokanta komennolla ```start-pg.sh```
- Lataa repositori
- Luo sovelluksen juurihakemistoon .env tiedosto ja syötä sinne
```
DATABASE_URL=postgresql+psycopg2:///tietokannan-osoite
SECRET_KEY=salainen-avain
```
- Aktivoi virtuaaliympäristö komennoilla

``` python3 -m venv venv ```

``` source venv/bin/activate ```

- Asenna riippuvuuudet virtuaaliympäristössä komennolla ```pip install -r requirements.txt```
- Määritä sovelluksen tietokanta komennolla ```psql<schema.sql```
- Käynnistä sovellus komennolla ```flask run```
- Tee sovellukselle käyttäjä ja kirjaudu sisään
