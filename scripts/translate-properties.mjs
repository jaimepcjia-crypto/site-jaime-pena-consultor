import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const sourcePath = resolve(root, 'src/data/empreendimentos.json');
const cachePath = resolve(root, '.astro/property-translation-cache.json');
const targets = ['en', 'es'];
const fields = ['localizacao', 'statusObra', 'metragens', 'tipologia', 'description'];
const protectedTerms = [
  'Moura Dubeux',
  'Jaime Pena',
  'MD Store',
  'Salvador',
  'Bahia',
  'Rio Vermelho',
  'Horto Florestal',
  'Caminho das Árvores',
  'Shopping da Bahia',
  'Farol da Barra',
  'Morro do Cristo',
  'Praia da Paciência',
  'Casa do Rio Vermelho',
  'Architects + Co',
  'Takeda Design',
];

const source = JSON.parse(await readFile(sourcePath, 'utf8'));
let cache = {};
try {
  cache = JSON.parse(await readFile(cachePath, 'utf8'));
} catch {
  // First run.
}

function protect(text) {
  let result = text;
  const replacements = [];
  for (const term of protectedTerms) {
    if (!result.includes(term)) continue;
    const token = `ZXQTERM${replacements.length}QXZ`;
    replacements.push([token, term]);
    result = result.replaceAll(term, token);
  }
  return { result, replacements };
}

function restore(text, replacements) {
  let result = text;
  for (const [token, term] of replacements) {
    result = result.replaceAll(token, term);
  }
  return result;
}

async function requestTranslation(text, target, attempt = 1) {
  const key = `${target}:${text}`;
  if (cache[key]) return cache[key];

  const { result, replacements } = protect(text);
  const url = new URL('https://translate.googleapis.com/translate_a/single');
  url.searchParams.set('client', 'gtx');
  url.searchParams.set('sl', 'pt');
  url.searchParams.set('tl', target);
  url.searchParams.set('dt', 't');
  url.searchParams.set('q', result);

  try {
    const response = await fetch(url, { signal: AbortSignal.timeout(30000) });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const body = await response.json();
    const translated = restore(body[0].map((part) => part[0]).join(''), replacements);
    cache[key] = translated;
    return translated;
  } catch (error) {
    if (attempt >= 5) throw error;
    await new Promise((resolvePromise) => setTimeout(resolvePromise, attempt * 1500));
    return requestTranslation(text, target, attempt + 1);
  }
}

async function translateText(text, target) {
  if (!text) return text;
  if (text.length <= 3500) return requestTranslation(text, target);

  const lines = text.split('\n');
  const translated = [];
  for (const line of lines) {
    translated.push(line ? await requestTranslation(line, target) : '');
  }
  return translated.join('\n');
}

async function translateProperty(property, target) {
  const translated = {};
  for (const field of fields) {
    translated[field] = await translateText(property[field], target);
  }
  translated.sections = [];
  for (const section of property.sections ?? []) {
    translated.sections.push({
      heading: await translateText(section.heading, target),
      items: await Promise.all(section.items.map((item) => translateText(item, target))),
    });
  }
  return translated;
}

await mkdir(dirname(cachePath), { recursive: true });
for (const target of targets) {
  const output = {};
  for (const [index, property] of source.entries()) {
    console.log(`[${target}] ${index + 1}/${source.length} ${property.slug}`);
    output[property.slug] = await translateProperty(property, target);
    await writeFile(cachePath, `${JSON.stringify(cache)}\n`);
  }
  const outputPath = resolve(root, `src/data/empreendimentos.${target}.json`);
  await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`);
}
