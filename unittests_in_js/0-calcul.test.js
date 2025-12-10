const assert = require("assert");
const calculateNumber = require("./0-calcul");

describe("calculateNumber", function () {
  it("should return integer for integer arguments", function () {
    assert.strictEqual(calculateNumber(1, 3), 4);
  });
  it("should return integer for float on second argument", function () {
    assert.strictEqual(calculateNumber(1, 3.7), 5);
  });
  it("should return integer for float on both arguments", function () {
    assert.strictEqual(calculateNumber(1.2, 3.7), 5);
  });
  it("should return integer for float on both arguments", function () {
    assert.strictEqual(calculateNumber(1.5, 3.7), 6);
  });
});