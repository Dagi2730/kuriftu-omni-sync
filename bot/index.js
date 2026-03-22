// bot/index.js
const { Telegraf } = require('telegraf');
const axios = require('axios');
require('dotenv').config();

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => ctx.reply('Welcome to Kuriftu! 🌿 I am your AI assistant. Type "help" if you need anything.'));

// Scenario: Guest reports a problem (e.g., "The AC is broken")
bot.on('text', async (ctx) => {
    const message = ctx.message.text.toLowerCase();

    if (message.includes('broken') || message.includes('fix') || message.includes('problem')) {
        try {
            // 1. Tell the Server about the problem
            await axios.post('http://localhost:5000/api/alerts', {
                room: "Room 302", // In a real app, we'd get this from the guest profile
                issue: message,
                severity: "High"
            });

            // 2. Reply to the Guest
            ctx.reply("I've alerted the Maintenance team and the Manager. They are on their way! Would you like a fresh juice while you wait at the bar? 🍹");
        } catch (err) {
            console.error("Error linking to server:", err.message);
            ctx.reply("I'm having trouble reaching the team, but I will keep trying!");
        }
    }
});

bot.launch().then(() => console.log('🤖 Bot is listening...'));