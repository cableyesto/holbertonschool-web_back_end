const { expect } = require('chai');
const request = require('request');

describe("Index page", function() {
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