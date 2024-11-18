# kostal_porssisahko

Yksinkertainen python-skripti, joka kytkee Kostalin Plenticore invertterin syöttötehon rajoituksen päälle, kun sähkön hinta on negatiivinen (pienempi kuin marginaali). Tämän voi ajastaa esim. cronista joka tunti, jolloin se tsekkaa spot-hinta.fi:n API:sta sähkön hinnan ja mikäli se on alhaisempi kuin asetettu marginaali, kytkee tämä invertterin tehon rajoituksen päälle. Plenticore-invertterin syöttötehon rajoitus on toteutettu niin, että jos omaa kulutusta on, tuottaa invertteri kuitenkin aina oman kulutuksen verran sähköä.

Huomaa, että invertteriin on liitettävä energiamittari, jotta syöttötehon rajoitus on mahdollista.
