function checkvalues(id_input, id_autocomplete, data) {
    let input_element = document.getElementById(id_input);
    let autocomplete_element = document.getElementById(id_autocomplete);
    let input_name = input_element.value;
    if (input_name) {
        autocomplete_element.innerHTML = null;
        input_name = input_name.toLowerCase();
        let founds = 0;
        let index = 0;
        let names = Object.keys(data);
        while (founds < 5 && index < names.length) {
            if (names[index].toLowerCase().includes(input_name)) {
                founds++;
                addAutoCompleteLine(names[index], input_element, autocomplete_element);
            }
            index++;
        }

        if(founds > 0)
            autocomplete_element.className ="dropdown-menu show";
        else
            autocomplete_element.className ="dropdown-menu";
    }
}

function complete(text, input_element, autocomplete_element) {
    input_element.value = text; 
    autocomplete_element.innerHTML = null;
    autocomplete_element.className ="dropdown-menu";
}

function addAutoCompleteLine(text, input_element, autocomplete_element) {
    let textlink = document.createElement('a');
    textlink.href = '#';
    textlink.className = 'dropdown-item';
    textlink.onclick = function(){complete(text, input_element, autocomplete_element); return false;};
    textlink.innerHTML = text;
    autocomplete_element.appendChild(textlink);
}
