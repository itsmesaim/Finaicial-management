'use strict';

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, signOut, createUserWithEmailAndPassword, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

let auth;

document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOM Loaded. Initializing Firebase...");

    try {
        const res = await fetch("/firebase-config");
        const firebaseConfig = await res.json();

        const app = initializeApp(firebaseConfig);
        auth = getAuth(app);

        console.log("Firebase Initialized");

        // Monitor authentication state
        onAuthStateChanged(auth, (user) => {
            if (user) {
                console.log("User logged in:", user.email);
                user.getIdToken(true).then((token) => {
                    document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                    updateUI(true, user.email);
                });
            } else {
                console.log("No user logged in.");
                updateUI(false);
            }
        });

        // Attach event listeners
        attachEventListeners();
    } catch (error) {
        console.error("Firebase Initialization Error:", error);
    }
});

function attachEventListeners() {
    const loginBtn = document.getElementById("login");
    const signUpBtn = document.getElementById("sign-up");
    const signOutBtn = document.getElementById("sign-out");

    if (loginBtn) {
        loginBtn.addEventListener("click", handleLogin);
    }
    if (signUpBtn) {
        signUpBtn.addEventListener("click", handleSignUp);
    }
    if (signOutBtn) {
        signOutBtn.addEventListener("click", handleSignOut);
    }
}

async function handleLogin() {
    console.log("🔹 Login button clicked");
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        user.getIdToken(true).then(async (token) => {
            document.cookie = "token=" + token + ";path=/;SameSite=Strict";
            updateUI(true, user.email);
            await sendVerificationEmail(user.email);
            window.location = "/verify-code";
        });
    } catch (error) {
        console.error("Login Error:", error.code, error.message);
    }
}

async function handleSignUp() {
    console.log("🔹 Sign Up button clicked");
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password") ? document.getElementById("confirm-password").value : null;

    if (confirmPassword !== null && password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        user.getIdToken(true).then(async (token) => {
            document.cookie = "token=" + token + ";path=/;SameSite=Strict";
            updateUI(true, user.email);
            await sendVerificationEmail(user.email);
            window.location = "/verify-code";
        });
    } catch (error) {
        console.error("Sign Up Error:", error.code, error.message);
    }
}

async function handleSignOut() {
    console.log("🔹 Sign Out button clicked");
    try {
        await signOut(auth);
        document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
        console.log("Signed out successfully");
        window.location = "/";
    } catch (error) {
        console.error("Sign-out Error:", error.message);
    }
}

async function sendVerificationEmail(email) {
    try {
        const formData = new FormData();
        formData.append("email", email);

        await fetch("/send-verification", {
            method: "POST",
            body: formData
        });
    } catch (error) {
        console.error("Failed to send verification email:", error);
    }
}

function updateUI(isLoggedIn, email = "") {
    const userLabel = document.getElementById("user-label");
    const loginBox = document.getElementById("login-box");
    const signOutBtn = document.getElementById("sign-out");
    const userInfo = document.getElementById("user-info");

    if (isLoggedIn) {
        if (userLabel) userLabel.textContent = `Welcome, ${email}`;
        if (loginBox) loginBox.hidden = true;
        if (signOutBtn) signOutBtn.hidden = false;
        if (userInfo) userInfo.hidden = false;
    } else {
        if (userLabel) userLabel.textContent = "";
        if (loginBox) loginBox.hidden = false;
        if (signOutBtn) signOutBtn.hidden = true;
        if (userInfo) userInfo.hidden = true;
    }
}
