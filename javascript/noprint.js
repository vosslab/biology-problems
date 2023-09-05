/*
NoPrint.js V1.0
Created by PDFAntiCopy.com
Modified by Neil Voss, Sept 2023
*/

// Setting default values for the variables.
// If the variables are not defined elsewhere, they will default to 'true'.
var noPrint = typeof noPrint !== 'undefined' ? noPrint : true;
var noCopy = typeof noCopy !== 'undefined' ? noCopy : true;
var noScreenshot = typeof noScreenshot !== 'undefined' ? noScreenshot : true;
var autoBlur = typeof autoBlur !== 'undefined' ? autoBlur : true;

console.log("Script loaded. Debugging the flags.");
console.log(`noPrint: ${noPrint}`);
console.log(`noCopy: ${noCopy}`);
console.log(`noScreenshot: ${noScreenshot}`);
console.log(`autoBlur: ${autoBlur}`);

// Check if the noCopy flag is set to true
if (noCopy) {
    // Disable the copy functionality
    console.log("noCopy is true, adding handlers.");
    document.body.oncopy = function() { return false };

    // Disable the context menu (right-click menu)
    document.body.oncontextmenu = function() { return false };

    // Disable text selection and drag operations
    document.body.onselectstart = document.body.ondrag = function() {
        return false;
    };

    // Add an event listener to capture 'keydown' events
    document.addEventListener('keydown', function(event) {
        // Prevent saving via Ctrl-S or Command-S
        if ((event.ctrlKey || event.metaKey) && (event.keyCode === 83 || event.code === 'KeyS')) {
            event.preventDefault();
        }
    });
}

// Check if the noPrint flag is set to true
if (noPrint) {
    // Create a span element to overlay the body when printing
    console.log("noPrint is true, adding handlers.");
    var c = document.createElement("span");

    // Initially set to be invisible and positioned absolutely
    c.style.display = "none";
    c.style.position = "absolute";
    c.style.background = "#000";

    // Insert the span as the first child of the body
    document.body.insertBefore(c, document.body.firstChild);

    // Set the dimensions of the span to match the body
    c.style.width = document.body.scrollWidth + 'px';
    c.style.height = document.body.scrollHeight + 'px';

    // Make the span visible
    c.style.display = "block";

    // Create a style element to hide the body when printing
    var cssNode3 = document.createElement('style');
    cssNode3.type = 'text/css';
    cssNode3.media = 'print';
    cssNode3.innerHTML = 'body{display:none}';

    // Append the style to the head element
    document.head.appendChild(cssNode3);
}

var cssNode2 = document.createElement('style');
cssNode2.type = 'text/css';
cssNode2.media = 'screen';
cssNode2.innerHTML ='div{-webkit-touch-callout: none;-webkit-user-select: none;-khtml-user-select: none;-moz-user-select: none;-ms-user-select: none;user-select: none;}';
document.head.appendChild(cssNode2);
document.body.style.cssText="-webkit-touch-callout: none;-webkit-user-select: none;-khtml-user-select: none;-moz-user-select: none;-ms-user-select: none;user-select: none;";

function toBlur()
{
	if (autoBlur)
	document.body.style.cssText="-webkit-filter: blur(5px);-moz-filter: blur(5px);-ms-filter: blur(5px);-o-filter: blur(5px);filter: blur(5px);"
}

function toClear()
{
	document.body.style.cssText="-webkit-filter: blur(0px);-moz-filter: blur(0px);-ms-filter: blur(0px);-o-filter: blur(0px);filter: blur(0px);"
}

document.onclick = function(event){
 	toClear();
}

document.onmouseleave = function(event){
	toBlur();
}

document.onblur = function(event){
 	toBlur();
}

document.addEventListener('keyup', (e) => {
    if (e.key == 'PrintScreen') {
        console.log("PrintScreen event detected.");
    	if (noScreenshot)
    	{
        navigator.clipboard.writeText('');
      }
    }
});

document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key == 'p') {
        if (noPrint)
	    	{
	        e.cancelBubble = true;
	        e.preventDefault();
	        e.stopImmediatePropagation();
	      }
    }
});
