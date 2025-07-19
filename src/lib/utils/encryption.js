import CryptoJS from 'crypto-js';

const SECRET_KEY = 'SomeSecretKey123!'; // Replace with your actual secret key

export function encryptShareableID(id) {
	try {
		if (!id) {
			console.warn('Empty ID passed to encryptShareableID:', id);
			return '';
		}
		const idString = String(id);

		const encrypted = CryptoJS.AES.encrypt(idString, SECRET_KEY).toString();
		return encrypted;
	} catch (error) {
		console.error('Encryption failed:', error);
		return String(id);
	}
}

export function decryptShareableID(encryptedId) {
	try {
		if (!encryptedId) {
			console.warn('Empty encrypted ID passed to decryptShareableID:', encryptedId);
			return '';
		}

		const encryptedString = String(encryptedId);
		const decrypted = CryptoJS.AES.decrypt(encryptedString, SECRET_KEY);
		const decryptedString = decrypted.toString(CryptoJS.enc.Utf8);

		return decryptedString;
	} catch (error) {
		console.error('Decryption failed:', error);
		return String(encryptedId);
	}
}
