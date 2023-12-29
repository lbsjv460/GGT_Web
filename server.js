const express = require("express");
const bodyParser = require("body-parser");
const app = express();
const PORT = 3000;

// Temporary users data (replace with a database in a real application)
const users = [
  { username: "admin", password: "admin" },
  { username: "user", password: "password" },
];

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

// Middleware to check if a user is logged in
const requireLogin = (req, res, next) => {
  if (!req.session || !req.session.user) {
    res.redirect("/login");
  } else {
    next();
  }
};

// Set up session
const session = require("express-session");
app.use(
  session({ secret: "your-secret-key", resave: true, saveUninitialized: true }),
);

app.get("/", requireLogin, (req, res) => {
  res.sendFile(__dirname + "/public/index.html");
});

app.get("/login", (req, res) => {
  res.sendFile(__dirname + "/public/login.html");
});

app.post("/login", (req, res) => {
  const { username, password } = req.body;

  const user = users.find(
    (u) => u.username === username && u.password === password,
  );

  if (user) {
    req.session.user = user;
    res.redirect("/");
  } else {
    res.redirect("/login");
  }
});

app.get("/admin", requireLogin, (req, res) => {
  if (req.session.user.username === "admin") {
    res.sendFile(__dirname + "/public/admin.html");
  } else {
    res.status(403).send("Access forbidden");
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
