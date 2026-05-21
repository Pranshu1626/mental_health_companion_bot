(function () {
  const PRIVATE_KEY_STORAGE_KEY = "mindmate_private_key";
  const RSA_ALGORITHM = {
    name: "RSA-OAEP",
    modulusLength: 4096,
    publicExponent: new Uint8Array([1, 0, 1]),
    hash: "SHA-256",
  };

  function arrayBufferToBase64(buffer) {
    const bytes = new Uint8Array(buffer);
    const chunkSize = 0x8000;
    let binary = "";

    for (let i = 0; i < bytes.length; i += chunkSize) {
      binary += String.fromCharCode.apply(null, bytes.subarray(i, i + chunkSize));
    }

    return btoa(binary);
  }

  function base64ToArrayBuffer(base64) {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);

    for (let i = 0; i < binary.length; i += 1) {
      bytes[i] = binary.charCodeAt(i);
    }

    return bytes.buffer;
  }

  async function generateKeyPair() {
    return window.crypto.subtle.generateKey(
      RSA_ALGORITHM,
      true,
      ["encrypt", "decrypt"]
    );
  }

  async function exportPublicKey(publicKey) {
    const exported = await window.crypto.subtle.exportKey("spki", publicKey);
    return arrayBufferToBase64(exported);
  }

  async function savePrivateKey(privateKey) {
    const jwk = await window.crypto.subtle.exportKey("jwk", privateKey);
    localStorage.setItem(PRIVATE_KEY_STORAGE_KEY, JSON.stringify(jwk));
  }

  async function loadPrivateKey() {
    const storedKey = localStorage.getItem(PRIVATE_KEY_STORAGE_KEY);

    if (!storedKey) {
      return null;
    }

    return window.crypto.subtle.importKey(
      "jwk",
      JSON.parse(storedKey),
      {
        name: "RSA-OAEP",
        hash: "SHA-256",
      },
      true,
      ["decrypt"]
    );
  }

  async function importPublicKey(publicKeyBase64) {
    return window.crypto.subtle.importKey(
      "spki",
      base64ToArrayBuffer(publicKeyBase64),
      {
        name: "RSA-OAEP",
        hash: "SHA-256",
      },
      true,
      ["encrypt"]
    );
  }

  async function encryptMessage(message, publicKeyBase64) {
    const publicKey = await importPublicKey(publicKeyBase64);
    const encodedMessage = new TextEncoder().encode(message);

    const ciphertext = await window.crypto.subtle.encrypt(
      {
        name: "RSA-OAEP",
      },
      publicKey,
      encodedMessage
    );

    return arrayBufferToBase64(ciphertext);
  }

  async function decryptMessage(ciphertextBase64, privateKey) {
    const plaintext = await window.crypto.subtle.decrypt(
      {
        name: "RSA-OAEP",
      },
      privateKey,
      base64ToArrayBuffer(ciphertextBase64)
    );

    return new TextDecoder().decode(plaintext);
  }

  window.MindMateCrypto = {
    generateKeyPair,
    exportPublicKey,
    savePrivateKey,
    loadPrivateKey,
    encryptMessage,
    decryptMessage,
  };
})();