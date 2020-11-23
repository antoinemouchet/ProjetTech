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
    imgCol.className = "col-sm";
    let img = document.createElement("img");
    img.src = "/" + show["img"];
    img.width = 256;

    imgCol.appendChild(img);

    // Create a second colum
    let descCol = document.createElement("div");
    imgCol.className = "col-sm";
    
    // Inner container
    let innerCont = document.createElement("div");
    innerCont.className = "container";

    // Row 1 is description
    let iRow1 = document.createElement("div");
    iRow1.className = "row";
    let desc = document.createElement("p");
    desc.textContent = show["desc"];

    iRow1.appendChild(desc);

    // Row 2 is tags
    let iRow2 = document.createElement("div");
    iRow2.className = "row";
    let tags = document.createElement("p");
    tags.textContent = show["tags"];

    iRow2.appendChild(tags);

    // Add rows to inner container
    innerCont.appendChild(iRow1);
    innerCont.appendChild(iRow2);

    // Add container to column
    descCol.appendChild(innerCont);

    // Add columns to outermost row
    row2.appendChild(imgCol);
    row2.appendChild(descCol);

    // Add rows to page
    details.appendChild(row1);
    details.appendChild(row2);
}