function getPrice(val) {
    let g = 0;
    let s = 0;
    let b;

    b = val % 100;
    const rem = Math.floor(val / 100)

    s = rem % 100;
    const rem2 = Math.floor(rem / 100)

    g = rem2

    return [g, s, b]

}

function getItem(url, realm=null, faction=null) {
    fetch(
        url,
    ).then(
        function (resp) {
            return resp.json()
        }
    ).then(
        function (data) {
            const h5 = document.createElement('h5')
            h5.innerText = 'Items found:'
            h5.className = 'foundInfo'

            document.querySelector('.container').appendChild(h5)

            const itemTable = document.createElement('table')
            itemTable.className = 'table'
            document.querySelector('.container').appendChild(itemTable)

            const tr = document.createElement('tr')

            if (data.length === 0) {
                tr.innerText = 'No items found matching given query.'    
                itemTable.appendChild(tr)

            } else {
                for (element of data){
                    const tr = document.createElement('tr')
                    const id = element.wow_id
                
                    const img_td = document.createElement('td')
                    const img = document.createElement('img')
                    img.setAttribute('src', `http://localhost:8000/api/icon/${id}/`)

                    img_td.appendChild(img)
                    tr.appendChild(img_td)

                    const name_td = document.createElement('td')
                    name_td.innerText = element.name

                    const itemLink = document.createElement('a')
                    itemLink.setAttribute('href', `http://localhost:8000/item/${realm}/${faction}/${id}/`)

                    const itemLinkButton = document.createElement('button')
                    itemLinkButton.className = 'btn btn-warning'
                    itemLinkButton.innerText = 'View'
                    
                    itemLink.appendChild(itemLinkButton)

                    const link_td = document.createElement('td')
                    link_td.appendChild(itemLink)

                    const item_quality = element.quality

                    switch (item_quality) {
                        case 'Common':
                            name_td.style.color = 'white'
                            break;

                        case 'Uncommon':
                            name_td.style.color = '#1eff00'
                            break;
                        
                        case 'Rare':
                            name_td.style.color = '#0070dd'
                            break;
                        
                        case 'Epic':
                            name_td.style.color = '#a335ee'
                            break;
                    
                    }

                    tr.appendChild(name_td)
                    tr.appendChild(link_td)
                    itemTable.appendChild(tr)
                }
            }
        }
    )
}

function getAuctionsData(url) {
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

            const h5 = document.createElement('h5')
            h5.innerText = `Current auctions on chosen realm, side: `
            h5.className = 'foundInfo'

            document.querySelector('.container').appendChild(h5)

            table.className = "table"

            const tableHeader = document.createElement('tr')

            let tableHeaderData = document.createElement('th')
            tableHeaderData.innerText = ''
            tableHeader.appendChild(tableHeaderData)

            tableHeaderData = document.createElement('th')
            tableHeaderData.innerText = 'Name'
            tableHeader.appendChild(tableHeaderData)

            tableHeaderData = document.createElement('th')
            tableHeaderData.innerText = 'Quantity'
            tableHeader.appendChild(tableHeaderData)

            tableHeaderData = document.createElement('th')
            tableHeaderData.innerText = 'Buyout (g, s, b)'
            tableHeader.appendChild(tableHeaderData)

            table.appendChild(tableHeader)

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
                            case 'Poor':
                                quality_td.style.color = '#9d9d9d'
                                break;

                            case 'Common':
                                quality_td.style.color = 'white'
                                break;

                            case 'Uncommon':
                                quality_td.style.color = '#1eff00'
                                break;
                            
                            case 'Rare':
                                quality_td.style.color = '#0070dd'
                                break;
                            
                            case 'Epic':
                                quality_td.style.color = '#a335ee'
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

            document.querySelector('.container').appendChild(table)

        }
    )
}

const searchForm = document.querySelector('#search')

document.querySelector('#search_button').addEventListener('click', function(e){
    e.preventDefault()

    if (document.querySelector('.foundInfo')) {
        for (const h5 of document.querySelectorAll('.foundInfo')){
            h5.remove()
        }
    }

    if (document.querySelector('table')){
        for (const table of document.querySelectorAll('table')){
            table.remove()
        }
    }

    if (document.querySelector('.obs')){
        document.querySelector('.obs').remove()
    }
    
    const itemQuery = searchForm.elements['search_input'].value
    
    const realm = document.querySelector('#select_realm')
    const chosen_realm = realm.options[realm.selectedIndex].value

    const faction = document.querySelector('#select_faction')
    const chosen_faction = faction.options[faction.selectedIndex].value

    getItem(`http://localhost:8000/api/item/${itemQuery}/`, chosen_realm, chosen_faction)
    getAuctionsData(`http://localhost:8000/api/auctions/${chosen_realm}/${chosen_faction}/${itemQuery}/`)
})
