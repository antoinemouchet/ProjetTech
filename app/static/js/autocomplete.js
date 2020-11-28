function checkvalues(id_input, id_autocomplete, data){
    let input_element = document.getElementById(id_input);
    let autocomplete_element = document.getElementById(id_autocomplete);
    let input_name = input_element.value;
    if(input_name)
    {
        autocomplete_element.innerHTML = null;
        input_name = input_name.toLowerCase();
        let founds = 0;
        let index = 0;
        let names =  Object.keys(data);
        while(founds < 5 && index < names.length)
        {
            if(names[index].includes(input_name))
            {
                founds++;
                addAutoCompleteLine(names[index], input_element, autocomplete_element);
            }
            index++;
        }

    }
}

function complete(text, input_element, autocomplete_element){
    input_element.value = text;autocomplete_element.innerHTML = null;
}

function addAutoCompleteLine(text, input_element, autocomplete_element){
    let line = document.createElement('input');
    line.type = 'button';
    let textlink = document.createElement('a');
    textlink.href = '#';
    textlink.onclick = function(){complete(text, input_element, autocomplete_element); return false;};
    line.value = text;
    textlink.appendChild(line);
    autocomplete_element.appendChild(textlink);
}