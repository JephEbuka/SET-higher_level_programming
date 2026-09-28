#!/usr/bin/node

const dict = require('./101-data').dict;
const newDict = {};

Object.keys(dict).forEach((key) => {
  const occurrence = dict[key];

  if (newDict[occurrence] === undefined) {
    newDict[occurrence] = [];
  }

  newDict[occurrence].push(key);
});

console.log(newDict);
