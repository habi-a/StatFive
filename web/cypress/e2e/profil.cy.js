const CREDENTIALS = "credentials.json";

describe("Connexion", () => {
  it("Modifier son profil", () => {
    cy.visit("/");
    cy.fetchCredentials(CREDENTIALS);
    cy.login(CREDENTIALS);
    cy.visit("/parametre");
    cy.getElement('[datatestid="profil_textarea"]')
      .clear()
      .type("Je suis un test fonctionnel");
    cy.getElement("select").select("Attaquant");
    cy.getElement('[datatestid="profil_button"]').click();
    cy.getElement("#toast-1-description").contains(
      "Votre profil a bien été modifié"
    );
  });
});
