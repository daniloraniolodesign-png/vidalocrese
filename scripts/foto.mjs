// Crea le versioni WebP delle foto (640 e 1280 px, senza ingrandire) in public/img/web.
// Parte da sola prima di "npm run dev" e "npm run build". Le originali stanno in /foto.
import sharp from 'sharp';
import { readdir, mkdir, stat } from 'node:fs/promises';
import { join, parse } from 'node:path';

const SRC = 'foto';
const OUT = 'public/img/web';
const WIDTHS = [640, 1280]; // le foto del cliente arrivano al massimo a 700 px

async function walk(dir) {
  const out = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else if (/\.(jpe?g|png|webp)$/i.test(e.name)) out.push(p);
  }
  return out;
}

await mkdir(OUT, { recursive: true });
const files = await walk(SRC);
let made = 0;
for (const f of files) {
  const rel = parse(f.slice(SRC.length + 1));
  const sub = rel.dir ? `${rel.dir.replace(/[\\/]/g, '-')}-` : '';
  const img = sharp(f);
  const meta = await img.metadata();
  for (const w of WIDTHS) {
    const target = join(OUT, `${sub}${rel.name}-${w}.webp`);
    try { await stat(target); continue; } catch {}
    await sharp(f)
      .resize({ width: Math.min(w, meta.width), withoutEnlargement: true })
      .webp({ quality: 74 })
      .toFile(target);
    made++;
  }
}
console.log(`foto: ${files.length} originali, ${made} versioni nuove`);
