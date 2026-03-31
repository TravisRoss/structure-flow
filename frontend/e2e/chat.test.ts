import { expect, test, type Page } from "@playwright/test";

const STUB_TEXT_RESPONSE =
  "[stub_anthropic] Hi! I can help you visualise processes as diagrams. What would you like to create?";
const STUB_DIAGRAM_RESPONSE = "I've generated a diagram based on your request.";

async function sendMessage(page: Page, text: string): Promise<void> {
  await page.getByPlaceholder("Type your message...").fill(text);
  await page.getByRole("button", { name: "Send" }).click();
}

test.beforeEach(async ({ page }) => {
  await page.goto("/");
});

test("shows empty chat and diagram placeholder on first visit", async ({
  page,
}) => {
  await expect(page.getByText("Start a conversation...")).toBeVisible();
  await expect(page.getByText("Your diagram will appear here")).toBeVisible();
});

test("user sends a message and sees the response", async ({ page }) => {
  await sendMessage(page, "hi");

  await expect(page.getByText("hi", { exact: true })).toBeVisible();
  await expect(page.getByText(STUB_TEXT_RESPONSE)).toBeVisible();
  await expect(page.getByText("Your diagram will appear here")).toBeVisible();
});

test("user requests a diagram and sees it appear", async ({ page }) => {
  await sendMessage(page, "Create a flowchart");

  await expect(page.getByText(STUB_DIAGRAM_RESPONSE)).toBeVisible();
  await expect(
    page.getByText("Your diagram will appear here"),
  ).not.toBeVisible();
});

test("shows an error banner if the backend is unreachable", async ({
  page,
}) => {
  await page.route("**/api/chat/stream", (route) => route.abort());

  await sendMessage(page, "hi");

  await expect(
    page.getByText(
      "Unable to reach the server. Please check that the backend is running.",
    ),
  ).toBeVisible();
});

test("shows an error banner when the stream contains an error event", async ({
  page,
}) => {
  await page.route("**/api/chat/stream", (route) =>
    route.fulfill({
      status: 200,
      headers: { "Content-Type": "text/event-stream" },
      body: 'data: {"type":"error","message":"The AI service encountered an error. Please try again."}\n\ndata: {"type":"done"}\n\n',
    }),
  );

  await sendMessage(page, "hi");

  await expect(
    page.getByText("The AI service encountered an error. Please try again."),
  ).toBeVisible();
});

test("clears the input field after sending a message", async ({ page }) => {
  await sendMessage(page, "hi");
  await expect(page.getByText(STUB_TEXT_RESPONSE)).toBeVisible();

  await expect(page.getByPlaceholder("Type your message...")).toHaveValue("");
});

test("clears the error banner when the next message succeeds", async ({
  page,
}) => {
  await page.route("**/api/chat/stream", (route) => route.abort());
  await sendMessage(page, "hi");
  await expect(
    page.getByText(
      "Unable to reach the server. Please check that the backend is running.",
    ),
  ).toBeVisible();

  await page.unroute("**/api/chat/stream");
  await sendMessage(page, "hi");
  await expect(
    page.getByText(
      "Unable to reach the server. Please check that the backend is running.",
    ),
  ).not.toBeVisible();
  await expect(page.getByText(STUB_TEXT_RESPONSE)).toBeVisible();
});

test("preserves conversation history across multiple turns", async ({
  page,
}) => {
  await sendMessage(page, "hi");
  await expect(page.getByText(STUB_TEXT_RESPONSE)).toBeVisible();

  await sendMessage(page, "Create a flowchart");
  await expect(page.getByText(STUB_DIAGRAM_RESPONSE)).toBeVisible();

  await expect(page.getByText("hi", { exact: true })).toBeVisible();
  await expect(page.getByText(STUB_TEXT_RESPONSE)).toBeVisible();
  await expect(
    page.getByText("Create a flowchart", { exact: true }),
  ).toBeVisible();
});

test("diagram is replaced when user requests a new one", async ({ page }) => {
  await sendMessage(page, "hi");
  await expect(page.getByText(STUB_TEXT_RESPONSE)).toBeVisible();

  await sendMessage(page, "now create a flowchart");
  await expect(page.getByText(STUB_DIAGRAM_RESPONSE)).toBeVisible();
  await expect(
    page.getByText("Your diagram will appear here"),
  ).not.toBeVisible();
});
