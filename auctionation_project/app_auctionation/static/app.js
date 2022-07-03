function getPrice(val) {
    let g = 0;
    let s = 0;
    let b;

    b = val % 100;
    const rem = Math.floor(val / 100)

    s = rem % 100;
    const rem2 = Math.floor(rem / 100)

    g = rem2

    // for (const item of result){
    //     if (item === 0){
    //         result.splice(result.indexOf(item), 1)
    //     }
    // }

    return [g, s, b]

}

function getData(url) {
    fetch(
        url, 
        {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*' ,
            }
        }
    ).then(
        function (resp) {
            return resp.json()
        }
    ).then(
        function (data) {

            const table = document.createElement('table')

            table.className = "table"
            for (data_element of data){
                const id = data_element.wow_item_id
                const buyout = data_element.buyout
                const quantity = data_element.quantity
                
                const tr = document.createElement('tr')
                fetch(
                    `http://localhost:8000/api/item/${id}/`
                ).then(
                    function (resp) {
                        return resp.json()
                    }
                ).then(
                    function (data) {
                        tr.className = ""
                        const img_td = document.createElement('td')
                        const img = document.createElement('img')
                        img.setAttribute('src', `http://localhost:8000/api/icon/${id}/`)
                        
                        const td_quantity = document.createElement('td')
                        td_quantity.innerText = quantity

                        img_td.appendChild(img)
                        tr.appendChild(img_td)

                        const quality_td = document.createElement('td')
                        quality_td.innerText = data.name

                        const item_quality = data.quality

                        switch (item_quality) {
                            case 'Uncommon':
                                quality_td.style.color = 'green'
                                break;
                            
                            case 'Rare':
                                quality_td.style.color = 'blue'
                                break;
                            
                            case 'Epic':
                                quality_td.style.color = 'purple'
                                break;
                
                        }

                        const td_buy = document.createElement('td')
                        td_buy.innerText = getPrice(buyout)
                        td_buy.style.justifyContent = 'right'

                        tr.appendChild(quality_td)
                        tr.appendChild(td_quantity)
                        tr.appendChild(td_buy)

                        table.appendChild(tr)
                        
                    }
                )
            }

            document.querySelector('body').appendChild(table)

        }
    )
}

const searchForm = document.querySelector('#search')

document.querySelector('#search_button').addEventListener('click', function(e){
    e.preventDefault()

    if (document.querySelector('table')){
        document.querySelector('table').remove()
    }
    
    const itemQuery = searchForm.elements['search_input'].value
    
    const realm = document.querySelector('#select_realm')
    const chosen_realm = realm.options[realm.selectedIndex].value

    const faction = document.querySelector('#select_faction')
    const chosen_faction = faction.options[faction.selectedIndex].value

    return getData(`http://localhost:8000/api/auctions/${chosen_realm}/${chosen_faction}/${itemQuery}/`)
})


// for (element of document.querySelectorAll('.db-item')) {
//     fetch(
//         `https://us.api.blizzard.com/data/wow/item/${element.id}?namespace=static-classic-us&locale=en_US&access_token=USHPrxtIW9KtEcG9gGPgZTBM0yKY4WKeS7`
//     ).then(
//         function (resp) {
//             return resp.json()
//         }
//     ).then(
//         function (data) {
//             // console.log(data.id, data.name)
//             for (const el of document.querySelectorAll(`[id="${data.id}"]`)) {
//                 el.querySelector('span').innerText = data.name
//             }
//         }
//     )
// }

// for (element of document.querySelectorAll('.db-item')) {
//     fetch(
//         `https://us.api.blizzard.com/data/wow/media/item/${element.id}?namespace=static-classic-us&locale=en_US&access_token=USHPrxtIW9KtEcG9gGPgZTBM0yKY4WKeS7`
//     ).then(
//         function (resp) {
//             return resp.json()
//         }
//     ).then(
//         function (data) {
//             for (const el of document.querySelectorAll(`[id="${data.id}"]`)) {
//                 img = el.querySelector('img')
//                 img.setAttribute('src', data.assets[0].value)
//             }
//         }
//     )
// }

// for (const element of document.querySelectorAll('.buyout')) {
//     const elementContent = element.innerText
//     element.innerText = getPrice(elementContent)[0] + 'g ' + getPrice(elementContent)[1] + 's ' + getPrice(elementContent)[2] + 'b'
// }


// document.querySelector('#search').addEventListener('submit', function(e){
//     e.preventDefault()
//     const search = this.elements.search.value
//     fetch(
//         `https://us.api.blizzard.com/data/wow/search/item?namespace=static-us&name.en_US=${search}&orderby=id&_page=1&access_token=USHPrxtIW9KtEcG9gGPgZTBM0yKY4WKeS7`
//     ).then(
//         function(resp){
//             return resp.json
//         }
//     ).then(
//         function(data){
            
//         }
//     )
// })

// document.addEventListener('DOMContentLoaded', function(){
//     return loadAllElements()
// })