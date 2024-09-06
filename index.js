const { Builder, By, until } = require('selenium-webdriver');
const path = require('path');

(async function testGitHubPages() {
    // Créez une instance du navigateur
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // Remplacez l'URL par l'URL de votre GitHub Pages
        await driver.get('https://votre-utilisateur.github.io/nom-du-repository/');

        // Attendre que l'élément avec les classes spécifiques soit présent
        let element = await driver.wait(until.elementLocated(By.css('a.ant-typography.css-zl9ks2')), 10000);

        // Cliquer sur l'élément trouvé
        await element.click();

        // Vérifier le texte affiché après le clic
        let output = await driver.findElement(By.id('output'));
        let outputText = await output.getText();
        console.log("Texte affiché après le clic:", outputText);

        // Vérifiez que le texte affiché est correct
        if (outputText === 'Lien cliqué avec succès depuis GitHub Pages !') {
            console.log("Test réussi !");
        } else {
            console.log("Test échoué !");
        }
    } catch (error) {
        console.error('Une erreur est survenue :', error);
    } finally {
        // Fermer le navigateur
        await driver.quit();
    }
})();
