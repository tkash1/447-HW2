const sqlite3 = require('sqlite3').verbose();
let sql;

// connect to database
const db = new sqlite3.Database('./user.db',sqlite3.OPEN_READWRITE,(err)=>{
    if (err) return console.error(err.message);
})

// create table
sql = `CREATE TABLE users(id INTEGER PRIMARY KEY,name,user_id,points)`;
db.run(sql);

// insert data
sql = `INSERT INTO users(name,user_id,points) VALUES`