// Function to fetch the existing list from the server via GET request
const getList = async () => {
  let url = 'http://127.0.0.1:5000/companies';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.companies.forEach(item => insertList(item.company_name, item.trading_name, item.cnpj, item.contact_name, item.phone, item.email))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Call the function for initial data loading
getList()

// Function to add an item to the server list via POST request
const postItem = async (inputCompany, inputTradingName, inputCnpj, inputContact, inputPhone, inputEmail) => {
  const formData = new FormData();
  formData.append('company_name', inputCompany);
  formData.append('trading_name', inputTradingName);
  formData.append('cnpj', inputCnpj);
  formData.append('contact_name', inputContact);
  formData.append('phone', inputPhone);
  formData.append('email', inputEmail);

  let url = 'http://127.0.0.1:5000/company';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Function to create a close button for each item in the list
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

// Function to remove an item from the list when the close button is clicked
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const itemName = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Are you sure?")) {
        div.remove()
        deleteItem(itemName)
        alert("Removed!")
      }
    }
  }
}

// Function to delete an item from the server list via DELETE request
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/company?company_name=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Function to add a new item with company name, trading name, and other details
const newItem = () => {
  let inputCompany = document.getElementById("newInput").value;
  let inputTradingName = document.getElementById("newTradingName").value;
  let inputCnpj = document.getElementById("newCnpj").value;
  let inputContact = document.getElementById("newContact").value;
  let inputPhone = document.getElementById("newPhone").value;
  let inputEmail = document.getElementById("newEmail").value;

  let errorMessage = '';

  if (inputCompany === '') {
      errorMessage += "Company name \n";
  } if (inputTradingName === '') {
      errorMessage += "Trading name \n";
  } if (inputCnpj === '') {
      errorMessage += "CNPJ \n";
  } if (inputContact === '') {
      errorMessage += "Contact name \n";
  } if (inputPhone === '') {
      errorMessage += "Phone \n";
  } if (inputEmail === '') {
      errorMessage += "Email \n";
  } if (errorMessage !== '') {
    alert("The following fields are mandatory:\n" + errorMessage);
  } else {
    insertList(inputCompany, inputTradingName, inputCnpj, inputContact, inputPhone, inputEmail);
    postItem(inputCompany, inputTradingName, inputCnpj, inputContact, inputPhone, inputEmail);
    alert("Item added!");
  }
}

// Function to insert items into the presented list
const insertList = (nameCompany, TradingName, Cnpj, Contact, Phone, Email) => {
  var item = [nameCompany, TradingName, Cnpj, Contact, Phone, Email]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1))
  document.getElementById("newInput").value = "";
  document.getElementById("newTradingName").value = "";
  document.getElementById("newCnpj").value = "";
  document.getElementById("newContact").value = "";
  document.getElementById("newPhone").value = "";
  document.getElementById("newEmail").value = "";

  removeElement()
}
