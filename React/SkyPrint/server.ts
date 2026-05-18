import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import admin from "firebase-admin";
import bcrypt from "bcryptjs";
import fs from "fs";

// Load Firebase Config
const firebaseConfig = JSON.parse(fs.readFileSync("./firebase-applet-config.json", "utf-8"));

// Initialize Firebase Admin
// In this environment, applicationDefault() will work because it's running in Cloud Run
// with the project's service account.
if (admin.apps.length === 0) {
  admin.initializeApp({
    projectId: firebaseConfig.projectId,
  });
}

const db = admin.firestore(firebaseConfig.firestoreDatabaseId);
const auth = admin.auth();

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

  // API Route: Login with username/password
  app.post("/api/login", async (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ error: "Usuário e senha são obrigatórios." });
    }

    try {
      const userRef = db.collection("users").doc(username);
      const secretRef = db.collection("auth_secrets").doc(username);
      
      const userDoc = await userRef.get();
      const secretDoc = await secretRef.get();

      // Check if it's the initial admin setup
      if (!userDoc.exists && username === "admin" && password === "admin") {
        const hashedPassword = await bcrypt.hash("admin", 10);
        
        // Use a transaction to ensure atomic creation
        await db.runTransaction(async (t) => {
          t.set(userRef, {
            uid: username,
            displayName: "Administrador",
            email: `${username}@printcontrol.local`,
            role: "manager",
            createdAt: admin.firestore.FieldValue.serverTimestamp(),
          });
          t.set(secretRef, {
            hashedPassword,
            updatedAt: admin.firestore.FieldValue.serverTimestamp(),
          });
        });

        const customToken = await auth.createCustomToken(username);
        return res.json({ token: customToken });
      }

      if (!userDoc.exists || !secretDoc.exists) {
        return res.status(401).json({ error: "Usuário ou senha incorretos." });
      }

      const isValid = await bcrypt.compare(password, secretDoc.data()?.hashedPassword);
      if (!isValid) {
        return res.status(401).json({ error: "Usuário ou senha incorretos." });
      }

      // Generate custom token for Firebase Client SDK login
      const customToken = await auth.createCustomToken(username);
      res.json({ token: customToken });

    } catch (error) {
      console.error("Login Error:", error);
      res.status(500).json({ error: "Erro interno do servidor." });
    }
  });

  // API Route: Create User (by Manager)
  // This will be called from the frontend when a manager adds a new user
  app.post("/api/users/create", async (req, res) => {
    const { managerToken, newUser } = req.body;
    const { username, role } = newUser;

    try {
      // Verify the manager's status using their custom token
      const decodedToken = await auth.verifyIdToken(managerToken);
      const managerRef = db.collection("users").doc(decodedToken.uid);
      const managerSnap = await managerRef.get();

      if (!managerSnap.exists || managerSnap.data()?.role !== "manager") {
        return res.status(403).json({ error: "Permissão negada. Apenas gerentes podem criar usuários." });
      }

      // Default password is '123456' for new users (they can change it later if implemented)
      const hashedPassword = await bcrypt.hash("123456", 10);
      const userRef = db.collection("users").doc(username);
      const secretRef = db.collection("auth_secrets").doc(username);

      const existingUser = await userRef.get();
      if (existingUser.exists) {
        return res.status(400).json({ error: "Este usuário já existe." });
      }

      await db.runTransaction(async (t) => {
        t.set(userRef, {
          uid: username,
          displayName: username,
          email: `${username}@printcontrol.local`,
          role: role,
          createdAt: admin.firestore.FieldValue.serverTimestamp(),
        });
        t.set(secretRef, {
          hashedPassword,
          updatedAt: admin.firestore.FieldValue.serverTimestamp(),
        });
      });

      res.json({ success: true });
    } catch (error) {
      console.error("User Creation Error:", error);
      res.status(500).json({ error: "Erro ao criar usuário." });
    }
  });

  // Vite middleware for development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
