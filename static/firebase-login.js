'use strict';

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, signOut, createUserWithEmailAndPassword, onAuthStateChanged, updateProfile } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";

let auth;

async function saveUserToBackend(user) {
    try {
        await fetch("/save-user", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: user.uid,
                email: user.email,
                name: user.displayName || "No Name"
            })
        });
    } catch (error) {
        console.error("Error saving user to backend:", error);
    }
}

async function sendVerificationEmail(email) {
    try {
        await fetch("/send-verification", {
            method: "POST",
            body: new URLSearchParams({ email })
        });
    } catch (error) {
        console.error("Error sending verification email:", error);
    }
}

function updateUI(isLoggedIn, email = "") {
    const userLabel = document.getElementById("user-label");
    const loginSection = document.getElementById("login-section") || document.getElementById("signup-section");
    const signOutBtn = document.getElementById("sign-out");
    const userInfo = document.getElementById("user-info");

    if (isLoggedIn) {
        if (userLabel) userLabel.textContent = `Welcome, ${email}`;
        if (loginSection) loginSection.hidden = true;
        if (signOutBtn) signOutBtn.hidden = false;
        if (userInfo) userInfo.hidden = false;
    } else {
        if (userLabel) userLabel.textContent = "";
        if (loginSection) loginSection.hidden = false;
        if (signOutBtn) signOutBtn.hidden = true;
        if (userInfo) userInfo.hidden = true;
    }
}

function attachEventListeners() {
    const loginBtn = document.getElementById("login-btn");
    const signupBtn = document.getElementById("signup-btn");
    const signOutBtn = document.getElementById("sign-out");

    if (loginBtn) {
        loginBtn.addEventListener("click", async () => {
            console.log("🔹 Login button clicked");
            const email = document.getElementById("login-email").value;
            const password = document.getElementById("login-password").value;

            try {
                const userCredential = await signInWithEmailAndPassword(auth, email, password);
                const user = userCredential.user;
                const token = await user.getIdToken(true);
                document.cookie = "token=" + token + ";path=/;SameSite=Strict";

                await saveUserToBackend(user);
                await sendVerificationEmail(user.email); // ➔ Send OTP after login
                window.location = "/verify-code";
            } catch (error) {
                console.error("Login Error:", error.code, error.message);
            }
        });
    }

    if (signupBtn) {
        signupBtn.addEventListener("click", async () => {
            console.log("🔹 Signup button clicked");
            const email = document.getElementById("signup-email").value;
            const password = document.getElementById("signup-password").value;
            const confirmPassword = document.getElementById("signup-confirm-password").value;
            const name = document.getElementById("signup-name").value;

            if (password !== confirmPassword) {
                alert("Passwords do not match!");
                return;
            }

            try {
                const userCredential = await createUserWithEmailAndPassword(auth, email, password);
                const user = userCredential.user;
                await updateProfile(user, { displayName: name });
                const token = await user.getIdToken(true);
                document.cookie = "token=" + token + ";path=/;SameSite=Strict";

                await saveUserToBackend(user);
                await sendVerificationEmail(user.email); // ➔ Send OTP after signup
                window.location = "/verify-code";
            } catch (error) {
                console.error("Signup Error:", error.code, error.message);
            }
        });
    }

    if (signOutBtn) {
        signOutBtn.addEventListener("click", async () => {
            console.log("🔹 Sign Out button clicked");
            try {
                await signOut(auth);
                document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
                window.location = "/";
            } catch (error) {
                console.error("Sign-out Error:", error.message);
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    console.log("DOM Loaded. Initializing Firebase...");

    try {
        const res = await fetch("/firebase-config");
        const firebaseConfig = await res.json();

        const app = initializeApp(firebaseConfig);
        auth = getAuth(app);

        console.log("Firebase Initialized");

        onAuthStateChanged(auth, async (user) => {
            if (user) {
                console.log("User logged in:", user.email);
                const token = await user.getIdToken(true);
                document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                await saveUserToBackend(user);
                updateUI(true, user.email);
            } else {
                console.log("No user logged in.");
                updateUI(false);
            }
        });

        attachEventListeners();
    } catch (error) {
        console.error("Firebase Initialization Error:", error);
    }
});
