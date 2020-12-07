
let changes = { add: [], delete: [] }
let compareMode = false;
let shows = {};
let statusFormats = {0 : ["To see", "btn btn-danger"], 1 : ["In progress", "btn btn-warning"], 2 : ["Seen", "btn btn-success"]}
let users = {};

/**
 * Create an HTML button with a specified text.
 * @param {String} value Text of the button.
 */
function createButton(value) {
    let button = document.createElement('input');
    button.type = 'button';
    button.value = value;
    return button;
}

/**
 * Delete a show by adding them as a delete change.
 * @param {Number} showId Id of show to delete.
 */
function deleteShow(showId) {
    changes.delete.push(showId);
    sendChanges();
}

/**
 * Add a show by adding the value of input entry as an add change.
 */
function addShow() {
    let showName = document.getElementById('addShowId').value;
    let showId = shows[showName];
    if (showId) {
        // Get real id from name
        changes.add.push(showId);
        sendChanges();
    }
}

async function createAndJoinWatchParty(showId) {
    // Create a watch party
    let data = await fetch('http://localhost:5000/session/' + showId, {
        method: "POST",
        mode: "cors",
    });

    // Retrieve watch party id
    let id = (await data.json())['id'];

    // Join watch party
    location.href = "http://localhost:5000/watch/" + id;
}

/**
 * Create new show row
 * @param {*} pictureLink, show's picture
 * @param {*} showName 
 * @param {*} showTag, show's tags
 * @param {*} showId, show's id
 */
function rowShow(pictureLink, showName, showTag, showId) {
    let row = document.createElement('tr');

    // Image of current show
    let logo = document.createElement('td');
    let picture = document.createElement('img');
    picture.src = '/' + pictureLink;
    picture.width = 128;
    logo.appendChild(picture);

    // Information of current show
    let name = document.createElement('td');
    let tags = document.createElement('td');

    // Actions
    let actions = document.createElement('td');

    // Create a watch party
    let showLink = document.createElement('a');
    // showLink.href = '/session/' + showId;
    showLink.href = '#';
    showLink.onclick = () => {
        createAndJoinWatchParty(showId);
    }

    let nameTxt = document.createTextNode(showName);
    showLink.appendChild(nameTxt);
    name.appendChild(showLink);

    // Tags
    let tagsDiv = document.createElement('div');
    let tagNames = showTag.split(';');
    tagNames.sort();

    for (tagName of tagNames) {
        if(tagName.trim() != ""){
            let tagBlock = document.createElement('button');
            tagBlock.type = "button";
            tagBlock.className = "btn btn-secondary btn-sm";
            tagBlock.innerText = tagName ;
            tagBlock.style.margin = "1px";
            tagBlock.style.textTransform = "capitalize";
            tagsDiv.appendChild(tagBlock);
        }
    }

    tags.appendChild(tagsDiv);

    let deleteButton = createButton('Remove');
    deleteButton.className = "btn btn-danger";
    deleteButton.onclick = function () { deleteShow(showId) };
    actions.appendChild(deleteButton);

    row.appendChild(logo);
    row.appendChild(name);
    row.appendChild(tags);
    row.appendChild(actions);

    return row;
}

/**
 * Populate watch list table with its shows.
 * @param {Array} list 
 */
function populateTable(list) {
    let tbody = document.getElementById('tshows');
    tbody.innerHTML = null;
    for (let show of list) {
        tbody.appendChild(rowShow(show.img, show.name, show.tags, show.id));
    }
}

/**
 * Modify the status of the watch list (Client side only)
 * @param {Number} status, id
 */
function changeStatus(status) {
    let statusButton = document.getElementById('status');
    statusButton.status = status;
    let statusFormat = statusFormats[status];
    statusButton.value = statusFormat[0];
    statusButton.className = statusFormat[1];
}

/**
 * Fetch data from backend and parse it.
 */
async function getData() {
    let watchListId = users[document.getElementById('watchId').value];
    if (watchListId >= 0) {
        let json = await fetchData(watchListId);
        if (json.error) {
            alert(json.error);
            return;
        }
        // Draw table
        populateTable(json.data);
        // Update status button
        changeStatus(json.status);
    }
}

/**
 * Tick the backend to force creation of a watch list.
 */
async function createWatchList() {
    let watchListId = users[document.getElementById('watchId').value];
    if (watchListId >= 0) {
        await fetch('http://localhost:5000/list/', {
            method: "POST",
            mode: "cors",
        });
    }
}

/**
 * Send changes in watchlist's shows and status
 */
async function sendChanges() {
    let watchListId = users[document.getElementById('watchId').value];
    if (watchListId >= 0 && Object.keys(changes).length > 0) {
        await fetch('http://localhost:5000/list/' + watchListId, {
            method: "POST",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(changes),
        });
        changes = { add: [], delete: [], status: -1 }; //reset changes
        getData();

    }
}

/**
 * Change and send new status.
 */
async function sendStatus() {
    let statusButton = document.getElementById('status');
    let status = statusButton.status;
    changes.status = (status+1) % 3;
    sendChanges();
}

/**
 * Fetch watch list data.
 * @param {Number} watchListId 
 */
async function fetchData(watchListId) {

    let data = await fetch('http://localhost:5000/list/' + watchListId, {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    return await data.json();
}

/**
 * Fetch all shows and populate the shows dictionary.
 */
async function fetchShows() {

    let data = await fetch('http://localhost:5000/shows/', {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    let shows_data = await data.json();
    for (let show of shows_data) {
        shows[show.name] = show.id;
    }


}

/**
 * Fetch all users and populate the users dictionary.
 */
async function fetchUsers() {

    let data = await fetch('http://localhost:5000/users', {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    let usersData = await data.json();
    for (let user of usersData) {
        users[user.pseudo] = user.id;
    }
    document.getElementById('watchId').value = user_name;
    getData();

}

window.onload = function () {
    fetchUsers();  
    fetchShows();
};
