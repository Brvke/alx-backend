const { promisify } = require('util');
import { createClient } from 'redis';
const redis = require('redis');

const client = createClient();

client.on('error', err => console.log('Redis client not connected to the server:', err));

console.log('Redis client connected to the server');

const getAsync = promisify(client.get).bind(client);

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

async function displaySchoolValue(schoolName) {
  try {
    const value = await getAsync(schoolName);
    console.log(value);
  } catch (err) {
    console.error(err);
  }
}

displaySchoolValue('Holberton').then(() => {
  setNewSchool('HolbertonSanFrancisco', '100');
  displaySchoolValue('HolbertonSanFrancisco');
});
