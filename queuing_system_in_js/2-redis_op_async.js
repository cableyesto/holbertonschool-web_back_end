import { createClient, print } from "redis";
import { promisify } from "util";

const client = createClient();

client.on("error", function(err) {
    console.log(`Redis client not connected to the server: ${err}`);
});

client.on("connect", function() {
    console.log("Redis client connected to the server");
});

const getAsync = promisify(client.get).bind(client);

async function displaySchoolValue(schoolName) {
    try {
        const value = await getAsync(schoolName);
        console.log(value);
    } catch (error) {
        console.error(error);
    }
}

function setNewSchool(schoolName, value) {
    client.set(schoolName, value, print);
}

// Cannot use top level await with node v12.x
async function main() {
    await displaySchoolValue('Holberton');
    setNewSchool('HolbertonSanFrancisco', '100');
    await displaySchoolValue('HolbertonSanFrancisco');
}

main();