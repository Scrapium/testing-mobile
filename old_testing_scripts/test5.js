const uuid = require('uuid');
const queryParameters = {
}
const oauth_timestamp = Math.floor(Date.now() / 1000);
const oauth_nonce = uuid.v1(); 
const parameters = {
      ...queryParameters,
      oauth_consumer_key:"3rJOl1ODzm9yZy63FACdg",
      oauth_signature_method:"HMAC-SHA1",
      oauth_timestamp: oauth_timestamp,
      oauth_nonce: oauth_nonce,
      oauth_version:"1.0"
}

let ordered = {};
Object.keys(parameters).sort().forEach(function(key) {
    ordered[key] = parameters[key];
});
let encodedParameters = '';
for (k in ordered) {
  const encodedValue = escape(ordered[k]);
  const encodedKey = encodeURIComponent(k);
  if(encodedParameters === ''){
     encodedParameters +=     encodeURIComponent(`${encodedKey}=${encodedValue}`)
  }
  else{
   encodedParameters += encodeURIComponent(`&${encodedKey}=${encodedValue}`);
  }
}
console.log(encodedParameters);

const method = 'GET';
const base_url = 'https://schoolwebsite.org/campus/oneroster/schoolName/learningdata/v1/schools';
const encodedUrl = encodeURIComponent(base_url);
encodedParameters = encodeURIComponent(encodedParameters); // encodedParameters which we generated in last step.
const signature_base_string = `${method}&${encodedUrl}&${encodedParameters}`
console.log(signature_base_string)

const secret_key = `5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8`;
const token_secret = `Zh3X7LqjofGnmn3QoTqbcdAOjrIFDob0`;
const signing_key = `${secret_key}&${token_secret}`; //as token is missing in our case.

const crypto = require('crypto');
const oauth_signature = crypto.createHmac("sha1", signing_key).update(signature_base_string).digest().toString('base64');
console.log(oauth_signature);

const encoded_oauth_signature = encodeURIComponent(oauth_signature);
console.log(encoded_oauth_signature);
