let state = {
    "time": 0,
    "state": "paused"
};

let firstTime = true;
let userModified = false;

/**
 * Apply state on video.
 */
function update() {
    let video = document.getElementById("main-video");
    if (state.time - 500.0 / 60.0 > video.currentTime || state.time + 500.0 / 60.0 < video.currentTime) {
        video.currentTime = state.time;
    }
    if (state.state == "paused") {
        video.pause();
    } else {
        video.play();
    }
}

/**
 * Pause video.
 */
function pause() {
    state.state = "paused";
    userModified = true;
    update();
}

/**
 * Play video.
 */
function play() {
    state.state = "played";
    userModified = true;
    update();
}

/**
 * Change current time of video.
 */
function jumpTo(time) {
    state.time += time;
    if (state.time < 0) {
        state.time = 0;
    }
    userModified = true;
    update();
}

/**
 * Sync video state with server.
 */
async function sync() {
    let video = document.getElementById("main-video");
    // We aren't a viewer yet
    // Time to be up-to-date
    // And to not push our state
    // (which is default state)
    if (firstTime) {
        firstTime = false;
        let data = await fetch('http://localhost:5000/session/' + watchPartyTag, {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
        });
        let json = await data.json();
        console.log(json);
        state = json;
        setInterval(() => {
            sync();
        }, 500);
    } else {
        // Get state first
        // If current state is different than mine
        // Just apply it
        let data = await fetch('http://localhost:5000/session/' + watchPartyTag, {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
        });
        let json = await data.json();
        let changed = false;
        if (video.currentTime - 500.0 / 60.0 > json["time"] || video.currentTime + 500.0 / 60.0 < json["time"]) {
            state.time = video.currentTime;
            changed = true;
        }
        if (state.state != json["state"]) {
            state.time = video.currentTime;
            changed = true;
        }
        // If remote state changed
        // AND IF user do not make a  change
        if (changed && !userModified) {
            state = json;
            update();
            // End function 
            return;
        } else {
            // Okay we can safely
            // push our state
            fetch('http://localhost:5000/session/' + watchPartyTag + '/', {
                method: "PATCH",
                mode: "cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(state)
            });
            console.log(JSON.stringify(state));
            userModified = false;
        }
    }
    update();
}

/**
 * Launch player when page is loaded
 */
window.onload = () => {
    sync();
}