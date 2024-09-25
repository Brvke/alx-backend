const express = require('express');
const { createClient } = require('redis');
const { promisify } = require('util');
const kue = require('kue');
const { availableParallelism } = require('os');

const queue = kue.createQueue();
const app = express();
const client = createClient();
const port = 1245;
let reservationEnabled = true;

client.on('error', err => console.log('Redis client not connected to the server:', err));

console.log('Redis client connected to the server');
// client.set('available_seats', 50);
const getAsync = promisify(client.get).bind(client);

function reserveSeat(number) {
  client.set('available_seats', number);
}

async function getCurrentAvailableSeats() {
  try {
    const value = await getAsync('available_seats');
    return value;
  } catch (err) {
    console.error(err);
  }
}

app.get('/available_seats', async function (req, res) {
  const seat = await getCurrentAvailableSeats();
  res.json({ "numberOfAvailableSeats": seat });
});

app.get('/reserve_seat', (req, res) => {
  if (reservationEnabled === false) {
    res.json({ "status": "Reservation are blocked" });
    return;
  }
  const job = queue.create('reserve_seat', { 'seat': 1 }).save((error) => {
    if (error) {
      res.json({ "status": "Reservation failed" });
    } else {
      res.json({ "status": "Reservation in process" });
    }
  });
  job.on('complete', () => console.log(`Seat reservation job ${job.id} completed`));
  job.on('failed', (err) => console.log(`Seat reservation job ${job.id} failed: ${err}`));
});

app.get('/process', async function (req, res) {
  res.json({ "status": "Queue processing" });
  queue.process('reserve_seat', async function (job, done) {
    const currentseats = await getCurrentAvailableSeats();
    if (currentseats <= 0) {
      reservationEnabled = false;
      done(Error('Not enough seats available'));
    }
    reserveSeat(currentseats - 1);
    done();
  })
})

app.listen(port, () => console.log('...'));
