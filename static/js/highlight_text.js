const worktext = document.getElementById("displayed_text").innerHTML

function highlightText(target){
    let regexPattern = new RegExp("\\b"+target+"\\b", 'gi');

    if(target.startsWith("-")){
        regexPattern = new RegExp("\\w+"+target.replace("-","")+"\\b", 'gi');
    }

    let text = worktext;
    text = text.replace(/(<mark class="highlightColor">|<\/mark>)/gim, '');
    const newText = text.replace(regexPattern, '<mark class="highlightColor">$&</mark>');
    document.getElementById("displayed_text").innerHTML = newText;
}

function highlightTextReset(){
    document.getElementById("displayed_text").innerHTML = worktext;
}
