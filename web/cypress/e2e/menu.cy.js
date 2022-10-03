const CREDENTIALS = "credentials-role-1.json";
const CREDENTIALS_ONE = "credentials-role-2.json";
const CREDENTIALS_TWO = "credentials-role-3.json";

describe("Connexion", () => {
  beforeEach(() => {
    cy.visit("/");
    cy.clearLocalStorage();
    cy.clearCookies();
  });

  it("Menu pour role 0", () => {
    cy.fetchCredentials(CREDENTIALS);
    cy.login(CREDENTIALS);
    cy.getElement('[datatestid="menu_url"]').should("have.length", 5);
  });
  it("Menu pour role 1", () => {
    cy.fetchCredentials(CREDENTIALS_ONE, 1);
    cy.login(CREDENTIALS_ONE);
    cy.getElement('[datatestid="menu_url"]').should("have.length", 7);
  });
  it("Menu pour role 2", () => {
    cy.fetchCredentials(CREDENTIALS_TWO, 2);
    cy.login(CREDENTIALS_TWO);
    cy.getElement('[datatestid="menu_url"]').should("have.length", 8);
  });
});
