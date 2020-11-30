
let changes = { add: [], delete: [] }
let compareMode = false;
let shows = {};

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

function rowShow(pictureLink, showName, showPath, showTag, showId) {
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
    let seen = document.createElement('td');

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
    for (let tagName of tagNames) {
        if (tagName != "") {
            let tagBlock = document.createElement('p');
            let tagTxt = document.createTextNode(tagName);
            tagBlock.appendChild(tagTxt);
            tagsDiv.appendChild(tagBlock);
        }
    }
    tags.appendChild(tagsDiv);

    // Seen
    let modifySeen = document.createElement('a');
    seen.appendChild(modifySeen);

    let deleteButton = createButton('remove');
    deleteButton.onclick = function () { deleteShow(showId) };
    actions.appendChild(deleteButton);

    row.appendChild(logo);
    row.appendChild(name);
    row.appendChild(tags);
    row.appendChild(seen);
    row.appendChild(actions);

    return row;
}

function populateTable(list) {
    let tbody = document.getElementById('tshows');
    tbody.innerHTML = null;
    for (let show of list) {
        tbody.appendChild(rowShow(show.img, show.name, show.video, show.tags, show.id));
    }
}

/**
 * Fetch data from backend and parse it.
 */
async function getData() {
    let watchListId = document.getElementById('watchId').value;
    if (watchListId >= 0) {
        let json = await fetchData(watchListId);
        if (json.error) {
            alert(json.error);
            return;
        }
        // Draw table
        populateTable(json.data);

        if (document.getElementById('addShowId') == undefined) {
            let displayData = document.getElementById('displayData');
            let InputShowID = document.createElement('input');
            InputShowID.type = 'text';
            InputShowID.min = 0;
            InputShowID.id = 'addShowId';
            let addIdButton = createButton('Add Show');
            addIdButton.onclick = function () { addShow() };
            displayData.appendChild(InputShowID);
            displayData.appendChild(addIdButton);
        }

    }
}

/**
 * Tick the backend to force creation of a watch list.
 */
async function createWatchList() {
    let watchListId = document.getElementById('watchId').value;
    if (watchListId >= 0) {
        await fetch('http://localhost:5000/list/', {
            method: "POST",
            mode: "cors",
        });

        if (document.getElementById('addShowId') == undefined) {
            let displayData = document.getElementById('displayData');
            let InputShowID = document.createElement('input');
            InputShowID.type = 'text';
            InputShowID.min = 0;
            InputShowID.id = 'addShowId';
            let addIdButton = createButton('Add Show');
            addIdButton.onclick = function () { addRow() };
            displayData.appendChild(InputShowID);
            displayData.appendChild(addIdButton);
        }

    }
}

async function sendChanges() {
    let watchListId = document.getElementById('watchId').value;
    if (watchListId >= 0 && Object.keys(changes).length > 0) {
        await fetch('http://localhost:5000/list/' + watchListId, {
            method: "POST",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(changes),
        });
        changes = { add: [], delete: [] }; //reset changes
        getData();

    }
}

async function fetchData(watchListId) {

    let data = await fetch('http://localhost:5000/list/' + watchListId, {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    return await data.json();
}


async function fetchShows() {

    let data = await fetch('http://localhost:5000/shows/', {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    let shows_data = await data.json();
    for (let show of shows_data) {
        shows[show.name.toLowerCase()] = show.id;
    }


}


window.onload = function () {
    document.getElementById('watchId').value = user_id;
    getData();
    fetchShows();

};







