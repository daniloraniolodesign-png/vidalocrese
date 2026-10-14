# Sito Vida Locrese

Sito statico in Astro per Vida Locrese, B&B a Merici (Gerace, RC). Progetto Cosmos Agency.

## Comandi
- `npm install` (Node 22.12 o superiore)
- `npm run dev` — anteprima in locale
- `npm run build` — crea il sito in `dist/`

Le foto stanno in `foto/` (prese dal sito attuale, al massimo 700 px di lato). Prima di `dev` e `build`, `scripts/foto.mjs` crea le versioni WebP in `public/img/web/` (non va su git).

## Dove si cambiano i contenuti
- `src/data/impostazioni.csv` — telefoni, email, indirizzo, link Booking e mappa, orari. Campo vuoto = non mostrato.
- `src/data/faq.csv` — domande frequenti della home (anche nei dati strutturati per Google).
- `src/data/gazzettino.csv` — le notizie di Donna Ida.
- `src/data/consigli.csv` — ristoranti e link utili della pagina Mare e dintorni.

## Anteprima su Vercel
Sull'indirizzo *.vercel.app il sito risponde con "noindex" (regola in `vercel.json`), così Google non lo indicizza come copia. Sul dominio vero la regola non si applica.

## Prima di andare online
- [ ] Foto originali in alta risoluzione (quelle attuali sono al massimo 700 px) e logo in formato vettoriale.
- [ ] Nome e dati fiscali di chi gestisce la struttura, codice CIN (obbligatorio per le strutture ricettive) in `impostazioni.csv`.
- [ ] Decidere come si prenota: oggi il modulo chiede la disponibilità (servizio da impostare in `PUBLIC_FORM_ENDPOINT`) e c'è il link a Booking.com.
- [ ] Completare privacy e cookie (note in cima alle pagine) e farle leggere a un consulente.
- [ ] Nomi o colori ufficiali delle quattro camere, se ne hanno.
- [ ] DNS del dominio verso Vercel (oggi il sito è su Aruba), Search Console, sitemap inviata.
- [ ] Controllare i reindirizzamenti in `vercel.json`.
