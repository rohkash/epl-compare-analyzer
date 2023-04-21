const express = require('express');
const { MongoClient } = require('mongodb');
require('dotenv').config();

constardf app = express();
const port = process.env.PORT || 3000;

const client = new MongoClient(process.env.MONGOCLIENT_URL, { useUnifiedTopology: true });

async function start() {
  await client.connect();
  console.log('Connected to database');

  const db = client.db('test');

  app.get('/', (req, res) => {
    res.send('Welcome to my app!');
  });
  
  
  app.listen(port, () => {
    console.log(`Server listening on port ${port}`);
  });
}

start();
