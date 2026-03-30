import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  use: {
    baseURL: "http://127.0.0.1:5173",
  },
  webServer: [
    {
      command: "node_modules/.bin/vite",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: !process.env.CI,
    },
    {
      command: "MODEL_PROVIDER=stub_anthropic make -C ../backend dev",
      url: "http://localhost:8000/openapi.json",
      reuseExistingServer: !process.env.CI,
    },
  ],
});
