function createPushNotificationsJobs(jobs, queue) {
    if (jobs.constructor !== Array) {
        throw new Error("Jobs is not an array");
    }

    jobs.forEach((jobData) => {
        const job = queue.create("push_notification_code_3", jobData);

        job.save(function(err) {
            if( !err ) {
                console.log(`Notification job created: ${job.id}`);
            }
        });

        job.on('complete', function() {
            console.log(`Notification job ${job.id} completed`);
        }).on('failed attempt', function(error) {
            // remaining attempts
            console.log(`Notification job ${job.id} failed: ${error}`);
        }).on('failed', function(error) {
            // no remaining attempts
            console.log(`Notification job ${job.id} failed: ${error}`);
        }).on('progress', function(progress) {
            if (progress !== 100) {
                console.log(`Notification job ${job.id} ${progress}% complete`);
            }
        });
    });
}
// CommonJS is used for node v12.x
module.exports = createPushNotificationsJobs;