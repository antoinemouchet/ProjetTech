
let changes = {add : [],  delete : []}
let compareMode = false;
let Shows = {};

function createButton(value)
{
	let button = document.createElement('input');
	button.type = 'button';
	button.value = value;
	return button;
}

function deleteRow(showId)
{
    changes.delete.push(showId);
    sendChanges();
}


function addRow()
{
    let show_name = document.getElementById('addShowId').value;
    let show_id = Shows[show_name];
    if(show_id){
        changes.add.push(show_id);
        sendChanges();

    }
}



function rowShow(pictureLink, showName, showPath, showTag, showId)
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


    // TODO: here to create watch party
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

    //seen
    let modifySeen = document.createElement('a');
    seen.appendChild(modifySeen);

    let deleteButton = createButton('remove');
    deleteButton.onclick = function(){deleteRow(showId)};
    actions.appendChild(deleteButton);

    row.appendChild(logo);
    row.appendChild(name);
    row.appendChild(tags);
    row.appendChild(seen);
    row.appendChild(actions);

    return row;
}

function populateTable(list)
{
    let tbody = document.getElementById('tshows');
    tbody.innerHTML = null;
    for(let show of list)
    {
        tbody.appendChild(rowShow(show.img, show.name, show.video, show.tags, show.id));
    }
}


async function getData() {
    let watchListId = document.getElementById('watchId').value;
    if(watchListId >= 0)
    {
        let json = await fetchData(watchListId);
        if(json.error)
        {
            alert(json.error);
            return;
        }
        populateTable(json.data);

        if(document.getElementById('addShowId') == undefined)
        {
            let displayData = document.getElementById('displayData');
            let InputShowID = document.createElement('input');
            InputShowID.type = 'text';
            InputShowID.min = 0;
            InputShowID.id = 'addShowId';
            let addIdButton = createButton('Add Show');
            addIdButton.onclick = function(){addRow()};
            displayData.appendChild(InputShowID);
            displayData.appendChild(addIdButton);
        }

    }   
}

async function createWatchList() {
    let watchListId = document.getElementById('watchId').value;
    if(watchListId >= 0)
    {
        await fetch('http://localhost:5000/list/', {
                method: "POST",
                mode: "cors",
        });

        if(document.getElementById('addShowId') == undefined)
        {
            let displayData = document.getElementById('displayData');
            let InputShowID = document.createElement('input');
            InputShowID.type = 'text';
            InputShowID.min = 0;
            InputShowID.id = 'addShowId';
            let addIdButton = createButton('Add Show');
            addIdButton.onclick = function(){addRow()};
            displayData.appendChild(InputShowID);
            displayData.appendChild(addIdButton);
        }

    }   
}

async function sendChanges() {
    let watchListId = document.getElementById('watchId').value;
    if( watchListId >= 0 && Object.keys(changes).length > 0)
    {
        await fetch('http://localhost:5000/list/' + watchListId, {
                method: "POST",
                mode: "cors",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(changes),
        });
        changes = {add : [],  delete : []}; //reset changes
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
    for(let show of shows_data)
    {
        Shows[show.name.toLowerCase()] = show.id;
    }

    
}


window.onload = function(){
    document.getElementById('watchId').value =  user_id;
    getData();  
    fetchShows();
    
};







