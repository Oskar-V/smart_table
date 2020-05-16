const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const app = express();
const port = 80;
const outputFilePath = "/home/pi/widgets/json.json";

app.use(bodyParser.json());

let cache = {};
let cacheIndex = 1;

app.get('/', (req, res) => res.send('Only post request accepted'));
app.post('/', (req, res) => {
        cache[cacheIndex] = req.body
        cacheIndex += 1;
        //console.log(cache);
        res.send(req.body);    // echo the result back
});

setInterval(() => {
        getFileContent(outputFilePath);
        fs.writeFile(outputFilePath, JSON.stringify(cache), 'utf-8', function(err) {
                if(err) {
                        console.log(err)
                        return err
                } else {
                        cache = {};
                        cacheIndex = 1;
                }
        })
},5000);


function getFileContent(filePath) {
        fs.readFile(filePath, 'utf-8', function(err, fileContents) {
                if (err) throw err;
                //console.log(fileContents);
        });
}

app.listen(port, () => console.log(`App handler listening on: "http://localhost:${port}`));
