import { test, expect } from "@playwright/test";

const TEXT_RESPONSE = {
  message: "Hi! I can help you create diagrams.",
  diagram: null,
};

const DIAGRAM_RESPONSE = {
  message: "Here's your diagram.",
  diagram: "graph TD\n  A[Start] --> B[End]",
};

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test("shows empty chat and diagram placeholder on first visit", async ({ page }) => {
  await expect(page.getByText("Start a conversation...")).toBeVisible();
  await expect(page.getByText("Your diagram will appear here")).toBeVisible();
});

test("user sends a message and sees the response", async ({ page }) => {
  await page.route("**/api/chat", (route) => route.fulfill({ json: TEXT_RESPONSE }));

  await page.getByPlaceholder("Type your message...").fill("hi");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByText("hi", { exact: true })).toBeVisible();
  await expect(page.getByText(TEXT_RESPONSE.message)).toBeVisible();
  await expect(page.getByText("Your diagram will appear here")).toBeVisible();
});

test("user requests a diagram and sees it appear", async ({ page }) => {
  await page.route("**/api/chat", (route) => route.fulfill({ json: DIAGRAM_RESPONSE }));

  await page.getByPlaceholder("Type your message...").fill("Create a flowchart");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByText(DIAGRAM_RESPONSE.message)).toBeVisible();
  await expect(page.getByText("Your diagram will appear here")).not.toBeVisible();
});

test("diagram is replaced when user requests a new one", async ({ page }) => {
  await page.route("**/api/chat", (route) => route.fulfill({ json: TEXT_RESPONSE }));

  await page.getByPlaceholder("Type your message...").fill("hi");
  await page.getByRole("button", { name: "Send" }).click();
  await expect(page.getByText(TEXT_RESPONSE.message)).toBeVisible();

  await page.route("**/api/chat", (route) => route.fulfill({ json: DIAGRAM_RESPONSE }));

  await page.getByPlaceholder("Type your message...").fill("now create a flowchart");
  await page.getByRole("button", { name: "Send" }).click();

  await expect(page.getByText(DIAGRAM_RESPONSE.message)).toBeVisible();
  await expect(page.getByText("Your diagram will appear here")).not.toBeVisible();
});
