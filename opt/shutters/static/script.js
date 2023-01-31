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
    const response = await fetch('/open-time')
    data = await response.json();
    document.getElementById('appt').value = data['data'][0];
    document.getElementById('appa').value = data['data'][1];
}

async function getAction(selectObject) {
    var action = selectObject.value;
    var datetime = document.getElementById('appt').value;

    var value = {"datetime": datetime, "action": action}

    const response = await fetch('/open-time', {method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify(value)});
    data = await response.json();
    document.getElementById('appt').value = data['data'][0];
    document.getElementById('appa').value = data['data'][1];
    console.log(value);
  }