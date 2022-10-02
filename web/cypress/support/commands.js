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

Cypress.Commands.add("fetchCredentials", (fileName, nb = 0) => {
  const baseURL = Cypress.env("apiUrl");
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
