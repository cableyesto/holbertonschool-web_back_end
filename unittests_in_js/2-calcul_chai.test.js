const { expect } = require('chai');
const calculateNumber = require("./2-calcul_chai");

describe("calculateNumber", function () {
  it("should return sum", function () {
    expect(calculateNumber('SUM', 1.4, 4.5)).to.equal(6);
  });
  it("should return subtraction", function () {
    expect(calculateNumber('SUBTRACT', 1.4, 4.5)).to.equal(-4);
  });
  it("should return division", function () {
    expect(calculateNumber('DIVIDE', 1.4, 4.5)).to.equal(0.2);
  });
  it("should return Error string for argument 0", function () {
    expect(calculateNumber('DIVIDE', 1.4, 0)).to.equal('Error');
  });
});