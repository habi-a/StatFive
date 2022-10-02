const CREDENTIALS = "credentials.json";

describe("Connexion", () => {
  it("Créer un match", () => {
    cy.visit("/");
    cy.fetchCredentials(CREDENTIALS, 1);
    cy.login(CREDENTIALS);
    cy.visit("/creation-match");
    cy.get('[datatestid="match_creation"]').should("not.exist");
    cy.get('[datatestid="match_change_video"]').should("not.exist");
    cy.get(".css-b62m3t-container:eq(0)").click();
    cy.wait(500);
    cy.get(".css-b62m3t-container:eq(0)").type("Sofiane 1{enter}");
    cy.get(".css-b62m3t-container:eq(1)").click();
    cy.wait(500);
    cy.get(".css-b62m3t-container:eq(1)").type("Sofiane 2{enter}");
    cy.get('[datatestid="match_video"]').attachFile(
      "../fixtures/five-a-side.mp4",
      {
        encoding: "utf-8",
        subjectType: "drag-n-drop",
      }
    );
    cy.get('[datatestid="match_change_video"]').should("be.visible");
    cy.get('[datatestid="match_creation"]').should("be.visible").click();
    cy.get("#toast-1-description").contains("Elle sera bientôt disponible..");
  });
});
