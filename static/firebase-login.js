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

    if (!loginBtn || !signUpBtn || !signOutBtn) {
        console.error("Missing elements. Event listeners not attached.");
        return;
    }

    // Signup logic
    signUpBtn.addEventListener("click", () => {
        console.log("🔹 Sign Up button clicked");
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        createUserWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                const user = userCredential.user;
                user.getIdToken(true).then((token) => {
                    document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                    console.log("Account created:", user.email);
                    window.location = window.location.pathname;
                });
            })
            .catch((error) => {
                console.error("Sign Up Error:", error.code, error.message);
            });
    });

    // Login logic
    loginBtn.addEventListener("click", () => {
        console.log("🔹 Login button clicked");
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                const user = userCredential.user;
                user.getIdToken(true).then((token) => {
                    document.cookie = "token=" + token + ";path=/;SameSite=Strict";
                    console.log("Logged in:", user.email);
                    window.location = window.location.pathname;
                });
            })
            .catch((error) => {
                console.error("Login Error:", error.code, error.message);
            });
    });

    // Sign-out logic
    signOutBtn.addEventListener("click", () => {
        console.log("Sign Out button clicked");
        signOut(auth)
            .then(() => {
                document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
                console.log("signed out successfully");
                window.location = window.location.pathname;
            })
            .catch((error) => {
                console.error("Sign-out Error:", error.message);
            });
    });
}

function updateUI(isLoggedIn, email = "") {
    // Show/hide elements based on login state
    const userLabel = document.getElementById("user-label");
    const loginBox = document.getElementById("login-box");
    const signOutBtn = document.getElementById("sign-out");
    const userInfo = document.getElementById("user-info");

    if (isLoggedIn) {
        // Show user info
        userLabel.textContent = `Welcome, ${email}`;
        loginBox.hidden = true; 
        signOutBtn.hidden = false
        userInfo.hidden = false; 
    } else {
        // Hide user info
        userLabel.textContent = "";
        loginBox.hidden = false;
        signOutBtn.hidden = true;
        userInfo.hidden = true;
    }
}
