import { createQueue } from "kue";

const queue = createQueue();

let objectJob = {
    phoneNumber: "4153518780",
    message: "This is the code to verify your account"
};

const job = queue.create("push_notification_code", objectJob).save(function(err) {
    if( !err ) {
        console.log(`Notification job created: ${job.id}`);
    }
});

job.on('complete', function() {
    console.log("Notification job completed");
}).on('failed attempt', function() {
    // remaining attempts
    console.log("Notification job failed");
}).on('failed', function() {
    // no remaining attempts
    console.log("Notification job failed");
});