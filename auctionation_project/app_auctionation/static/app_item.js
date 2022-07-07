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

const itemQuality = document.querySelector('.item').getAttribute('id')
const itemText = document.querySelector('.item')

switch (itemQuality) {
    case 'Poor':
        itemText.style.color = '#9d9d9d'
        break;

    case 'Common':
        itemText.style.color = 'white'
        break;

    case 'Uncommon':
        itemText.style.color = '#1eff00'
        break;

    case 'Rare':
        itemText.style.color = '#0070dd'
        break;

    case 'Epic':
        itemText.style.color = '#a335ee'
        break;

}

const realmId = document.querySelector('#realmId').innerText;
const itemId = document.querySelector('#itemId').innerText;
const faction = document.querySelector('#faction').innerText;

fetch(
    `http://localhost:8000/api/item_stats/${realmId}/${faction}/${itemId}`
).then(
    function (resp) {
        return resp.json()
    }
).then(
    function (data) {
        const dates = [];
        const lowestBuyout = [];
        const meanBuyout = [];
        const medianBuyout = [];
        const auctionsCount = [];

        for (const entry of data){
            dates.push(entry.date.value);
            lowestBuyout.push(entry.lowest_buyout);
            meanBuyout.push(entry.mean_buyout);
            medianBuyout.push(entry.median_buyout);
            auctionsCount.push(entry.auctions_count);
        }

        let ctx = document.querySelector('#auctions_count').getContext('2d');
        let myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Auctions Count',
                    data: auctionsCount,
                    borderColor:'rgba(255, 255, 255, 1)',
                    borderWidth: 1,
                    pointRadius: 1,
                    pointHitRadius: 15
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                    x: {
                        ticks: {
                            callback: function(val, index) {
                                return index % 3 === 0 ? this.getLabelForValue(val) : '';
                            }
                        }
                    }

                },
                plugins: {
                    title: {
                        text: 'Lowest Buyout'
                    }
                }
            }
        });

        ctx = document.querySelector('#lowest_buyout').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Lowest Buyout',
                    data: lowestBuyout,
                    borderColor:'rgb(255, 120, 120)',
                    borderWidth: 1,
                    pointRadius: 1,
                    pointHitRadius: 15
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                    x: {
                        ticks: {
                            callback: function(val, index) {
                                return index % 3 === 0 ? this.getLabelForValue(val) : '';
                            }
                        }
                    }

                },
                plugins: {
                    title: {
                        text: 'Lowest Buyout'
                    }
                }
            }
        });

        ctx = document.querySelector('#mean_buyout').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Mean Buyout',
                    data: meanBuyout,
                    borderColor:'rgb(101, 255, 62)',
                    borderWidth: 1,
                    pointRadius: 1,
                    pointHitRadius: 15
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                    x: {
                        ticks: {
                            callback: function(val, index) {
                                return index % 3 === 0 ? this.getLabelForValue(val) : '';
                            }
                        }
                    }

                },
                plugins: {
                    title: {
                        text: 'Mean Buyout'
                    }
                }
            }
        });

        ctx = document.querySelector('#median_buyout').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Median Buyout',
                    data: medianBuyout,
                    borderColor:'rgb(255, 211, 115)',
                    borderWidth: 1,
                    pointRadius: 1,
                    pointHitRadius: 15
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    },
                    x: {
                        ticks: {
                            callback: function(val, index) {
                                return index % 3 === 0 ? this.getLabelForValue(val) : '';
                            }
                        }
                    }

                },
                plugins: {
                    title: {
                        text: 'Median Buyout'
                    }
                }
            }
        });
    }
)
