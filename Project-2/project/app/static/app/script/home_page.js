let dropdownDisplay=document.getElementById('dropdown-display');
let dropdownMenu=document.getElementById('dropdown-menu');

dropdownDisplay.addEventListener('click',()=>{
    if(window.getComputedStyle(dropdownMenu).visibility==='hidden'){
        dropdownMenu.style.visibility='visible';
        dropdownMenu.style.animation='dropdown-show .5s linear both';


    }
    else if (window.getComputedStyle(dropdownMenu).visibility==='visible') {
        dropdownMenu.style.animation='dropdown-hide .5s linear both';
    }

})