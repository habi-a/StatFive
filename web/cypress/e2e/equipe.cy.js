const CREDENTIALS = "credentials.json";

describe("Connexion", () => {
  it("Créer une équipe", () => {
    cy.visit("/");
    cy.fetchCredentials(CREDENTIALS, 1);
    cy.login(CREDENTIALS);
    cy.visit("/equipe");
    const uuid = () => Cypress._.random(0, 1e6);
    const id = uuid();
    cy.get('[datatestid="equipe_button"]').should("not.exist");
    cy.get('[datatestid="equipe_input"]')
      .clear()
      .type(`Test fonctionnel equipe ${id}`);
    for (let i = 0; i <= 4; i++) {
      cy.getElement(`[datatestid="equipe_new_player-${i}"]`).click();
      cy.wait(1000);
      cy.getElement(`[datatestid="new_player_${i}"]`).click();
    }
    cy.getElement('[datatestid="equipe_button"]').should("be.visible").click();
    cy.getElement("#toast-1-description").contains(
      "Votre équipe est disponible"
    );
  });
});
