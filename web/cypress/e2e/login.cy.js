const CREDENTIALS = "credentials.json";

describe("Connexion", () => {
  before(() => {
    cy.fetchCredentials(CREDENTIALS);
  });

  it("Connection fail", () => {
    cy.visit("/");
    cy.getElement('[datatestid="login_mail"').type("test@test.fr");
    cy.getElement('[datatestid="login_password"').type("mauvaispassword");
    cy.getElement('[datatestid="login_button').click();
    cy.getElement('[datatestid="login_error"]').should("be.visible");
  });

  it("Connection with fail otp and otp valid", () => {
    cy.visit("/");
    cy.fixture(CREDENTIALS).then((credentials) => {
      cy.getElement('[datatestid="login_mail"')
        .clear()
        .type(`${credentials.email}`);
      cy.getElement('[datatestid="login_password"')
        .clear()
        .type(`${credentials.password}`);
    });
    cy.getElement('[datatestid="login_button').click();
    cy.url().should("include", "/verification");
    cy.wait(500);
    cy.getElement("input").eq(0).clear().type("000000");
    cy.wait(1000);
    cy.getElement('[datatestid="verification_error"]').should("be.visible");
    for (let i = 0; i <= 6; i++) {
      cy.getElement(`input:eq(${i})`).clear();
    }
    cy.fixture(CREDENTIALS).then((credentials) => {
      cy.getElement(`input:eq(0)`).clear().type(`${credentials.code}`);
    });
    cy.wait(3000);
    cy.url().should("include", "/accueil");
  });
});
