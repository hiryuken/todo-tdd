import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: false,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? 'github' : 'list',

  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],

  webServer: [
    {
      command: 'cd backend && python run.py',
      port: 5000,
      reuseExistingServer: !process.env.CI,
      timeout: 20_000,
    },
    {
      command: 'cd frontend && npx http-server src -p 3000 -c-1 --silent',
      port: 3000,
      reuseExistingServer: !process.env.CI,
      timeout: 15_000,
    },
  ],
});
