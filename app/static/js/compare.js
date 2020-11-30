let friends = {};

function C_rowShows(pictureLink, showName)
{
    let row = document.createElement('tr');
    //elements
    let col = document.createElement('td');
   
    
    //picture
    let picture = document.createElement('img');
    picture.src = pictureLink;
    col.appendChild(picture);

    //name
    let Name = document.createElement('p');
    let nametxt = document.createTextNode(showName);
    Name.appendChild(nametxt);
    col.appendChild(Name);



    row.appendChild(col);

    return row;
}


async function C_populateTable(userId, tbodyId)
{   
    let json = await fetchData(userId);
    if(json.error)
    {
            alert(json.error);
            return;
    }
    let tbody = document.getElementById(tbodyId);
    tbody.innerHTML = null;
    for(let show of json.data)
    {
        tbody.appendChild(C_rowShows(show.img, show.name));
    }
}

async function friend_populateTable(type)
{
    let friendId = friends[document.getElementById(type+'_id').value];
    if(friendId)
        C_populateTable(friendId, type+'_table');

}

async function fetchData(userId) {
  
    let data = await fetch('http://localhost:5000/list/' + userId, {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
    });
    return await data.json();
}

async function fetchFriends() {
  
    let data = await fetch('http://localhost:5000/friends/'+ user_id, {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
    });
    let friends_data = await data.json();
    for(let friend of friends_data.friends)
    {
        friends[friend.pseudo.toLowerCase()] = friend.id;
    }

    
}

window.onload = function(){
    fetchFriends();
    C_populateTable(user_id, 'me_table');  
};