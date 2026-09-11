import { test, expect } from '@playwright/test';
import { readFileSync, mkdirSync } from 'node:fs';
const golden = id => JSON.parse(readFileSync(new URL(`../../tests/fixtures/${id}.json`, import.meta.url), 'utf8'));

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'PD1 · Reconocer las cuentas' })).toBeVisible();
});

test('PD1 completo, clasificación contra-activos y persistencia tras recargar', async ({ page }) => {
  const f = golden('pd1_clasificacion');
  for (const [key, value] of Object.entries(f.expected)) await page.locator(`#answer-${key}`).selectOption(value);
  await page.getByRole('button', { name: 'Comprobar respuestas' }).click();
  await expect(page.getByRole('heading', { name: 'Ejercicio completado' })).toBeVisible();
  await expect(page.getByText('29 de 29 respuestas correctas.', { exact: false })).toBeVisible();
  await page.reload();
  await page.getByRole('button', { name: 'Mi progreso' }).click();
  await expect(page.getByRole('heading', { name: 'Mi progreso' })).toBeVisible();
  await expect(page.getByRole('cell', { name: '29 / 29 · Completado' })).toBeVisible();
});

test('práctica ER oculta respuestas y pistas; comprueba error y corrección completa', async ({ page }) => {
  await page.getByRole('button', { name: 'Práctica sin ayuda' }).click();
  await page.getByLabel('Ejercicio', { exact: true }).selectOption('pd3_er');
  await expect(page.getByRole('heading', { name: 'PD3 · EXA PERÚ S.A.C.' })).toBeVisible();
  await expect(page.getByRole('button', { name: 'Ver regla' })).toHaveCount(0);
  await expect(page.getByText('301881.00', { exact: true })).toHaveCount(0);
  await page.locator('#answer-net_sales').fill('1');
  await page.getByRole('button', { name: 'Comprobar respuestas' }).click();
  await expect(page.getByRole('heading', { name: 'Revisa las diferencias' })).toBeVisible();
  await expect(page.getByText('Completa esta respuesta.', { exact: true })).toHaveCount(5);
  const f = golden('pd3_er');
  for (const [key, value] of Object.entries(f.expected)) await page.locator(`#answer-${key}`).fill(Number(value).toFixed(2));
  await page.getByRole('button', { name: 'Comprobar respuestas' }).click();
  await expect(page.getByRole('heading', { name: 'Ejercicio completado' })).toBeVisible();
});

test('Aprender ofrece las cuatro plantillas con encabezados y resultados', async ({ page }) => {
  await page.getByRole('button', { name: 'Aprender un estado' }).click();
  for (const [type, title] of [['ESF', 'Estado de Situación Financiera'], ['ER', 'Estado de Resultados'], ['ECPN', 'Estado de Cambios en el Patrimonio Neto'], ['EFE', 'Estado de Flujos de Efectivo']]) {
    await page.getByRole('button', { name: type, exact: true }).click();
    await expect(page.getByRole('heading', { name: new RegExp(title) })).toBeVisible();
    await expect(page.getByRole('heading', { name: 'Plantilla resuelta' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Comprobar respuestas' })).toHaveCount(0);
  }
});

test('feedback distingue signo EFE y clasificación de actividad', async ({ page }) => {
  await page.getByLabel('Ejercicio', { exact: true }).selectOption('pd3_efe');
  await page.locator('#answer-flow_0').selectOption('AI');
  await page.locator('#answer-AI').fill('8000');
  await page.getByRole('button', { name: 'Comprobar respuestas' }).click();
  await expect(page.getByText('La magnitud coincide; revisa el signo.', { exact: true })).toBeVisible();
  await expect(page.getByText('Distingue operación, inversión y financiamiento.', { exact: true })).toBeVisible();
});

test('Park City, predicción, propagación en cuatro estados y deshacer', async ({ page }) => {
  await page.getByRole('button', { name: 'Integración y simulador' }).click();
  await expect(page.getByText('✓ A = P + PN', { exact: true })).toBeVisible();
  await expect(page.locator('.statement-grid')).toContainText('188,141.00');
  await page.getByRole('button', { name: 'Aplicar operación', exact: true }).click();
  await expect(page.getByRole('heading', { name: '3. Contrasta tu predicción' })).toBeVisible();
  await expect(page.getByText('Faltó incluir esta cuenta.', { exact: true })).toHaveCount(2);
  await expect(page.locator('.statement-grid')).toContainText('188,564.00');
  await expect(page.locator('.change-table')).toContainText('Recalculado');
  await page.getByRole('button', { name: 'Antes de la última operación', exact: true }).click();
  await expect(page.locator('.statement-grid')).toContainText('188,141.00');
  await page.getByRole('button', { name: 'Después', exact: true }).click();
  await page.getByRole('button', { name: 'Deshacer última' }).click();
  await expect(page.locator('.statement-grid')).toContainText('188,141.00');
  await expect(page.getByRole('button', { name: 'Deshacer última' })).toBeDisabled();
  mkdirSync('../docs/qa', { recursive: true });
  await page.screenshot({ path: '../docs/qa/integracion-desktop.png', fullPage: true });
});

test('operación inválida no modifica saldos; empresa nueva acepta un aporte', async ({ page }) => {
  await page.getByRole('button', { name: 'Integración y simulador' }).click();
  await expect(page.getByLabel('Caso inicial')).toBeEnabled();
  await page.getByLabel('Caso inicial').selectOption('empty');
  await expect(page.getByRole('button', { name: 'Aplicar operación', exact: true })).toBeEnabled();
  await page.getByRole('button', { name: 'Aplicar operación', exact: true }).click();
  await expect(page.getByRole('alert')).toContainText('Saldo insuficiente');
  await expect(page.getByText('0 operaciones aplicadas a este caso.', { exact: true })).toBeVisible();
  await page.locator('#operation-type').selectOption('contribution');
  await page.getByRole('button', { name: 'Aplicar operación', exact: true }).click();
  await expect(page.getByText('1 operaciones aplicadas a este caso.', { exact: true })).toBeVisible();
  await expect(page.getByRole('alert')).toHaveCount(0);
});

test('móvil: formulario usable, teclado y página sin desbordamiento', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.getByLabel('Ejercicio', { exact: true }).selectOption('pd3_er');
  await page.locator('#answer-net_sales').fill('989750.00');
  await page.locator('#answer-net_sales').press('Tab');
  await expect(page.getByRole('button', { name: 'Ver regla' }).first()).toBeFocused();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBeTruthy();
  await page.screenshot({ path: '../docs/qa/ejercicio-mobile.png', fullPage: true });
  await page.getByRole('button', { name: 'Integración y simulador' }).click();
  await expect(page.getByText('✓ A = P + PN', { exact: true })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBeTruthy();
});

test('fallo de red muestra un error recuperable', async ({ page }) => {
  await page.route('**/api/catalog', route => route.abort());
  await page.reload();
  await expect(page.getByRole('alert')).toContainText('No se pudo cargar');
  await page.unroute('**/api/catalog');
  await page.getByRole('button', { name: 'Reintentar' }).click();
  await expect(page.getByRole('heading', { name: 'PD1 · Reconocer las cuentas' })).toBeVisible();
});

test('escritorio: no errores de JavaScript ni solicitudes externas durante el uso', async ({ page }) => {
  const errors = [], external = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('request', r => { if (!r.url().startsWith('http://127.0.0.1:8001')) external.push(r.url()); });
  await page.reload();
  await page.getByLabel('Ejercicio', { exact: true }).selectOption('pd3_er');
  await page.getByRole('button', { name: 'Ver regla' }).first().click();
  await expect(page.locator('.hint')).toContainText('PD3');
  expect(errors).toEqual([]); expect(external).toEqual([]);
  await page.screenshot({ path: '../docs/qa/ejercicio-desktop.png', fullPage: true });
});
