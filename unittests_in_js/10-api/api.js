const express = require('express');
const app = express();
const port = 7865;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('Welcome to the payment system');
});

app.get('/cart/:id(\\d+)', (req, res) => {
  res.send(`Payment methods for cart ${req.params.id}`);
});

app.get('/available_payments', (req, res) => {
  const obj = {
    payment_methods: {
      credit_cards: true,
      paypal: false
    }
  };
  res.json(obj);
});

app.post('/login', (req, res) => {
  if (!req.body) {
    return res.sendStatus(404);
  }
  const name = req.body.userName
  if (!name) {
    return res.sendStatus(404);
  }
  return res.send(`Welcome ${name}`);
});

app.listen(port, () => {
  console.log(`API available on localhost port ${port}`);
});