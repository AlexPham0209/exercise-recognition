import { SerialPort } from 'serialport'
import { ReadlineParser } from '@serialport/parser-readline'
import express from "express";
import { Server } from "socket.io";
import http from 'http';

const serialPort = 'COM3';

// Start instance of express app and create an HTTP server
const app = express();
const server = http.createServer(app);
const port = process.env.PORT || 2904;

// Establish websocket connection
const io = new Server(server);

// Establish connection with Arduino Nano over COM3 serial port
const serial = new SerialPort({ path: serialPort, baudRate: 9600 });
const parser = serial.pipe(new ReadlineParser({ delimiter: '\r\n' }));

app.get('/', (req, res) => {
    res.send("Hello");
});

server.listen(port, () => {
    console.log(`Listening on port ${port}`);
});

serial.on("open", () => {
  console.log(`Serial port ${serialPort} opened`);
});

parser.on('data', data =>{
  console.log(data);
});