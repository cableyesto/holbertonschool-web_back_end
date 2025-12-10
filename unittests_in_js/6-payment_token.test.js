const { expect } = require('chai');
const getPaymentTokenFromAPI = require("./6-payment_token");

describe("getPaymentTokenFromAPI", function () {
  it("should correctly resolve the promises", function (done) {
    let res = getPaymentTokenFromAPI(true)
    
    res.then((obj) => {
      console.log(obj);
      expect(obj).to.deep.equal({data: 'Successful response from the API' });
      done();
    });
  });
});