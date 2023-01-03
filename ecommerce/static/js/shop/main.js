

const url = window.location.href
const searchform = document.getElementById('search-form')
const searchInput = document.getElementById('search-input')
const resultsBox = document.getElementById('results-box')

const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData = (product)  => {
    $.ajax({
        type: 'POST',
        url: '/search/',
        data:{
            'csrfmiddlewaretoken': csrf,
            'product': product, 
        },
        success: (res)=> {
            console.log(res)
            const data = res.data
            if (Array.isArray(data)) {
                resultsBox.innerHTML = ""
                data.forEach(product => {
                    resultsBox.innerHTML += `
                        <a href="${'/product/'}${product.slug}" class="text-decoration-none">
                            <div class="row mt-2 mb-2">
                                <div class="col-2">
                                    <img src="${product.image}" class="product-img">
                                </div>
                                <div class="col-10">
                                    <h5>${product.name}</h5>
                                </div>
                            </div>
                        </a>
                        `
                })
            }
            else{
                if (searchInput.value.length > 0){
                    resultsBox.innerHTML = `<b> ${data}</b>`
                }
                else{
                    console.log("not visible")
                    resultsBox.classList.add('invisible')
                }
            }
        },
        error: (res)=>{

        }
    })
}

searchInput.addEventListener('keyup', e=>{
    console.log(e.target.value)
    if (resultsBox.classList.contains('invisible')){
        resultsBox.classList.remove('invisible')
    }
    sendSearchData(e.target.value)
})