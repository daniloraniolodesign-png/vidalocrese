// Legge i dati del sito dai CSV in src/data.
// Un campo vuoto significa "non mostrare": mai segnaposto visibili.
import { parse } from 'csv-parse/sync';
import csvImpostazioni from '../data/impostazioni.csv?raw';
import csvFaq from '../data/faq.csv?raw';
import csvGazzettino from '../data/gazzettino.csv?raw';
import csvConsigli from '../data/consigli.csv?raw';

const leggi = (testo: string): Record<string, string>[] =>
  parse(testo, { columns: true, skip_empty_lines: true, trim: true });

export const imp: Record<string, string> = Object.fromEntries(
  leggi(csvImpostazioni).map((r) => [r.chiave, r.valore ?? '']),
);
export const faq = leggi(csvFaq);
export const consigli = leggi(csvConsigli);

const giorno = new Intl.DateTimeFormat('it-IT', { day: 'numeric', month: 'long', year: 'numeric' });
export const gazzettino = leggi(csvGazzettino)
  .map((r) => ({ ...r, quando: giorno.format(new Date(r.data)) }))
  .sort((a, b) => b.data.localeCompare(a.data));

export const tel = (n: string) => `tel:${n.replace(/\s/g, '')}`;

export const VOCI = [
  { href: '/camere', nome: 'Camere', id: 'camere' },
  { href: '/colazioni', nome: 'Colazioni', id: 'colazioni' },
  { href: '/giardino-e-piscina', nome: 'Piscina', id: 'piscina' },
  { href: '/mare-e-dintorni', nome: 'Mare', id: 'mare' },
  { href: '/chi-siamo', nome: 'Chi siamo', id: 'chi-siamo' },
  { href: '/contatti', nome: 'Contatti', id: 'contatti' },
];
