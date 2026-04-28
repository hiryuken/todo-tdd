/**
 * Vitest Unit Tests — todo-logic.js            ⏱ 10 minuti
 * =============================================
 * Test puri: nessun fetch, nessun DOM.
 *
 * Esegui: npm test
 */
import { describe, it, expect } from 'vitest';
import { formatPendingLabel, filterTodos, validateTitle, sortTodos } from '../src/todo-logic.js';

// ─────────────────────────────────────────────────────────────────────────────
// formatPendingLabel
// ─────────────────────────────────────────────────────────────────────────────

describe('formatPendingLabel', () => {
  it('shows celebration when nothing is pending', () => {
    expect(formatPendingLabel(0)).toContain('🎉');
  });

  it('uses singular for 1 item', () => {
    expect(formatPendingLabel(1)).toContain('1 attività rimasta');
  });

  it('uses plural for more than 1', () => {
    expect(formatPendingLabel(3)).toContain('3 attività rimaste');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// filterTodos
// ─────────────────────────────────────────────────────────────────────────────

describe('filterTodos', () => {
  const items = [
    { id: '1', title: 'A', done: false },
    { id: '2', title: 'B', done: true  },
    { id: '3', title: 'C', done: false },
  ];

  it('filter=all returns all items', () => {
    expect(filterTodos(items, 'all')).toHaveLength(3);
  });

  it('filter=active returns only pending items', () => {
    const result = filterTodos(items, 'active');
    expect(result).toHaveLength(2);
    expect(result.every(i => !i.done)).toBe(true);
  });

  it('filter=completed returns only done items', () => {
    const result = filterTodos(items, 'completed');
    expect(result).toHaveLength(1);
    expect(result[0].id).toBe('2');
  });

  it('returns empty array when no items match filter', () => {
    expect(filterTodos([], 'active')).toHaveLength(0);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// validateTitle
// ─────────────────────────────────────────────────────────────────────────────

describe('validateTitle', () => {
  it('accepts a normal title', () => {
    expect(validateTitle('Comprare il latte').valid).toBe(true);
  });

  it('rejects empty string', () => {
    expect(validateTitle('').valid).toBe(false);
  });

  it('rejects whitespace-only string', () => {
    expect(validateTitle('   ').valid).toBe(false);
  });

  it('rejects title longer than 100 chars', () => {
    expect(validateTitle('A'.repeat(101)).valid).toBe(false);
  });

  it('returns an error message on invalid input', () => {
    expect(validateTitle('').error).toBeTruthy();
  });

  it('accepts title of exactly 100 chars', () => {
    expect(validateTitle('A'.repeat(100)).valid).toBe(true);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// sortTodos
// ─────────────────────────────────────────────────────────────────────────────

describe('sortTodos', () => {
  it('puts pending items before completed', () => {
    const items = [
      { id: '1', done: true  },
      { id: '2', done: false },
    ];
    const sorted = sortTodos(items);
    expect(sorted[0].done).toBe(false);
    expect(sorted[1].done).toBe(true);
  });

  it('does not mutate the original array', () => {
    const items = [{ id: '1', done: true }, { id: '2', done: false }];
    sortTodos(items);
    expect(items[0].done).toBe(true);
  });
});
