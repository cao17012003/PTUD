const input = document.querySelector("input#nameInput");
const phoneInput = document.querySelector("input#phoneInput");
const addButton = document.querySelector(".add-button");
const todosHtml = document.querySelector(".todos");
const emptyImage = document.querySelector(".empty-image");
let todosJson = JSON.parse(localStorage.getItem("todos")) || [];
const deleteAllButton = document.querySelector(".delete-all");
const filters = document.querySelectorAll(".filter");
let filter = '';

showTodos();

function getTodoHtml(todo, index) {
  if (filter && filter != todo.status) {
    return '';
  }
  let checked = todo.status == "completed" ? "checked" : "";
  return /* html */ `
    <li class="todo">
      <label for="${index}">
        <input id="${index}" onclick="updateStatus(this)" type="checkbox" ${checked}>
        <span class="todo-name ${checked}" data-index="${index}" data-phone="${todo.phone}">${todo.name}</span>
      </label>
      <button class="delete-btn" data-index="${index}" onclick="remove(this)"><i class="fa fa-times"></i></button>
      <button class="edit-btn" data-index="${index}" onclick="editContact(this)"><i class="fa fa-pencil"></i></button>
    </li>
  `; 
}

function showTodos() {
  if (todosJson.length == 0) {
    todosHtml.innerHTML = '';
    emptyImage.style.display = 'block';
  } else {
    todosHtml.innerHTML = todosJson.map(getTodoHtml).join('');
    emptyImage.style.display = 'none';
  }
}

function addTodo()  {
  let name = input.value.trim();
  let phone = phoneInput.value.trim();
  if (!name || !phone) {
    return;
  }
  input.value = "";
  phoneInput.value = "";
  todosJson.unshift({ name: name, phone: phone, status: "pending" });
  localStorage.setItem("todos", JSON.stringify(todosJson));
  showTodos();
}

input.addEventListener("keyup", e => {
  if (e.key != "Enter") {
    return;
  }
  addTodo();
});

phoneInput.addEventListener("keyup", e => {
  if (e.key != "Enter") {
    return;
  }
  addTodo();
});

addButton.addEventListener("click", () => {
  addTodo();
});

function updateStatus(todo) {
  let todoName = todo.parentElement.querySelector('.todo-name');
  if (todo.checked) {
    todoName.classList.add("checked");
    todosJson[todo.id].status = "completed";
  } else {
    todoName.classList.remove("checked");
    todosJson[todo.id].status = "pending";
  }
  localStorage.setItem("todos", JSON.stringify(todosJson));
}

function remove(button) {
  const index = button.dataset.index;
  todosJson.splice(index, 1);
  showTodos();
  localStorage.setItem("todos", JSON.stringify(todosJson));
}

function editContact(button) {
  const index = button.dataset.index;
  const newName = prompt("Nhập tên mới:", todosJson[index].name);
  const newPhone = prompt("Nhập số điện thoại mới:", todosJson[index].phone);
  if (newName !== null && newPhone !== null) {
    todosJson[index].name = newName.trim();
    todosJson[index].phone = newPhone.trim();
    localStorage.setItem("todos", JSON.stringify(todosJson));
    showTodos();
  }
}

filters.forEach(function (el) {
  el.addEventListener("click", (e) => {
    if (el.classList.contains('active')) {
      el.classList.remove('active');
      filter = '';
    } else {
      filters.forEach(tag => tag.classList.remove('active'));
      el.classList.add('active');
      filter = e.target.dataset.filter;
    }
    showTodos();
  });
});

todosHtml.addEventListener("click", (e) => {
  if (e.target.classList.contains("todo-name")) {
    const phone = e.target.dataset.phone;
    if (phone) {
      alert("Số điện thoại: " + phone);
    }
  }
});

deleteAllButton.addEventListener("click", () => {
  todosJson = [];
  localStorage.setItem("todos", JSON.stringify(todosJson));
  showTodos();
});
