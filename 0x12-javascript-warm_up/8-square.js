#!/usr/bin/node
const size = parseInt(process.argv[2]);

if (Number.isNaN(size)) {
  console.log('Missing size');
} else {
  for (let row = 0; row < size; row++) {
    let line = '';
    for (let column = 0; column < size; column++) {
      line += 'X';
    }
    console.log(line);
  }
}
