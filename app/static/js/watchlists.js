
let changes = {add : [],  delete : []}
let compareMode = false;

function createButton(value)
{
	let button = document.createElement('input');
	button.type = 'button';
	button.value = value;
	return button;
}

function deleteRow(button, showId)
{
    let row = button.parentNode.parentNode;
    row.parentNode.removeChild(row);
    changes.delete.push(showId);
}


function addRow()
{
    let showId = document.getElementById('addShowId').value;
    let tbody = document.getElementById('tshows');
    tbody.appendChild(rowShow('', '', '', '', showId));
    changes.add.push(showId);
}



function rowShow(pictureLink, showName, showPath, showId)
{
    let row = document.createElement('tr');
    //elements
    let logo = document.createElement('td');
    let name = document.createElement('td');
    let seen = document.createElement('td');
    //actions
    let actions = document.createElement('td');

    let picture = document.createElement('img');
    picture.src = pictureLink;
    logo.appendChild(picture);

    let showLink = document.createElement('a');
    showLink.href = showPath;
    let nametxt = document.createTextNode(showName);
    showLink.appendChild(nametxt);
    name.appendChild(showLink);

    //seen
    let modifySeen = document.createElement('a');
    seen.appendChild(modifySeen);

    let deleteButton = createButton('remove');
    deleteButton.onclick = function(){deleteRow(this,showId)};
    actions.appendChild(deleteButton);

    row.appendChild(logo);
    row.appendChild(name);
    row.appendChild(seen);
    row.appendChild(actions);

    return row;
}

function populateTable(list)
{
    let tbody = document.getElementById('tshows');
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
            InputShowID.type = 'number';
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
            InputShowID.type = 'number';
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

    }   
}


// compare Mode

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


async function C_populateTable(button)
{
    let type = button.id;
    let watchListId = document.getElementById(type+'_id');
    let tbody = document.getElementById(type+'_table');
    let list = await fetchData(watchListId);
    if(json.error)
    {
            alert(json.error);
            return;
    }
    for(let show of list.data)
    {
        tbody.appendChild(C_rowShows(show.img, show.name));
    }
}

//All

function changeMode()
{
    let container = document.getElementById('container');
    compareMode = !compareMode;
    if(!compareMode)
    {
        container.innerHTML = '<h1>Watchlist</h1>\
        <input id="watchId" type="number" min=0>\
        <input type="button" value="Get" onclick="getData()">\
        <input type="button" value="Send changes" onclick="sendChanges()">\
        <input type="button" value="New" onclick="createWatchList()">\
        <div id="displayData">\
            <table class="table text-center">\
                <thead>\
                    <tr>\
                        <th>Logo</th>\
                        <th>Name</th>\
                        <th>Seen</th>\
                        <th>Actions</th>\
                    </tr>\
                </thead>\
                <tbody id="tshows">\
                </tbody>\
            </table>\
        </div>';
        changes = {add : [],  delete : []} //reset changes 
    }
    else
    {
        container.innerHTML = '<input id="me_id" type="number" min=0>\
        <input type="button" value="Get" id="me" onclick="C_populateTable(this)">\
        <table class="table text-center d-inline">\
            <thead>\
                <tr>\
                    <th>My list</th>\
                </tr>\
            </thead>\
            <tbody id="me_table">\
            </tbody>\
        </table>\
        <input id="friend_id" type="number" min=0>\
        <input type="button" value="Get" id="friend" onclick="C_populateTable(this)">\
        <table class="table text-center d-inline">\
            <thead>\
                <tr>\
                    <th>My friend\'s list</th>\
                </tr>\
            </thead>\
            <tbody id="friend_table">\
            </tbody>\
        </table>'
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







