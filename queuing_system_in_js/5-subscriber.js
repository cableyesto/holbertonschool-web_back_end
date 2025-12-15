import { createClient } from "redis";

const subscriber = createClient();

subscriber.on("error", function(err) {
    console.log(`Redis client not connected to the server: ${err}`);
});

subscriber.on("connect", function() {
    console.log("Redis client connected to the server");
});

subscriber.on("message", function(channel, message) {
    if (message === "KILL_SERVER") {
        subscriber.unsubscribe();
        subscriber.quit();
    }

    console.log(message);
});

subscriber.subscribe("holberton school channel");