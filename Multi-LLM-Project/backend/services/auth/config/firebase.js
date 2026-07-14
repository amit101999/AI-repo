import { cert } from 'firebase-admin/app';
import { initializeApp } from 'firebase-admin/app';
import dotenv from 'dotenv';
dotenv.config();

export const firebaseApp = InitializeApp({
    credential: cert()
})