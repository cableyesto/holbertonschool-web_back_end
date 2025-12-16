/*
Cannot use ES6 import with mocha and node v12.x
Remove "type": "module" in package.json
*/
const mocha = require('mocha');
const assert = require("assert");
const kue = require("kue");
const createPushNotificationsJobs = require("./8-job");
// import createPushNotificationsJobs from "./8-job";


mocha.describe("createPushNotificationsJobs", function () {
    let queue = kue.createQueue();

    mocha.before(function() {
        queue.testMode.enter();
    });

    mocha.afterEach(function() {
        queue.testMode.clear();
    });

    mocha.after(function() {
        queue.testMode.exit()
    });

    mocha.it("display a error message if jobs is not an array", function () {
        assert.throws(() => createPushNotificationsJobs('bob', queue),
            Error("Jobs is not an array")
        );
    });

    mocha.it("create two new jobs to the queue", function () {
        const jobsList = [
            {
                phoneNumber: '4153518780',
                message: 'This is the code 1234 to verify your account'
            },
            {
                phoneNumber: '4153518781',
                message: 'This is the code 5678 to verify your account'
            }
        ];

        createPushNotificationsJobs(jobsList, queue);

        assert.strictEqual(queue.testMode.jobs.length, 2);

        assert.strictEqual(queue.testMode.jobs[0].type, "push_notification_code_3");
        assert.strictEqual(queue.testMode.jobs[1].type, "push_notification_code_3");
    });

    mocha.it("should verify the data of each jobs", function () {
        const jobsList = [
            {
                phoneNumber: '4153518780',
                message: 'This is the code 1234 to verify your account'
            },
            {
                phoneNumber: '4153518781',
                message: 'This is the code 5678 to verify your account'
            }
        ];

        createPushNotificationsJobs(jobsList, queue);

        assert.strictEqual(queue.testMode.jobs[0].data.phoneNumber, "4153518780");
        assert.strictEqual(queue.testMode.jobs[0].data.message,
            "This is the code 1234 to verify your account");
        assert.strictEqual(queue.testMode.jobs[1].data.phoneNumber, "4153518781");
        assert.strictEqual(queue.testMode.jobs[1].data.message,
            "This is the code 5678 to verify your account");
    });
});