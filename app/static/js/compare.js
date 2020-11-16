


function rowShows(pictureLink, showName)
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


function populateTable(id, list)
{
    let tbody = document.getElementById(id);
    for(let show of list)
    {
        tbody.appendChild(rowShows(show.img, show.name));
    }
}

//test
window.onload = function(){
    //don'
    let me = [{img: './someting.png', name: 'show 1',  video : './video.mp4', id : 0},
                {img: './someting2.png', name: 'show 2',  video : './video.mp4', id : 1},
                {img: './someting3.png', name: 'show 3',  video : './video.mp4', id : 2}];

    let friend = [{img: './someting4.png', name: 'show 4',  video : './video.mp4', id : 3},
                {img: './someting5.png', name: 'show 5',  video : './video.mp4', id : 4},
                {img: './someting6.png', name: 'show 6',  video : './video.mp4', id : 5}];
    
    populateTable('me', me); //left
    populateTable('friend', friend); //right

}