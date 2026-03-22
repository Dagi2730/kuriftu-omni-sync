const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// --- MIDDLEWARE ---
app.use(cors()); // This fixes the 'Blocked by CORS' error in your browser
app.use(express.json());

// --- DATABASE CONNECTION ---
mongoose.connect(process.env.MONGO_URI || 'mongodb://localhost:27017/kuriftu_db')
    .then(() => console.log('✅ Connected to Kuriftu MongoDB'))
    .catch(err => console.error('❌ MongoDB Connection Error:', err));

// --- DATA STORAGE (Temporary until we use Mongo models) ---
let activeAlerts = [];

// --- ROUTES ---

// 1. Health Check
app.get('/', (req, res) => {
    res.send('Kuriftu Omni-Sync API is Running...');
});

// 2. Dashboard Stats (Energy & Food Waste)
app.get('/api/savings/status', (req, res) => {
    res.json({
        energy_saved_etb: 1250,
        food_waste_prevented_kg: 15.4,
        active_alerts: activeAlerts.length
    });
});

// 3. Post a New Alert (Used by your Telegram Bot)
app.post('/api/alerts', (req, res) => {
    const { room, issue } = req.body;
    
    const newAlert = {
        id: Date.now(),
        room: room || "Unknown Room",
        issue: issue || "General Issue",
        timestamp: new Date()
    };

    activeAlerts.push(newAlert);
    console.log("🚨 NEW ALERT RECEIVED:", newAlert);
    res.status(201).json({ message: "Alert logged successfully", alert: newAlert });
});

// 4. Get All Alerts (Used by your React Dashboard)
app.get('/api/alerts', (req, res) => {
    res.json(activeAlerts);
});

// 5. Clear Alerts (Optional: Use this to reset your demo)
app.delete('/api/alerts/clear', (req, res) => {
    activeAlerts = [];
    res.json({ message: "All alerts cleared" });
});

// --- START SERVER ---
app.listen(PORT, () => {
    console.log(`🚀 Server heart beating on port ${PORT}`);
});