//INIT

var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action


        if (action == 'see'){
            seeItem(productId);
            return true;
        }

        if (user == "AnonymousUser"){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }

    })
}

function addCookieItem(productId, action){

    if ((action == 'add') || (action == 'add_alt')){
        if (cart[productId] == undefined){
            cart[productId] = {'quantity':1}
        }
        else
        {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0){
            delete cart[productId]
        }
    }

    quantity = 0;
    for (var [key, child] of Object.entries(cart)) {
        quantity += child.quantity; 
    }
    
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/;SameSite=Strict; Secure";
    document.getElementById('cart-total').innerText = '('+quantity+')';

    if ((action == 'remove') || (action == 'add_alt')){
        location.reload();
    }
    else
    {
        showSnackbar(action);
    }
}

function updateUserOrder(productId, action){

    var url = '/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {

        document.getElementById('cart-total').innerText = '('+data.quantity+')';
        showSnackbar(action);
    })
}

function seeItem(productId){

    var url = '/get_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': '',
        },
        body: JSON.stringify({'productId':productId})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {

        $('#exampleModalCenter').modal('show');

        document.getElementById('exampleModalCenterTitle').innerText = data.name;
        document.getElementById('exampleModalPrice').innerText = 'Q '+data.price;
        document.getElementById('id-img-modal').src = data.url;

    })
}


function showSnackbar(action) {
    // Get the snackbar DIV
    var parent = document.getElementById("snackbars");
    var x = document.createElement("div");
  
    // Add the "show" class to DIV
    x.className = "snackbar show";

    text_act = '';
    if (action == 'add'){
        x.style.backgroundColor = 'ForestGreen';
        text_act = 'item added <i class="fas fa-cart-plus"></i>';
    }
    else
    {
        x.style.backgroundColor = 'orange';
        text_act = 'item removed -';
    }
  
    x.innerHTML = text_act;

    // After 2 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 2000);
    parent.appendChild(x);
  } 



////
window.ondragstart = function() { return false; } 
