const sinon = require('sinon');
const {expect} = require('chai');
const Utils = require("./utils");
const sendPaymentRequestToApi = require("./3-payment");

describe("sendPaymentRequestToApi", function() {
  it("should verify spy is working", function () {
    const spy = sinon.spy(Utils, "calculateNumber");

    sendPaymentRequestToApi(100, 20);

    expect(spy.calledOnce).to.equal(true);
    expect(spy.calledWith("SUM", 100, 20)).to.equal(true);

    spy.restore();
  })
});