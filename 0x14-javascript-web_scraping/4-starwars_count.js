#!/usr/bin/node

const request = require('request');

request(process.argv[2], (error, response, body) => {
  if (error) {
    console.log(error);
  } else {
    const films = JSON.parse(body).results;
    let count = 0;

    for (const film of films) {
      if (film.characters.some(character => character.includes('/18/'))) {
        count++;
      }
    }

    console.log(count);
  }
});
