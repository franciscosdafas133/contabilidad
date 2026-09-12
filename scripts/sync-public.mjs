import { cpSync, rmSync, existsSync } from 'node:fs';

const src = 'web/dist';
const dest = 'public';
if (!existsSync(src)) {
  console.error('Falta web/dist. Ejecuta antes el build de Vite.');
  process.exit(1);
}
rmSync(dest, { recursive: true, force: true });
cpSync(src, dest, { recursive: true });
console.log('Frontend copiado a public/');
