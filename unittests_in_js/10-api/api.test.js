const { expect } = require('chai');
const request = require('request');

describe("Index page", function() {
  let options;
  beforeEach(function () {
    options = {
      uri: "http://127.0.0.1:7865",
      method: "GET"
    };
  });
  it("should return status code 200 for `GET /`", function() {
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(200);
    });
  });
  it("should return correct body for `GET /`", function() {
    request(options, function(error, response, body) {
      expect(body).to.equal("Welcome to the payment system");
    });
  });
  it("should return status code 404 for `POST /`", function() {
    const options_post = {
      uri: "http://127.0.0.1:7865",
      method: "POST"
    };
    request(options_post, function(error, response, body) {
      expect(response.statusCode).to.equal(404);
    });
  });
})

describe("Cart page", function() {
  let options;
  beforeEach(function () {
    options = {
      uri: "http://127.0.0.1:7865/cart/",
      method: "GET"
    };
  });
  it("should return status code 200 for `GET /cart/1`", function() {
    options.uri += '1';
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(200);
    });
  });
  it("should return status code 200 for `GET /cart/255`", function() {
    options.uri += '255';
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(200);
    });
  });
  it("should return correct body for `GET /cart/1`", function() {
    const num = 1;
    options.uri += String(num);
    request(options, function(error, response, body) {
      expect(body).to.equal(`Payment methods for cart ${num}`);
    });
  });
  it("should return status code 404 for `GET /cart/hello`", function() {
    options.uri += 'hello';
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(404);
    });
  });
  it("should return status code 404 for `POST /cart/hello`", function() {
    const options_post = {
      uri: "http://127.0.0.1:7865/cart/10",
      method: "POST"
    };
    request(options_post, function(error, response, body) {
      expect(response.statusCode).to.equal(404);
    });
  });
});

describe("Available payments page", function() {
  let options;
  beforeEach(function () {
    options = {
      uri: "http://127.0.0.1:7865/available_payments",
      method: "GET"
    };
  });
  it("should return status code 200 for `GET /available_payments`", function() {
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(200);
    });
  });
  it("should return status code 404 for `GET /available_payments/test`", function() {
    options.uri += '/test';
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(404);
    });
  });
  it("should return correct body for `GET /available_payments`", function() {
    const expectedObj = {
      payment_methods: {
        credit_cards: true,
        paypal: false
      }
    };
    request(options, function(error, response, body) {
      expect(JSON.parse(body)).to.deep.equal(expectedObj);
    });
  });
  it("should return status code 404 for `POST /available_payments`", function() {
    options.method = "POST";
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(404);
    });
  });
});


describe("Login page", function() {
  let options;
  beforeEach(function () {
    options = {
      uri: "http://127.0.0.1:7865/login",
      method: "POST",
      json: true,
      body: {"userName": "Betty"}
    };
  });
  it("should return status code 200 for `POST /login` and body object with userName key", function() {
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(200);
    });
  });
  it("should return correct body for `POST /login` and body object with userName key", function() {
    request(options, function(error, response, body) {
      expect(body).to.equal("Welcome Betty");
    });
  });
  it("should return status code 404 for `POST /login` and body object without userName key", function() {
    options.body = {"bob": "name"};
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(404);
    });
  });
  it("should return status code 404 for `POST /login` and without body", function() {
    delete options.body;
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(404);
    });
  });
  it("should return status code 404 for `GET /login` and without body", function() {
    delete options.body;
    options.method = "GET";
    request(options, function(error, response, body) {
      expect(response.statusCode).to.equal(404);
    });
  });
});