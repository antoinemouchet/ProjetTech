window.onload = () => {buildPage();}


async function buildPage() {
  
    let data = await fetch('http://localhost:5000/show/' + showID, {
            method: "GET",
            mode: "cors",
            headers: { "Content-Type": "application/json" },
    });
    let show = await data.json();

    let details = document.getElementById("show-details");
    details.innerHTML = "";

    // First row title only
    let row1 = document.createElement("div");
    row1.className = "row";

    let titleCol = document.createElement("div");
    titleCol.className = "col-sm"

    let title = document.createElement("h3");
    title.innerText = show["name"];
    title.style.textAlign = "center";

    titleCol.appendChild(title);
    row1.appendChild(titleCol);


    // Second row img + inner container
    let row2 = document.createElement("div");
    row2.className = "row";

    let imgCol = document.createElement("div");
    imgCol.className = "col-4";
    let img = document.createElement("img");
    img.src = "/" + show["img"];
    img.width = 256;

    imgCol.appendChild(img);

    // Create a second colum
    let descCol = document.createElement("div");
    descCol.className = "col-8";
    
    let desc = document.createElement("p");
    desc.innerHTML = "Description: " + show["desc"] + "<br><br>Tags: " + show["tags"];
    desc.style.textAlign = "left";

    // Add description to column
    descCol.appendChild(desc);

    // Add columns to outermost row
    row2.appendChild(imgCol);
    row2.appendChild(descCol);

    // Add rows to page
    details.appendChild(row1);
    details.appendChild(document.createElement("hr"));
    details.appendChild(row2);
}