import { createQueue } from "kue";

let blackList = [
    "4153518780",
    "4153518781"
];

function sendNotification(phoneNumber, message, job, done) {
    job.progress(0, 100);
    if (blackList.includes(phoneNumber)) {
        return done(new Error(`Phone number ${phoneNumber} is blacklisted`));
    }
    job.progress(50, 100);
    console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    // allow another job to start
    setTimeout(() => {
        job.progress(100, 100);
        done();
    }, 500);
}

const queue = createQueue();

queue.process("push_notification_code_2", 2, function(job, done) {
    try {
        sendNotification(job.data.phoneNumber, job.data.message, job, done);
    } catch (err) {
        done(err);
    }
});