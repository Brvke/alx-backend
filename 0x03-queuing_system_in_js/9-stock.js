const express = require('express');
const { createClient } = require('redis');
const { promisify } = require('util');

const app = express();
const client = createClient();
const port = 1245;
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

client.on('error', err => console.log('Redis client not connected to the server:', err));
const getAsync = promisify(client.get).bind(client);

function getItemById(id) {
  for (const product of listProducts) {
    if (id === product.itemId) {
      return product;
    }
  }
}

function reserveStockById(itemId, stock) {
  client.set(itemId, stock);
}

async function getCurrentReservedStockById(itemId) {
  try {
    const value = await getAsync(itemId);
    return value;
  } catch (err) {
    return NaN;
  }
}

app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async function (req, res) {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));

  if (item) {
    const stock = await getCurrentReservedStockById(itemId);
    const resItem = {
      itemId: item.itemId,
      itemName: item.itemName,
      price: item.price,
      initialAvailableQuantity: item.initialAvailableQuantity,
      currentQuantity: stock !== null ? parseInt(stock) : item.initialAvailableQuantity,
    };
    res.json(resItem);
  } else {
    res.json({ "status": "Product not found" });
  }
});

app.get('/reserve_product/:itemId', async function (req, res) {
  const itemId = req.params.itemId;
  const item = getItemById(parseInt(itemId));

  if (item) {
    const stock = await getCurrentReservedStockById(itemId);
    if (stock === null) {
      res.json({ "status": "Not enough stock available", "itemId": item.itemId })
    } else {
      reserveStockById(itemId, stock)
      res.json({ "status": "Reservation confirmed", "itemId": item.itemId })
    }
  } else {
    res.json({ "status": "Product not found" });
  }
});

app.listen(port, () => console.log('...'));
