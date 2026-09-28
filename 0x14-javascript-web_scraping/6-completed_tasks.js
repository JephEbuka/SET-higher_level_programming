#!/usr/bin/node

const request = require('request');

request(process.argv[2], (error, response, body) => {
  if (error) {
    console.log(error);
  } else {
    const tasks = JSON.parse(body);
    const completed = {};

    tasks.forEach(task => {
      if (task.completed) {
        if (completed[task.userId] === undefined) {
          completed[task.userId] = 0;
        }

        completed[task.userId]++;
      }
    });

    console.log(completed);
  }
});
