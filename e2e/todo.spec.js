/**
 * E2E Tests — Todo TDD (Playwright)            ⏱ 10 minuti
 * ===========================================
 * Prerequisiti: Flask su :5000, http-server su :3000
 *
 * Esegui: npx playwright test
 * Debug:  npx playwright test --headed --slowMo=400
 */
import { test, expect } from '@playwright/test';

// ─────────────────────────────────────────────────────────────────────────────
// 1. Caricamento pagina
// ─────────────────────────────────────────────────────────────────────────────

test('shows empty todo list on load', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByTestId('todo-list')).toBeVisible();
  await expect(page.getByTestId('new-todo-input')).toBeVisible();
});

// ─────────────────────────────────────────────────────────────────────────────
// 2. Aggiunta todo
// ─────────────────────────────────────────────────────────────────────────────

test('adds a todo and shows it in the list', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('new-todo-input').fill('Comprare il latte');
  await page.getByTestId('add-btn').click();

  await expect(page.getByTestId('todo-list')).toContainText('Comprare il latte');
});

test('shows error on empty title', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('add-btn').click();
  await expect(page.getByTestId('error-msg')).not.toBeEmpty();
});

test('adds todo with Enter key', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('new-todo-input').fill('Task da tastiera');
  await page.getByTestId('new-todo-input').press('Enter');
  await expect(page.getByTestId('todo-list')).toContainText('Task da tastiera');
});

// ─────────────────────────────────────────────────────────────────────────────
// 3. Completamento
// ─────────────────────────────────────────────────────────────────────────────

test('completes a todo and updates pending label', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('new-todo-input').fill('Task da completare');
  await page.getByTestId('add-btn').click();

  // Trova il check button e cliccalo
  const item = page.locator('.todo-item').first();
  await item.locator('.check-btn').click();

  // L'item diventa "done" (testo barrato)
  await expect(item).toHaveClass(/done/);

  // Il contatore aggiorna
  await expect(page.getByTestId('pending-label')).toContainText('🎉');
});

// ─────────────────────────────────────────────────────────────────────────────
// 4. Eliminazione
// ─────────────────────────────────────────────────────────────────────────────

test('deletes a todo', async ({ page }) => {
  await page.goto('/');
  await page.getByTestId('new-todo-input').fill('Da eliminare');
  await page.getByTestId('add-btn').click();

  const item = page.locator('.todo-item').first();
  await item.hover();
  await item.locator('.del-btn').click();

  await expect(page.getByTestId('todo-list')).not.toContainText('Da eliminare');
});

// ─────────────────────────────────────────────────────────────────────────────
// 5. Filtri
// ─────────────────────────────────────────────────────────────────────────────

test('filter shows only active todos', async ({ page }) => {
  await page.goto('/');

  // Aggiungi due todo
  await page.getByTestId('new-todo-input').fill('Attivo');
  await page.getByTestId('add-btn').click();
  await page.getByTestId('new-todo-input').fill('Da completare');
  await page.getByTestId('add-btn').click();

  // Completa il secondo
  const items = page.locator('.todo-item');
  await items.nth(1).locator('.check-btn').click();

  // Filtra su "Attivi"
  await page.getByTestId('filter-active').click();
  await expect(page.locator('.todo-item')).toHaveCount(1);
  await expect(page.getByTestId('todo-list')).toContainText('Attivo');
});

// ─────────────────────────────────────────────────────────────────────────────
// 6. Clear completed
// ─────────────────────────────────────────────────────────────────────────────

test('clear completed removes done todos', async ({ page }) => {
  await page.goto('/');

  await page.getByTestId('new-todo-input').fill('Da tenere');
  await page.getByTestId('add-btn').click();
  await page.getByTestId('new-todo-input').fill('Da eliminare');
  await page.getByTestId('add-btn').click();

  // Completa il secondo
  const items = page.locator('.todo-item');
  await items.nth(1).locator('.check-btn').click();

  // Clicca "Elimina completati"
  await page.getByTestId('clear-btn').click();

  await expect(page.locator('.todo-item')).toHaveCount(1);
  await expect(page.getByTestId('todo-list')).toContainText('Da tenere');
});
