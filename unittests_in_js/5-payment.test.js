const sinon = require('sinon');
const {expect} = require('chai');
const Utils = require("./utils");
const sendPaymentRequestToApi = require("./3-payment");

describe("Hooks test", function() {
  let logSpy;
  beforeEach(function () {
    logSpy = sinon.spy(console, "log");
  });
  afterEach(function () {
    logSpy.restore();
  });
  it("Verification SUM 100 20", function () {
    sendPaymentRequestToApi(100, 20);

    expect(logSpy.calledWith("The total is: 120")).to.equal(true);
    expect(logSpy.calledOnce).to.equal(true);
  });
  it("Verification SUM 10 10", function () {
    sendPaymentRequestToApi(10, 10);

    expect(logSpy.calledWith("The total is: 20")).to.equal(true);
    expect(logSpy.calledOnce).to.equal(true);
  });
});