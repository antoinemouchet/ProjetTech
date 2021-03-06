let friends = {};

/**
 * Create new row node. 
 * @param {String} pictureLink, link to the show's picture. 
 * @param {String} showName, name of the show.
 */
function C_rowShows(pictureLink, showName) {
    let row = document.createElement('tr');
    // Elements
    let col = document.createElement('td');

    // Picture
    let picture = document.createElement('img');
    picture.src = '/' + pictureLink;
    picture.style.maxWidth = "128px";
    picture.style.maxHeight = "128px";
    col.appendChild(picture);

    // Name
    let Name = document.createElement('p');
    let nametxt = document.createTextNode(showName);
    Name.appendChild(nametxt);
    col.appendChild(Name);

    row.appendChild(col);

    return row;
}

/**
 * Populate the corresponding table body with the watch list of the corresponding user.
 * @param {Number} userId, user's id.
 * @param {String} tbodyId, HMTL id of the table body to populate. 
 */
async function C_populateTable(userId, tbodyId) {
    let json = await fetchData(userId);
    if (json.error) {
        alert(json.error);
        return;
    }
    let tbody = document.getElementById(tbodyId);
    tbody.innerHTML = null;
    for (let show of json.data) {
        tbody.appendChild(C_rowShows(show.img, show.name));
    }
}

/**
 * Populate table of the given type.
 * @param {String} type, used to get the corresponding elements. For the type "friend", will get elements with "friend_id" and "friend_table" HTML ids. 
 */
async function friend_populateTable(type) {
    let friendId = friends[document.getElementById(type + '_id').value];
    if (friendId)
        C_populateTable(friendId, type + '_table');

}

/**
 * Fetch Watch list data for the given user id.
 * @param {Number} userId 
 */
async function fetchData(userId) {

    let data = await fetch('http://localhost:5000/list/' + userId, {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    return await data.json();
}

/**
 * Fetch current user's friend list and populate the friends dictionary.
 */
async function fetchFriends() {

    let data = await fetch('http://localhost:5000/friends/' + user_id, {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    let friends_data = await data.json();
    for (let friend of friends_data.friends) {
        friends[friend.pseudo] = friend.id;
    }
}

window.onload = function () {
    fetchFriends();
    C_populateTable(user_id, 'me_table');
};
