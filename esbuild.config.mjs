import * as esbuild from 'esbuild';
import fs from 'node:fs';
import path from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';

function simpleHash(str) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0
  }
  return (hash >>> 0).toString(36)
}

const hash = simpleHash(crypto.randomUUID())

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let result = await esbuild.build({
  absWorkingDir: path.join(__dirname, 'assets'),
  nodePaths: ['js'],
  entryPoints: [
    'js/home/index.js',
    'js/settings/settings.js'
  ],
  entryNames: `[dir]/[name]-${hash}`,
  bundle: true,
  // minify: true,
  sourcemap: true,
  target: ['chrome58', 'firefox57', 'safari11', 'edge16'],
  outbase: '.',
  outdir: '../static',
  metafile: true,
  // splitting: true,
  // chunkNames: `chunkNames/[name]-${hash}`,
  // format: 'esm',
});

result.metafile.hash = hash;

fs.writeFileSync('meta.json', JSON.stringify(result.metafile, null, 2));
