window.onload = () => {buildPage();}


async function buildPage() {
  
    let data = await fetch('http://localhost:5000/shows/', {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
    });
    let json = await data.json();


    let showList = document.getElementById("show-list");
    showList.innerHTML = "";

    for (let i = 0; i < json.length; i++) {
        const show = json[i];
        let row = document.createElement("div");
        row.className = "row";

        // First column is for image
        let col1 = document.createElement("div");
        col1.className = "col-sm";
        let img = document.createElement("img");
        img.src = "/" + show["img"];
        img.width = 128;
        col1.appendChild(img);

        // Second column is title
        let col2 = document.createElement("div");
        col2.className = "col-sm";
        col2.innerText = show["name"];

        // Third column is for tags
        let col3 = document.createElement("div");
        col3.className = "col-sm";
        col3.innerText = show["tags"];

        // Fourth column is to go to specific page
        let col4 = document.createElement("div");
        col4.className = "col-sm";

        let a = document.createElement("a");
        a.href = "/shows/" + i;

        let detail = document.createElement("button");
        detail.className = "btn btn-primary";
        detail.innerText = "Details";

        a.appendChild(detail);
        col4.appendChild(a);

        row.appendChild(col1);
        row.appendChild(col2);
        row.appendChild(col3);
        row.appendChild(col4);
        
        showList.appendChild(row);
        showList.appendChild(document.createElement("hr"));
    }


}
