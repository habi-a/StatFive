// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

import "cypress-file-upload";
import "cypress-wait-until";



Cypress.Commands.add("login", (CREDENTIALS) => {
  cy.fixture(CREDENTIALS).then((credentials) => {
    cy.get('[datatestid="login_mail"').clear().type(`${credentials.email}`);
    cy.get('[datatestid="login_password"')
      .clear()
      .type(`${credentials.password}`);
  });
  cy.get('[datatestid="login_button').click();
  cy.url().should("include", "/verification");
  cy.wait(500);
  cy.fixture(CREDENTIALS).then((credentials) => {
    cy.get("input").eq(0).clear().type(`${credentials.code}`);
  });
  cy.wait(5000);
  cy.url().should("include", "/accueil");
});

Cypress.Commands.add("getElement", (elem) => {
  cy.waitUntil(() => Cypress.$(elem).length > 0, {
    errorMsg: `${elem} not found`, // overrides the default error message
    timeout: 30000, // waits up to 30000 ms, default to 5000
    interval: 300, // performs the check every 1000 ms, default to 200
  });
  return cy.get(elem);
});

Cypress.Commands.add("fetchCredentials", (fileName, nb = 0) => {
  cy.request({
    url: `https://api.preprod.statfive.fr/api/admin/dataset?role=${nb}`,
    header: {
      "Content-Type": "application/json",
    },
  }).then((data) => {
    cy.exec(
      `echo '${JSON.stringify(
        data.body.data,
        null,
        2
      )}' > cypress/fixtures/${fileName}`
    );
  });
});
