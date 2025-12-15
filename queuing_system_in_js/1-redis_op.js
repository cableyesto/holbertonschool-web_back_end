import { createClient, print } from "redis";

const client = createClient();

client.on("error", function(err) {
    console.log(`Redis client not connected to the server: ${err}`);
});

client.on("connect", function() {
    console.log("Redis client connected to the server");
});

function displaySchoolValue(schoolName) {
    client.get(schoolName, (err, reply) => {
        if (err) {
            console.log(err);
        } else {
            console.log(reply);
        }
    });
}

function setNewSchool(schoolName, value) {
    client.set(schoolName, value, print);
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');