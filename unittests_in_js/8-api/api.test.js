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
});