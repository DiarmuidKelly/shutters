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
    await updateView();
}

async function updateView(){
    const response = await fetch('/next-event')
    data = await response.json();
    document.getElementById('appt').value = data['data'][0];
    document.getElementById('appa').value = data['data'][1];
}

function updateEvent(){    
    var data = {
        type: document.getElementById('appa').value,
        time: document.getElementById('appt').value
    };

    var json = JSON.stringify(data);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/set-event");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(json);

    updateView();
}