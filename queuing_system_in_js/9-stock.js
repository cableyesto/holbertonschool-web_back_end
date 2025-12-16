import express from 'express';
import { createClient } from "redis";
import { promisify } from "util";


const listProducts = [
  {
    "itemId": 1,
    "itemName": "Suitcase 250",
    "price": 50,
    "initialAvailableQuantity": 4
  },
  {
    "itemId": 2,
    "itemName": "Suitcase 450",
    "price": 100,
    "initialAvailableQuantity": 10
  },
  {
    "itemId": 3,
    "itemName": "Suitcase 650",
    "price": 350,
    "initialAvailableQuantity": 2
  },
  {
    "itemId": 4,
    "itemName": "Suitcase 1050",
    "price": 550,
    "initialAvailableQuantity": 5
  }
];

// Utility functions
function getItemById(id) {
    const res = listProducts.filter((product) => product.itemId === Number(id));
    return res[0];
}

// Redis functions
const client = createClient();
const getAsync = promisify(client.get).bind(client);

async function getCurrentReservedStockById(itemId) {
    try {
        return await getAsync(`item.${itemId}`);
    } catch (error) {
        console.error(error);
    }
}

function reserveStockById(itemId, stock) {
    client.set(`item.${itemId}`, stock);
}

// Express app
const app = express();
const port = 1245; 
app.use(express.json());

app.get('/list_products', (req, res) => {
    return res.json(listProducts);
});

app.get('/list_products/:itemId(\\d+)', async (req, res) => {
    let itemObject = getItemById(req.params.itemId);
    if (itemObject) {
        let redisData = await getCurrentReservedStockById(req.params.itemId);
        itemObject = {
            ...itemObject,
            currentQuantity: Number(redisData)
        };
        return res.json(itemObject);
    } else {
        return res.json({status: "Product not found"});
    }
});

app.get('/reserve_product/:itemId(\\d+)', async (req, res) => {
    let itemObject = getItemById(req.params.itemId);
    if (itemObject) {
        let currentStock = await getCurrentReservedStockById(req.params.itemId);

        if (Number(currentStock) === 0 && currentStock !== null) {
            return res.json({status: "Not enough stock available", itemId: itemObject.itemId});
        }

        // initialize the current stock
        if (currentStock === null) {
            reserveStockById(
                req.params.itemId,
                --itemObject.initialAvailableQuantity
            );
        } else {
            reserveStockById(
                req.params.itemId,
                --currentStock
            );
        }
        return res.json({status: "Reservation confirmed", itemId: itemObject.itemId});
    } else {
        return res.json({status: "Product not found"});
    }
});

app.listen(port, () => {
  console.log(`API available on localhost port ${port}`);
});