const express = require('express');
const axios = require('axios');
const { JSDOM } = require('jsdom');

const app = express();
const PORT = process.env.PORT || 3000;

app.get('/fetch-metadata', async (req, res) => {
    const url = req.query.url;
    try {
        const response = await axios.get(url);
        const dom = new JSDOM(response.data);
        const title = dom.window.document.querySelector('title') ? dom.window.document.querySelector('title').textContent : 'No title available';
        res.json({ title });
    } catch (error) {
        console.error('Error fetching the metadata:', error);
        res.status(500).json({ title: 'Error fetching title' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});