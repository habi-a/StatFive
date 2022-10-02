const CREDENTIALS = "credentials.json";

describe("Connexion", () => {
  before(() => {
    cy.fetchCredentials(CREDENTIALS);
  });

  it("Connection fail", () => {
    cy.visit("/");
    cy.get('[datatestid="login_mail"').type("test@test.fr");
    cy.get('[datatestid="login_password"').type("mauvaispassword");
    cy.get('[datatestid="login_button').click();
    cy.get('[datatestid="login_error"]').should("be.visible");
  });

  it("Connection with fail otp and otp valid", () => {
    cy.visit("/");
    cy.fixture(CREDENTIALS).then((credentials) => {
      cy.get('[datatestid="login_mail"').clear().type(`${credentials.email}`);
      cy.get('[datatestid="login_password"')
        .clear()
        .type(`${credentials.password}`);
    });
    cy.get('[datatestid="login_button').click();
    cy.url().should("include", "/verification");
    cy.wait(500);
    cy.get("input").eq(0).clear().type("000000");
    cy.get('[datatestid="verification_error"]').should("be.visible");
    for (let i = 0; i <= 5; i++) {
      cy.get(`input:eq(${i})`).clear();
    }
    cy.fixture(CREDENTIALS).then((credentials) => {
      cy.get(`input:eq(0)`).type(`${credentials.code}`);
    });
    cy.wait(3000);
    cy.url().should("include", "/accueil");
  });
});
