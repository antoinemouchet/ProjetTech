window.onload = () => {
    buildStuff();
}

async function deleteFriend(friendId) {
    await fetch('http://localhost:5000/friends/' + userId, {
        method: 'delete',
        mode: 'cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "friend": friendId
        })
    });
    buildStuff();
}

function launchAdd() {
    addFriend(document.getElementById('user-name').value);
}

async function addFriend(friendId) {
    let response = await fetch('http://localhost:5000/friends/' + userId, {
        method: 'post',
        mode: 'cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            "friend": friendId
        })
    });
    let json = await response.json();
    if (json.msg == "do not exist") {
        document.getElementById('error').innerText = "This user do not exist";
    } else {
        document.getElementById('error').innerText = "";
    }
    buildStuff();
}

async function buildStuff() {
    let data = await fetch('http://localhost:5000/friends/' + userId, {
        method: 'get',
        mode: 'cors',
        headers: { 'Content-Type': 'application/json' },
    });
    let json = await data.json();
    console.log(JSON.stringify(json));

    let tbody = document.getElementById('list-friends');
    tbody.innerHTML = '';

    // Build page
    for (let i = 0; i < json['friends'].length; i++) {
        const friend = json['friends'][i];
        let tr = document.createElement('tr');
        let td1 = document.createElement('td');
        td1.innerText = friend['pseudo'];
        let td2 = document.createElement('td');
        let btn = document.createElement('button');
        btn.className = 'btn btn-danger';
        btn.innerText = "Delete";
        btn.onclick = () => {
            deleteFriend(friend['id']);
        }
        td2.appendChild(btn)
        tr.appendChild(td1)
        tr.appendChild(td2)
        tbody.appendChild(tr)
    }
}