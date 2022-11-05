const sleep = ms => new Promise(res => setTimeout(res, ms));

async function stop() {
    console.log("Stopping");
    const response = await fetch('/stop');
}
async function down() {
    console.log("going down");
    const response = await fetch('/down');
}
async function up() {
    console.log("going up");
    const response = await fetch('/up');
}
async function full_down() {
    down();
    await sleep(30000);
    stop();
}
async function full_up() {
    up();
    await sleep(35000);
    stop();
}
async function custom_down() {
    console.log("going down");
    const response = await fetch('/down');
    await sleep(18000);
    stop();
}

window.onload = async function () {
    const response = await fetch('/open-time');
    console.log(response);
    document.getElementById('appt').value = '08:00';
}
