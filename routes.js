const express = require('express');
const router = express.Router();

const passController = require('./controllers/passController');


//Home route
router.get('/', (req, res) => {
    res.status(200).json({
        message: "Bem vindo(a) ao gerador de senhas! Aqui você pode gerar senhas e criptografá-las"
    });
})

//Views paswords routes
router.get('/viewPasswords', passController.viewAllPasswords);
router.get('/createdPasswords', passController.viewCreatedPasswords);
router.get('/cryptoPasswords', passController.viewCryptoPasswords);

//Create passwords routes
router.post('/createPassword', passController.createPassword);
router.post('/cryptoPassword', passController.cryptoPassword);

module.exports = router;