var slider = document.getElementById('slider');
var min_price = parseFloat(document.getElementById('min_price').value).toFixed(2).toString();
var max_price = parseFloat(document.getElementById('max_price').value).toFixed(2).toString();

var price = [min_price, max_price];

noUiSlider.create(slider, {
    start: price,
    connect: true,
    behaviour: 'tap',
    tooltips: [true, true],
    range: {
        'min': 0,
        '0.01%': [0, 5],
        'max': 100
    }
});

slider.noUiSlider.on('change', function (values, handle) {

    if ((price[0] !== values[0]) || (price[1] !== values[1])){
        price = values;

        var url = '/set_opt/'

        fetch(url, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken': '',
            },
            body: JSON.stringify({'type':'price','min_price':price[0],'max_price':price[1]})
        })

        .then((response) => {
            return response.json()
        })

        .then((data) => {
            location.reload()
        })
    }
    
});

function CheckBox(o,type){

    var url = '/set_opt/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': '',
        },
        body: JSON.stringify({'type':type,'action':o.checked,'index': o.name })
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {

        location.reload()

    })

}