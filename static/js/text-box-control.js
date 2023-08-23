// Get the textarea element 
var textarea = document.getElementById ("content");

// Add an event listener for input event 
textarea.addEventListener ("input", function () { 
    // Reset the height to 0 
    textarea.style.height = 0; 
    // Set the height to the scroll height (the actual height of the content) 
    textarea.style.height = textarea.scrollHeight + "px"; 
}); 