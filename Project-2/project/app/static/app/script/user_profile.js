let post=document.getElementById('post');
let addPost=document.getElementById('add');
let sideShow=document.getElementById('side-show');
let aSide=document.getElementById('a-side');
let cancelPost=document.getElementById('cancel');

cancelPost.addEventListener('click',()=>{
    post.style.visibility='hidden';
})

console.log(aSide.style.visibility);
sideShow.addEventListener('click',()=>{

    if( window.getComputedStyle(aSide).visibility ==='hidden'){
    aSide.style.animation=' nav-side .5s linear both alternate';


    }
    else if( window.getComputedStyle(aSide).visibility ==='visible') {
        aSide.style.animation=' nav-side-hide .5s linear both alternate';
    }
})


add.addEventListener('click',()=>{
    if(window.getComputedStyle(post).visibility==='hidden')
    {
        post.style.visibility='visible';
    

    }
   
    else if (window.getComputedStyle(post).visibility==='visible')
        post.style.visibility='hidden';

    {

    }


})


