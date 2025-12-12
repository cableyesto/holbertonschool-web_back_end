import { createClient } from "redis";

const client = createClient();

client.on("error", function(err) {
    console.log(`Redis client not connected to the server: ${err}`);
    // console.error(`Redis client not connected to the server: ${err}`);
});

client.on("connect", function() {
    console.log("Redis client connected to the server");
});