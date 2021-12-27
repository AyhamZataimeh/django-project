let dropdownDisplay=document.getElementById('dropdown-display');
let dropdownMenu=document.getElementById('dropdown-menu');
let asideDisplay=document.getElementById('aside-show');
let aside=document.getElementById('aside');
let card=document.getElementById('card');

dropdownDisplay.addEventListener('click',()=>{
    if(window.getComputedStyle(dropdownMenu).visibility==='hidden'){
        dropdownMenu.style.visibility='visible';
        dropdownMenu.style.animation='dropdown-show .5s linear both';


    }
    else if (window.getComputedStyle(dropdownMenu).visibility==='visible') {
        dropdownMenu.style.animation='dropdown-hide .5s linear both';
    }

})

asideDisplay.addEventListener('click',()=>{
    if(window.getComputedStyle(aside).visibility==='hidden'){
        aside.style.animation='aside-show .5s linear both';
        asideDisplay.style.transition='.6s';
        asideDisplay.style.marginLeft='21%'
        asideDisplay.style.transform="rotate(90deg)";


    } else if (window.getComputedStyle(aside).visibility==='visible')
    {

        asideDisplay.style.transition='.5s';
        asideDisplay.style.marginLeft='0%'
        asideDisplay.style.transform="rotate(0deg)";
        aside.style.animation='aside-hide .5s linear both';

        

    }
  
})


if (window.innerWidth>600) {
    aside.style.display='none';

}