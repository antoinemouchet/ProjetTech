let users = {};

function rowShow(pictureLink, showName, showPath, showTag)
{
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
    showLink.href = showPath;
    let nametxt = document.createTextNode(showName);
    showLink.appendChild(nametxt);
    name.appendChild(showLink);

    //tags
    let tags_div = document.createElement('div');
    let tag_names = showTag.split(';');
    for(tag_name of tag_names)
    {
        let tag_block = document.createElement('p');
        let tag_txt = document.createTextNode(tag_name);
        tag_block.appendChild(tag_txt);
        tags_div.appendChild(tag_block);
    }
    tags.appendChild(tags_div);

    row.appendChild(logo);
    row.appendChild(name);
    row.appendChild(tags);

    return row;
}

function populateTable(list)
{
    let tbody = document.getElementById('tshows');
    tbody.innerHTML = null;
    for(let show of Object.values(list))
    {
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

async function fetch_and_populate(userId) {
    let recommendations = await fetchRecommendations(userId);
    if(recommendations.error) {
        alert(recommendations.error);
    }
    else {
        populateTable(recommendations.recommendations);      
    }
}

async function populate_by_username() {
    let user = users[document.getElementById('username').value.toLowerCase()];
    if(user)
        await fetch_and_populate(user);
    else
        alert('user not exist');
}

async function fetchUsers() {
  
    let data = await fetch('http://localhost:5000/users', {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
    });
    let users_data = await data.json();
    for(let user of users_data)
    {
        users[user.pseudo.toLowerCase()] = user.id;
    }

    
}


window.onload = function(){
    fetchUsers();
    fetch_and_populate(user_id);
};