const express = require("express");
const multer = require("multer");
const path = require("path");
const { exec } = require("child_process");
const fs = require("fs");

const app = express();
const PORT = 3000;

app.set("view engine","ejs");
app.use(express.static("public"));  //to store all image,css,js in public folder
app.use('/output', express.static('output'));   //to store output files

const upload = multer({ storage: multer.diskStorage({
    destination: (req, file, cb) => {
      if (file.fieldname === 'knownImages') cb(null, 'uploads/known');
      else if (file.fieldname === 'mixedImages') cb(null, 'uploads/mixed');
    },
    filename: (req, file, cb) => cb(null, file.originalname)
  })});

  
const knownStorage = multer.diskStorage({
    destination: "uploads/known",
    filename: (req,file,cb) => cb(null, file.originalname),
});

const mixedStorage = multer.diskStorage({
    destination: "uploads/mixed",
    filename: (req, file, cb) => cb(null, file.originalname),
});

const knownUpload = multer({ storage: knownStorage});
const mixedUpload = multer({ storage: mixedStorage});

app.get("/",(req,res) => {
    res.render("index");
})

const clearFolder = (folderPath) => {
  fs.readdir(folderPath, (err, files) => {
    if (err) throw err;
    for (const file of files) {
      fs.unlink(path.join(folderPath, file), err => {
        if (err) throw err;
      });
    }
  });
};

app.post("/upload", (req, res, next) => {
  clearFolder('uploads/known');
  clearFolder('uploads/mixed');
  clearFolder('output');
  next();
}, upload.fields([
  { name: 'knownImages', maxCount: 10 },
  { name: 'mixedImages', maxCount: 20 }
]), (req, res) => {
  exec("python process_faces.py", (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).send("Error during processing");
    }
    const outputFiles = fs.readdirSync("output");
    res.render("result", { images: outputFiles });
  });
});


  

app.listen(PORT, () => console.log(`Server sending on localhost : ${PORT}`));