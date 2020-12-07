/**
 * Main autocomplete function.
 * Display some possible values for AutoComplete, based on already written value.
 * @param {String} id_input, HMTL id of the input containing the value to autocomplete. 
 * @param {String} id_autocomplete, HTML id of the div containing the autocomplete proposals.
 * @param {*} data, Dictionary containing all possible values as keys.
 */
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

/**
 * Complete the passed input element.
 * @param {String} text, Completion value. 
 * @param {*} input_element, HTML input, Its value is replaced by text. 
 * @param {*} autocomplete_element, HTML div where the proposals are displayed. 
 */
function complete(text, input_element, autocomplete_element) {
    input_element.value = text; 
    autocomplete_element.innerHTML = null;
    autocomplete_element.className ="dropdown-menu";
}

/**
 * Add a new AutoComplete proposal.
 * @param {*} text, Completion value
 * @param {*} input_element, HTML input. 
 * @param {*} autocomplete_element,  HTML div where the proposals are displayed. 
 */
function addAutoCompleteLine(text, input_element, autocomplete_element) {
    let textlink = document.createElement('a');
    textlink.href = '#';
    textlink.className = 'dropdown-item';
    textlink.onclick = function(){complete(text, input_element, autocomplete_element); return false;};
    textlink.innerHTML = text;
    autocomplete_element.appendChild(textlink);
}
