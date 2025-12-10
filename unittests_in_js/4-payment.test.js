const sinon = require('sinon');
const {expect} = require('chai');
const Utils = require("./utils");
const sendPaymentRequestToApi = require("./3-payment");

describe("sendPaymentRequestToApi", function() {
  it("should verify stub is working", function () {
    const stub = sinon.stub(Utils, "calculateNumber");
    const logSpy = sinon.spy(console, "log");

    stub.returns(10);
    sendPaymentRequestToApi(100, 20);

    expect(stub.calledOnce).to.equal(true);
    expect(stub.calledWith("SUM", 100, 20)).to.equal(true);

    expect(logSpy.calledOnce).to.equal(true);
    expect(logSpy.calledWith("The total is: 10")).to.equal(true);

    stub.restore();
    logSpy.restore();
  })
});