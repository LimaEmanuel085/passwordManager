const bcrypt = require('bcrypt');
const e = require('express');
const passwordGenerate = require('generate-password');

const userCreatedPasswords = [];
const cryptoUserPasswords = [];

exports.viewAllPasswords = (req, res) => {
    res.status(200).json({
        message: "Suas genhas são:",
        createdPasswords: userCreatedPasswords,
        cryptoPasswords: cryptoUserPasswords
    })
}

exports.viewCreatedPasswords = (req, res) => {
    res.status(200).json({
        message: "Suas senhas criadas são:",
        createdPasswords: userCreatedPasswords
    })
}

exports.viewCryptoPasswords = (req, res) => {
    res.status(200).json({
        message: "Suas senhas criptografadas são:",
        cryptoPasswords: cryptoUserPasswords
    })
}

exports.createPassword = (req, res) => {
    const { length, numbers, symbols, uppercase} = req.body;
    if (!length) {
        return res.status(400).json({
            message: "Indique no mínimo o tamanho da senha"
        })
    }
    try {

        const newPassword = passwordGenerate.generate({
            length: length,
            numbers: numbers || false,
            symbols: symbols || false,
            uppercase: uppercase || false,
        });

        userCreatedPasswords.push(newPassword);

        res.status(200).json({
            message: "Sua nova senha é: " + newPassword
        })
    } catch (e) {
        console.log(e)
        res.status(500).json({
            error: e,
            message: "Erro ao gerar a senha"
        })
    }
}

exports.cryptoPassword = (req, res) => {
    const {password, saltLength} = req.body;

    if (!password || !saltLength) {
        return res.status(400).json({
            message: "Preencha todos os campos"
        })
    }

    if (saltLength < 4 || saltLength > 10) {
        return res.status(400).json({
            message: "O tamanho do salt deve ser entre 4 e 10"
        })
    }

    try{

        const salt = bcrypt.genSaltSync(saltLength);
    
        const hashedPassword = bcrypt.hashSync(password, salt);
    
        res.status(200).json({
            message: "Senha criptografada com sucesso!",
            hashedPassword: hashedPassword
        })


    } catch (error) {

        res.status(500).json({
            message: "Erro ao criptografar a senha"
        })

    }
}