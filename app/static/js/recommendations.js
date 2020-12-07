let users = {};

window.onload = function () {
    fetchUsers();
    fetchAndPopulate(user_id);
};

/**
 * Create new show row.
 * @param {String} pictureLink, show's picture
 * @param {String} showName 
 * @param {String} showPath, show's url
 * @param {String} showTag, show's tags 
 */
function rowShow(pictureLink, showName, showPath, showTag) {
    let row = document.createElement('tr');
    //elements
    let logo = document.createElement('td');
    let name = document.createElement('td');
    let tags = document.createElement('td');

    let picture = document.createElement('img');
    picture.src = '/' + pictureLink;
    picture.width = 128;
    logo.appendChild(picture);

    let showLink = document.createElement('a');
    showLink.href = '/' + showPath;
    let nametxt = document.createTextNode(showName);
    showLink.appendChild(nametxt);
    name.appendChild(showLink);

    //tags
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

    row.appendChild(logo);
    row.appendChild(name);
    row.appendChild(tags);

    return row;
}

/**
 * Populate recommendations table with recommended shows.
 * @param {Array} list, list of recommended shows. 
 */
function populateTable(list) {
    let tbody = document.getElementById('tshows');
    tbody.innerHTML = null;
    for (let show of Object.values(list)) {
        tbody.appendChild(rowShow(show.img, show.name, show.video, show.tags));
    }
}

/**
 * Fetch recommendations for the given user id
 * @param {Number} userId 
 */
async function fetchRecommendations(userId) {

    let data = await fetch('http://localhost:5000/recommendations/' + userId, {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    return await data.json();
}

/**
 * Fetch recommendations and populate the recommendations table for the given user id if exist.
 * @param {Number} userId 
 */
async function fetchAndPopulate(userId) {
    let recommendations = await fetchRecommendations(userId);
    if (recommendations.error) {
        alert(recommendations.error);
    }
    else {
        populateTable(recommendations.recommendations);
    }
}

/**
 * Fetch all users and populate the users dictionary
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


}
