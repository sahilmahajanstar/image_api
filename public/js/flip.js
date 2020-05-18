var card=document.querySelectorAll('.container')
var cover1=document.querySelectorAll('.cover1')
for (let i=0;i<card.length;i++)
{
    card[i].addEventListener('mouseover',function(){
            cover1[i].style.display="block";
            
        })
    
    card[i].addEventListener('mouseout',function(){
            cover1[i].style.display="none";
        })
           
}
function generate_key()
{
    name=document.getElementById('name').value;
    $.ajax({
        type: "post",
        url: "/generatekey",
        data: {'name':name},
        success: function (response) {
            console.log(response)
            document.querySelector('.key-content').innerText=response;
            document.getElementById('key').value=response;    
        }
    });
}

function get_image()
{
    key=document.getElementById('key').value;
    image=document.getElementById('image').value;
    $.ajax({
        type: "POST",
        url: `/imageapi?key=${key}&&image=${image}`,
        success: function (response) {
            document.querySelector('.res').innerText=JSON.stringify(response) ;
            document.getElementById('imageshow').src=response['url']
            console.log(typeof(response))
        }
    });
}