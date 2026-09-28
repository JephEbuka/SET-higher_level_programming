#!/usr/bin/node

const Square = require('./5-square');

class SquareNew extends Square {
  charPrint (c) {
    const character = c === undefined ? 'X' : c;

    for (let i = 0; i < this.height; i++) {
      console.log(character.repeat(this.width));
    }
  }
}

module.exports = SquareNew;
