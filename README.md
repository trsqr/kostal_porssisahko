# kostal_porssisahko

Yksinkertainen python-skripti, joka kytkee Kostalin Plenticore invertterin syöttötehon rajoituksen päälle, kun sähkön hinta on negatiivinen (pienempi kuin marginaali). Tämän voi ajastaa esim. cronista joka tunti, jolloin se tsekkaa spot-hinta.fi:n API:sta sähkön hinnan ja mikäli se on alhaisempi kuin asetettu marginaali, kytkee tämä invertterin tehon rajoituksen päälle. Plenticore-invertterin syöttötehon rajoitus on toteutettu niin, että jos omaa kulutusta on, tuottaa invertteri kuitenkin aina oman kulutuksen verran sähköä.

Muokkaa skriptiin invertterin IP-osoite, hallinnan salasana ja sähköyhtiösi marginaali.

Huomaa, että invertteriin on liitettävä energiamittari, jotta syöttötehon rajoitus on mahdollista. Kts. ohjekirjan [1] kappale 3.6.

### Vaatimukset

Jotta tämä toimisi, on seuraavat oltava asennettuna:

* python 3.9 tai uudempi
* pykoplenti (pip install pykoplenti)

### Viitteet

[1] Ohjekirja, Kostal Plenticore Plus, https://cdn-production.kostal.com/-/media/document-library-folder---kse/2023/11/20/14/52/plenticore-plus_ba_fi.pdf?rev=-1&hash=E5C4E55894D5EE29CA0B83AB3319D9F7
