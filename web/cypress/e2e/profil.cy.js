const CREDENTIALS = "credentials.json";

describe("Connexion", () => {
  it("Modifier son profil", () => {
    cy.visit("/");
    cy.fetchCredentials(CREDENTIALS);
    cy.login(CREDENTIALS);
    cy.visit("/parametre");
    cy.get('[datatestid="profil_textarea"]')
      .clear()
      .type("Je suis un test fonctionnel");
    cy.get("select").select("Attaquant");
    cy.get('[datatestid="profil_button"]').click();
    cy.get("#toast-1-description").contains("Votre profil a bien été modifié");
  });
});
