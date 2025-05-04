import { SerialPort } from 'serialport'
import { ReadlineParser } from '@serialport/parser-readline'
import express from "express";
import { Server } from "socket.io";
import http from 'http';
import path from 'path';

const serialPort = 'COM3';
const __dirname = path.resolve();

// Start instance of express app and create an HTTP server
const app = express();
const server = http.createServer(app);
const port = process.env.PORT || 2904;

app.use(express.static(path.join(__dirname, 'demo/app/dist')));

// Establish websocket connection
const io = new Server(server);

// Establish connection with Arduino Nano over COM3 serial port
const serial = new SerialPort({ path: serialPort, baudRate: 9600 });
const parser = serial.pipe(new ReadlineParser({ delimiter: '\r\n' }));

app.get('/', (req, res) => {
    res.status(200).send("Good");
});

io.on('connection', (socket) => {
  console.log('A user connected');
});

serial.on("open", () => {
  console.log(`Serial port ${serialPort} opened`);
});

parser.on('data', data => {
  const param = data.split(',');
  if (param.length != 4)
      return;
  
  const name = param[0];
  const probability = param.slice(1).map((x) => parseFloat(x));

  io.emit('data', {"name": name, "probability": probability});
});

server.listen(port, () => {
    console.log(`Listening on port ${port}`);
});

