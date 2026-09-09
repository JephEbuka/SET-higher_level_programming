#!/usr/bin/node
function factorial (number) {
  if (Number.isNaN(number) || number <= 1) {
    return 1;
  }

  return number * factorial(number - 1);
}

const number = parseInt(process.argv[2]);

console.log(factorial(number));
