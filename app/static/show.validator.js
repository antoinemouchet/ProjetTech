function validateShow() {
    
    // Validation on Strings
    let formName = document.getElementById("input-title").value;
    let desc = document.getElementById("input-desc").value;
    let tags = document.getElementById("input-tags").value;
    
    if (!checkString(formName) || !checkString(desc) || !checkString(tags)) {
        window.alert("The name, the description and the tags of the show have to be provided.");
        return false;
    }

    // Validation on files
    let imgValidExtensions = [".jpg", ".jpeg", ".bmp", ".gif", ".png"];
    let videoValidExtensions = [".mp4", ".webm"]
    
    if(!checkFile("input-image", "Image", imgValidExtensions) || !checkFile("input-video", "Video", videoValidExtensions)){
        return false;
    }

    return true;
}

/**
 * Returns true if the given string is non-empty and not whitespace only
 * @param {String} cstring : given string to check
 */
function checkString(cstring) {
    
    if(cstring.trim() === ""){
        return false;
    }

    return true;
}


function checkFile(fileID, fType, validExtensions)
{
    let cFile = document.getElementById(fileID).value;

    if (cFile.length == 0){
        window.alert(fType + " must be entered.");
        return false;
    }

    let validity = false;

    // check validity of extension        
    for (let i = 0; i < validExtensions.length; i++) {
        let currentExtension = validExtensions[i];
        
        if(cFile.substr(cFile.length - currentExtension.length, currentExtension.length).toLowerCase() == currentExtension.toLowerCase()){
            validity = true;
            return validity;
        }
    }

    // If invalid
    if(!validity){
        window.alert("Sorry, "+ fType + " extension is invalid, allowed extensions for " + fType +  " are: " + validExtensions.join(", "));
        return false;
    }

    return true;   
}




