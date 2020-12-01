let users = {};

window.onload = function () {
    fetchUsers();
    fetchAndPopulate(userId);
};

function rowShow(pictureLink, showName, showPath, showTag) {
    let row = document.createElement('tr');
    //elements
    let logo = document.createElement('td');
    let name = document.createElement('td');
    let tags = document.createElement('td');
    let seen = document.createElement('td');
    //actions
    let actions = document.createElement('td');

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

function populateTable(list) {
    let tbody = document.getElementById('tshows');
    tbody.innerHTML = null;
    for (let show of Object.values(list)) {
        tbody.appendChild(rowShow(show.img, show.name, show.video, show.tags));
    }
}

async function fetchRecommendations(userId) {

    let data = await fetch('http://localhost:5000/recommendations/' + userId, {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    return await data.json();
}

async function fetchAndPopulate(userId) {
    let recommendations = await fetchRecommendations(userId);
    if (recommendations.error) {
        alert(recommendations.error);
    }
    else {
        populateTable(recommendations.recommendations);
    }
}

async function populateByUsername() {
    let user = users[document.getElementById('username').value.toLowerCase()];
    if (user)
        await fetchAndPopulate(user);
    else
        alert('user not exist');
}

async function fetchUsers() {

    let data = await fetch('http://localhost:5000/users', {
        method: "GET",
        mode: "cors",
        headers: { "Content-Type": "application/json" },
    });
    let usersData = await data.json();
    for (let user of usersData) {
        users[user.pseudo.toLowerCase()] = user.id;
    }


}