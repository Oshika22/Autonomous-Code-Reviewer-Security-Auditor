// target_code.js
function processData(input) {
    // Dangerous parsing
    const data = JSON.parse(input);
    console.log(data);
}

function connect() {
    // Another potential risk
    const secret_key = "12345-ABCDE"; 
    console.log("Connected with key...");
}