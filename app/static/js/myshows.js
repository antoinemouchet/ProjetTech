function createButton(value)
{
	let button = document.createElement('input');
	button.type = 'button';
	button.value = value;
	return button;
}



function rowShow(pictureLink, showName, showPath, status, showId)
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
    deleteButton.src = '/{delete:['+showId+']}';
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
        tbody.appendChild(rowShow(show.img, show.name, show.video, null, show.id));
    }
}

//test
window.onload = function(){
    let data = [{img: './someting.png', name: 'show 1',  video : './video.mp4', id : 0},
                {img: './someting2.png', name: 'show 2',  video : './video.mp4', id : 1},
                {img: './someting3.png', name: 'show 3',  video : './video.mp4', id : 2}];
    populateTable(data);

}