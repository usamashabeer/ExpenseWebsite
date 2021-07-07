console.log('test');
searchField = document.querySelector('#searchField');
tableOutput = document.querySelector('.table-output');
appTable = document.querySelector('.app-table');
bodyTable = document.querySelector('.table-body');




pagiContainer = document.querySelector('.pagination-container');

tableOutput.style.display = 'none';

searchField.addEventListener('keyup', (e) => {
    searchVal = e.target.value;
    console.log(searchVal);

    if (searchVal.trim().length > 0) {
        pagiContainer.style.display = 'none';
        bodyTable.innerHTML = '';
        fetch('/income/search-income', {
                body: JSON.stringify({ searchText: searchVal }),
                method: 'POST',
            })
            .then((res) => res.json())
            .then((data) => {
                console.log('data', data)
                appTable.style.display = 'none';
                tableOutput.style.display = 'block';

                if (data.length === 0) {
                    tableOutput.innerHTML - '';
                    tableOutput.innerHTML += 'No Result Found';
                } else {
                    Object.values(data).forEach(item => {
                        bodyTable.innerHTML += '<tr> <td>' + item.amount + '</td><td>' + item.source + '</td> <td>' + item.description + '</td> <td>' + item.date + '</td> </tr>';

                    });
                }
            });
    } else {

        tableOutput.style.display = 'none';
        appTable.style.display = 'block';
        pagiContainer.style.display = 'block';

    }
});